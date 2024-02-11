# app.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import os

# load local variables from .env
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.app_context().push()

# set the SQLALCHEMY_DATABASE_URI key from environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

# create an SQLAlchemy object db and bind it to app
db = SQLAlchemy(app)

# instantiate LoginManager with instance app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# # create database
import routes
# from models import *
# db.create_all()
