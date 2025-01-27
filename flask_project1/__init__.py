from flask import Flask # it's a class using create a app
from flask_sqlalchemy import SQLAlchemy #for database intractions
from flask_login import LoginManager #for creating login session
from flask_migrate import Migrate

import os

db = SQLAlchemy() #instance for SQLAlchemy

#SECRET_KEY = os.getenv('SECRET_KEY') #get the env variables and store to variable for security
#DB_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
#SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
def create_app():

    app = Flask(__name__) # create a instance for a Flask class (object)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir,'db.sqlite')}"
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app) #initialize the app for database

    migrate = Migrate(app, db)

    #create instance for LoginManager class
    login_manager = LoginManager()

    login_manager.login_view = 'auth.login' #login view

    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint # import our main blueprint

    app.register_blueprint(main_blueprint) # register our main blueprint

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)
    
    return app # return the app



