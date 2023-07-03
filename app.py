### pre_beta
#https://www.youtube.com/watch?v=IBfj_0Zf2Mo

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#import pg8000
#from connect_unix import get_connect_url
import os
#from os import environ

app = Flask(__name__)

### important remember to set environmental variable in render as Python 3.10.4 and internal db
#db name = relistprebetatest1
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/db_app'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace("://", "ql://", 1)
#app.config['SQLALCHEMY_DATABASE_URI'] = get_connect_url()
#external render: postgresql://relistprebetatest1_user:RL4PpbEkDeNftL3GH8ixAirOmZ0r0tkr@dpg-cihfhrl9aq012etacut0-a.ohio-postgres.render.com/relistprebetatest1

#DATABASE_URL=postgresql://relistprebetatest1_user:RL4PpbEkDeNftL3GH8ixAirOmZ0r0tkr@dpg-cihfhrl9aq012etacut0-a.ohio-postgres.render.com/relistprebetatest1
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# use db beaver to view database

app.app_context().push()
app.config["SESSION_PERMANENT"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SESSION_COOKIE_NAME'] = "my_session"

db = SQLAlchemy(app)
#db.init_app(app)

migrate = Migrate(app, db)

#instantiate LoginManager with instance app
login_manager = LoginManager()
login_manager.init_app(app)
#endpoint to login object to redirect not logged in users
login_manager.login_view = 'login'

import routes
from models import *
#db.create_all()

#heroku run python
# >>> from app import db
# >>> db.create_all()

#heroku run python add_data.py

# activate virtual environment: $source ./Scripts/activate 
# deactivate:$deactivate

#configure debug mode
# app.config['ENV'] = 'development'
# app.config['DEBUG'] = True
# app.config['TESTING'] = True

# run this
# $ export FLASK_ENV=development 
# $ export FLASK_DEBUG=1

#git add .
#git commit -m 'html tag modification'
#git push origin master

