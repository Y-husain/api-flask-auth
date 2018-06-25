from flask import Flask
from flask_restplus import Api
from app.configurations.config import app_config

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'access_token'
    }
}

api = Api(
    version="1.0",
    authorizations=authorization,
    title="Maintenance API",
    description="A simple Maintenance API",
    prefix='/api/v1')

#delete default namespace
del api.namespaces[0]


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    from app.endpoints.auth import auth_namespace as auth
    from app.endpoints.request import request_namespace as user
    api.add_namespace(auth, path='/auth')
    api.add_namespace(user, "/user")
    api.init_app(app)
    return app