from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#import os

app = Flask(__name__)
app.app_context().push()

# set the SQLALCHEMY_DATABASE_URI key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:postgres@34.68.47.133:5432/app-service-db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:postgres@10.79.48.5:5432/app-service-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

#create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)

#instantiate LoginManager with instance app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


import routes
from models import *
db.create_all()
