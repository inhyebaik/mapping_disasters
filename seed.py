"""Load data into database."""
import pandas as pd 
import dateutil.parser

from model import Disaster, connect_to_db, db
from server import app

#---------------------------------------------------------------------#

def get_disasters():
    """ Seeds DB. """

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

    df = pd.read_csv('DisasterDeclarationsSummaries.csv')

    # Remove duplicates, missingness, NaNs

    df = df.dropna(axis=0, how='all')
    df = df.dropna()
    df = df[~df.astype(str).eq('None').any(1)]
    df = df[df.astype(str).ne('None').all(1)]
    df = df.drop_duplicates(['disasterNumber'])
    df = df.drop_duplicates()

    # Create Disaster instance for each row in dataset

    for i, row in df.iterrows():
        
        # get lat long for state
        state=row['state']
        state_lat, state_long = latlong[state]
        
        # convert to dates to datetime objects
        start = dateutil.parser.parse(str(row['incidentBeginDate']))
        end = dateutil.parser.parse(str(row['incidentEndDate']))
        closeout = dateutil.parser.parse(str(row['disasterCloseOutDate']))

        disaster = Disaster(disaster_num=row['disasterNumber'], 
                            state=state,
                            state_lat=str(state_lat),
                            state_long=str(state_long),
                            disaster_type=row['disasterType'],
                            incident_type=row['incidentType'],
                            title=row['title'],
                            start=start,
                            end=end,
                            closeout=closeout
                            )

        # add instance to DB
        db.session.add(disaster)


    # commit all modifications to DB
    db.session.commit()


#---------------------------------------------------------------------#
# if __name__ == '__main__':
#     connect_to_db(app, os.environ.get("DATABASE_URL"))
#     db.create_all(app=app)
#     get_disasters()