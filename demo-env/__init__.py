from flask import Flask, redirect
from flask.helpers import send_from_directory
from flask_jwt_extended import JWTManager
from flask_monogoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config

db: MongoEngine = MongoEngine()

#Flask Initialization
app = Flask(__name__)

#Initialize jwt manager using the secret key
app.config['JWT_SCERET_KEY'] = 'Containerized-Platform'














