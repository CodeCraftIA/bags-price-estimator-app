#this python file will make the website folder an python package

from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from os import path

# Function to create and configure the Flask application.
def create_app():
    # Creating an instance of the Flask class. This instance represents your web application.
    app = Flask(__name__, static_folder='static')
    # Setting the secret key for the Flask application. This key should be a random and secure token.
    app.config['SECRET_KEY'] = 'xxx'

    from .views import views

    # Registering blueprints. Blueprints are used for organizing your application into distinct components.
    app.register_blueprint(views, url_prefix= '/')

    
    # Creating the database tables based on the models.
    with app.app_context():
        print('App ready to use')
    
    # Returning the Flask app instance.
    return app

