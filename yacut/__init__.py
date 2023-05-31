from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Config

BASE_URL = 'http://127.0.0.1:5000/'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from . import error_handlers, views