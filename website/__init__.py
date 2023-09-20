from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__) #represents the name of the file that was ran
    app.config['SECRET_KEY'] = 'o12epm zknvi0n' #a secret key for the app, ideally don't share it to anyone
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)



    from .views import views #from the views.py import the variable views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) #telling the login manager which app we are using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #looking for the primary key and check if its equal to the one that we passed 

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME): #make a module and check if the database exists
        with app.app_context():
            db.create_all() #if it doesn't, its gonna create one
        print('Created Database!') #print

        