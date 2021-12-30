# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from app.backend.clock_model import start_clock

db = SQLAlchemy()
login_manager = LoginManager()

clock_hand_seconds = ''
refresh_timeout = 0.5

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def start_backend(app):
    clock_outer_thread = threading.Thread(target=start_clock)
    clock_outer_thread.start()

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.refresh_timeout = 0.2
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    start_backend(app)
    configure_database(app)
    return app
