from flask_sqlalchemy import SQLAlchemy

""" Data model for disasters. """
db = SQLAlchemy()

class Disaster(db.Model):
    """ Disaster object. """

    __tablename__ = 'disasters'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    disaster_num = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(10), nullable=True)
    disaster_type = db.Column(db.String(10), nullable=True)
    incident_type = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(200), nullable=True)

    