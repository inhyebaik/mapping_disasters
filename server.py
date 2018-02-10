from jinja2 import StrictUndefined
from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import datetime

from model import connect_to_db, db, Disaster

app = Flask(__name__)
app.secret_key = "abc"
app.jinja_env.undefined = StrictUndefined