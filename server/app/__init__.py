from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from .instance import AppConfig
from .api import register_resources

def create_app(config_class=AppConfig):
    app = Flask(__name__)
    api = Api(app)

    CORS(app)
    app.config.from_object(config_class)
    register_resources(api)

    return app