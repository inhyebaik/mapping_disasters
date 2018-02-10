"""Load data into database."""

from model import Disaster, connect_to_db, db
from server import app
import dateutil.parser
import pandas as pd 
from sqlalchemy.sql import label
from sqlalchemy import func


def get_disasters():
    """ Creates a disaster object for each row. """

    df = pd.read_csv('/DisasterDeclarationsSummaries.csv')

    # Remove duplicates, missingness, NaNs
    df = df.drop_duplicates() 
    df = df.dropna(axis=0, how='all')
    df = df.dropna()
    df = df[~df.astype(str).eq('None').any(1)]
    df = df[df.astype(str).ne('None').all(1)]

    