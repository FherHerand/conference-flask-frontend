# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    from . import api
    app.register_blueprint(api.bp)

    return app