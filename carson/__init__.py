from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('carson.default_settings')

db = SQLAlchemy(app)

from . import api
from . import models
