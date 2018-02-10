"""Load data into database."""

from model import Disaster, connect_to_db, db
from server import app
import pandas as pd 

#---------------------------------------------------------------------#

def get_disasters():
    """ Seeds DB. """

    df = pd.read_csv('./DisasterDeclarationsSummaries.csv')

    # Remove duplicates, missingness, NaNs

    df = df.drop_duplicates() 
    df = df.dropna(axis=0, how='all')
    df = df.dropna()
    df = df[~df.astype(str).eq('None').any(1)]
    df = df[df.astype(str).ne('None').all(1)]


    # Create Disaster instance for each row in dataset

    for i, row in df.iterrows():

        disaster = Disaster(disaster_num=row['disasterNumber'], 
                            state=row['state'], 
                            disaster_type=row['disasterType'],
                            incident_type=row['incidentType'],
                            title=row['title'],
                            start=row['incidentBeginDate'],
                            end=row['incidentEndDate'],
                            closeout=row['disasterCloseOutDate']
                            )
        # add instance to DB
        db.session.add(disaster)

    # commit all modifications to DB
    db.session.commit()

#---------------------------------------------------------------------#
if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    get_disasters()