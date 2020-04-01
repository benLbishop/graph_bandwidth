from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from .WindowRetriever import WindowRetriever

# set up the app
app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(WindowRetriever, '/bandwidths')