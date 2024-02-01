from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from config import DevelopmentConfig, TestingConfig

# Set the environment variable to determine the configuration (development, testing, or production)
environment = 'development'  # Change this to 'testing' or 'production' as needed

# Initialize Flask application
app = Flask(__name__)

# Configure the application based on the environment
if environment == 'development':
    app.config.from_object(DevelopmentConfig)
elif environment == 'testing':
    app.config.from_object(TestingConfig)

# app = Flask(__name__)
# app.config.from_object(Config)
    
# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Import routes from the 'api' module
from app.api import routes