from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from .instance import AppConfig
from .api import register_resources
from . import scheduler

api: Api | None = None
app: Flask | None = None


def create_app(config_class=AppConfig):
    global api, app

    app = Flask(__name__)
    api = Api(app, doc='/docs')

    CORS(app)
    app.config.from_object(config_class)
    register_resources(api)
    scheduler.start()

    return app
