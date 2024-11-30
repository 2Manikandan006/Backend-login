from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()       # sql data base 
DB_NAME = "database.db" # sql data base 

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Iam Batman as well as Leo Dass"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # sql data base 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db.init_app(app) # sql data base 
    print("Database initialized with app!")
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note


    create_database(app)     # return create_database

    
    login_manager = LoginManager      #??      
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))     #??

    return app

def create_database(app):      # creating database
    if not path.exists('website/' + DB_NAME):     # if there is no database exists create new
         print("Database does not exists. Creating...")
         with app.app_context(): 
            db.create_all()
            print("Created Database!.")
    else:
        print("Database already exists.")