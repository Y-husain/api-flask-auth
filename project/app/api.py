from flask import Flask
from flask_restplus import Api
from project.app.instance.config import app_config

api = Api(
    version="1.0",
    title="Maintenance API",
    description="A simple Maintenance API",
    prefix='/api/v1')

#delete default namespace
del api.namespaces[0]


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    return app
