from flask import Flask, request
from flask_restplus import Api

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Maintenance API",
    description="A simple Maintenance API",
    prefix='/api/v1')

#delete default namespace
del api.namespaces[0]