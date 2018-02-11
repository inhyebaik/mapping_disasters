""" Data model for disasters. """

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

DATABASE_URL = os.environ.get('DATABASE_URL')
#---------------------------------------------------------------------#

class Disaster(db.Model):
    """ Disaster object. """

    __tablename__ = 'disasters'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    disaster_num = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(10), nullable=True)
    state_lat = db.Column(db.String(100), nullable=True)
    state_long = db.Column(db.String(100), nullable=True)
    disaster_type = db.Column(db.String(10), nullable=True)
    incident_type = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(200), nullable=True)
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)
    closeout = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """ Cleaner representation of disaster. """

        repr_str = "<Disaster id={id} state={state}>"
        return repr_str.format(id=self.id, state=self.state)

#---------------------------------------------------------------------#

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."

