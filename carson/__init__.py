import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


def populate_configs(config, variables):
    for v in variables:
        value = os.environ.get(v, None)
        if value is not None:
            config[v] = value


app = Flask(__name__)
app.config.from_object('carson.default_settings')
app.config.from_envvar('CARSON_SETTINGS', silent=True)

# Allow overrides of some configuration params directly with env variables
populate_configs(
    app.config,
    ["SECRET_KEY", "GITHUB_API_KEY", "SLACK_API_KEY", "SQLALCHEMY_DATABASE_URI"]
)

db = SQLAlchemy(app)

from . import api
from . import models
