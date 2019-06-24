from gevent import monkey
monkey.patch_all()

from os import environ

from flask import Flask
from flask_caching import Cache
from flask_bootstrap import Bootstrap
from flask_debug import Debug
from flask_debugtoolbar import DebugToolbarExtension

import threading
from werkzeug.serving import make_server

from appointment_comparer.webapp.base import base
from appointment_comparer.webapp.compareauthors import compareauthors
from appointment_comparer.webapp.filter import friendly_time


class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.logger = app.logger
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()#
        
    def run(self):
        # self.logger.info('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


server = None

def start_server():
    global server
    app = Flask('Flask server')
    
    Bootstrap(app)
    Debug(app)

    # Check Configuring Flask-Cache section for more details
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    # register blueprints
    app.register_blueprint(base)
    app.register_blueprint(compareauthors)

    # register filter
    app.jinja_env.filters['friendly_time'] = friendly_time

    toolbar = DebugToolbarExtension(app)

    server = ServerThread(app)
    server.start()
    # app.logger.info('server started')

def stop_server():
    global server
    server.shutdown()

