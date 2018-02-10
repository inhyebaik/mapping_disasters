from jinja2 import StrictUndefined
from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql import label
from sqlalchemy import func
import datetime

from model import connect_to_db, db, Disaster

app = Flask(__name__)
app.secret_key = "abc"
app.jinja_env.undefined = StrictUndefined


#---------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disasters')
def show_map():

    TYPES = ['Flood', 'Tornado', 'Earthquake', 'Severe Storm(s)', 'Drought', 
            'Hurricane', 'Typhoon', 'Fire', 'Severe Ice Storm', 'Freezing', 
            'Snow', 'Coastal Storm', 'Fishing Losses', 'Dam/Levee Break', 
            'Mud/Landslide', 'Volcano', 'Toxic Substances', 'Human Cause', 
            'Terrorist', 'Tsunami']

    return render_template('map.html', TYPES=TYPES)

@app.route('/disasters.json')
def get_disasters_data():

    incident_type = request.args.get('incident_type')
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')

    if incident_type == 'all':
        q = db.session.query(Disaster.state, label('count', func.count(Disaster.disaster_num))).filter(Disaster.start >= min_date, Disaster.start <= max_date).group_by(Disaster.state).all()
    else:
        q = db.session.query(Disaster.state, label('count', func.count(Disaster.disaster_num))).filter(Disaster.incident_type==incident_type, Disaster.start >= min_date, Disaster.start <= max_date).group_by(Disaster.state).all()

    disasters = { 'counts':[] }
    
    latlong = {'WA': (47.400902, -121.490494), 'DE': (39.318523, -75.507141), 
           'DC': (38.897438, -77.026817), 'WI': (44.268543, -89.616508), 
           'WV': (38.491226, -80.954453), 'HI': (21.094318, -157.498337), 
           'FL': (27.766279, -81.686783), 'WY': (42.755966, -107.30249), 
           'NH': (43.452492, -71.563896), 'NJ': (40.298904, -74.521011), 
           'NM': (34.840515, -106.248482), 'TX': (31.054487, -97.563461), 
           'LA': (31.169546, -91.867805), 'NC': (35.630066, -79.806419), 
           'ND': (47.528912, -99.784012), 'NE': (41.12537, -98.268082), 
           'TN': (35.747845, -86.692345), 'NY': (42.165726, -74.948051), 
           'PA': (40.590752, -77.209755), 'CA': (36.116203, -119.681564), 
           'NV': (38.313515, -117.055374), 'VA': (37.769337, -78.169968), 
           'CO': (39.059811, -105.311104), 'AK': (61.370716, -152.404419), 
           'AL': (32.806671, -86.79113), 'AR': (34.969704, -92.373123), 
           'VT': (44.045876, -72.710686), 'IL': (40.349457, -88.986137), 
           'GA': (33.040619, -83.643074), 'IN': (39.849426, -86.258278), 
           'IA': (42.011539, -93.210526), 'OK': (35.565342, -96.928917), 
           'AZ': (33.729759, -111.431221), 'ID': (44.240459, -114.478828), 
           'CT': (41.597782, -72.755371), 'ME': (44.693947, -69.381927), 
           'MD': (39.063946, -76.802101), 'MA': (42.230171, -71.530106), 
           'OH': (40.388783, -82.764915), 'UT': (40.150032, -111.862434), 
           'MO': (38.456085, -92.288368), 'MN': (45.694454, -93.900192), 
           'MI': (43.326618, -84.536095), 'RI': (41.680893, -71.51178), 
           'KS': (38.5266, -96.726486), 'MT': (46.921925, -110.454353), 
           'MS': (32.741646, -89.678696), 'SC': (33.856892, -80.945007), 
           'KY': (37.66814, -84.670067), 'OR': (44.572021, -122.070938), 
           'SD': (44.299782, -99.438828), 'PR': (18.2208, 66.5901), 
           'GU': (13.4443, 144.7937), 'AS': (14.2710, 170.1322),
           'VI': (18.3358, 64.8963), 'PW': (7.5150, 134.5825), 
           'MP': (15.0979, 145.6739), 'FM': (7.4256, 150.5508), 
           'MH':(7.1315, 171.1845)}

    COLORS = {  'Chemical': "green",
                'Coastal Storm':"blue",
                'Dam/Levee Break':"brown",
                 'Drought':"lightGray",
                 'Earthquake':"darkGray",
                 'Fire':"orange",
                 'Fishing Losses':"blue",
                 'Flood':"lightBlue",
                 'Freezing':"white",
                 'Human Cause': 'olive',
                 'Hurricane':"blue",
                 'Mud/Landslide':"brown",
                 'Other':"purple",
                 'Severe Ice Storm':'white',
                 'Severe Storm(s)':"red",
                 'Snow':"white",
                 'Terrorist':"black",
                 'Tornado':"gray",
                 'Toxic Substances': "yellow",
                 'Tsunami':"lightBlue",
                 'Typhoon':"purple",
                 'Volcano':"pink",
                 'all': 'red'
                }

    for disaster in q:
        
        state, count = disaster
        lat, lo = latlong[state]

        disasters[state] = {
            "count": count,
            'state': state,
            'start': min_date,
            'end': max_date,
            'stateLat':lat,
            'stateLong':lo,
            'incidentType': incident_type,
            'color': COLORS[incident_type],
        }

        disasters['counts'].append(count)

    disasters['counts'].sort()
    print disasters['counts']
    return jsonify(disasters)


#---------------------------------------------------------------------#
if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(port=5000, host="0.0.0.0")