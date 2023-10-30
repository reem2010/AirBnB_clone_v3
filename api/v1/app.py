#!/usr/bin/python3
"""the app file"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(var):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if os.environ.get('HBNB_API_HOST'):
        host = os.environ.get('HBNB_API_HOST')
    if os.environ.get('HBNB_API_PORT'):
        port = int(os.environ.get('HBNB_API_PORT'))
    app.run(host=host, port=port, threaded=True)
