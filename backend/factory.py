  
import os
import sys
from flask import Flask, send_from_directory, request, jsonify, render_template
from flask_cors import CORS
from .routes import carRoutes
from .config import DB_URI

def create_app(config):

    # global configuration
    app = Flask(__name__, static_folder='./../frontend')
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    CORS(app)

    @app.after_request
    def add_header(response):
        return response

    # adding blueprint is a set of subroutes for specific models (in this case for cars)
    app.register_blueprint(carRoutes)

    # heartbeat route (test if the app works correctly by going to 'localhost:5000/api/heartbeat')
    # if this works it means atleast the server is running correctly (it doesn't mean the DB is connected)
    @app.route('/api/heartbeat', methods=['GET', 'POST'])
    def heartbeat():
        return jsonify(message="It's working")

    # this is how we serve the AngularJS frontend application (AngularJS has it's own routing system defined)
    # all routes except the frontend should start with /api/
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # error handlers for flask
    @app.errorhandler(500)
    def server_error(e):
        return jsonify(error="500 internal error")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="404 route not found")

    return app