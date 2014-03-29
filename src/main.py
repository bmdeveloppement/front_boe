#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import traceback

from os import path
from flask import redirect, url_for, make_response, g, session
from lib.configurator import Configurator
from lib.boe_app import BoeFlaskApplication

sys.path.append(path.dirname(__file__))
Configurator(os.path.dirname(__file__))
application = BoeFlaskApplication(__name__,
                                  template_folder='templates',
                                  static_folder='public')

@application.route('/')
def root():
    return redirect(url_for('client.list'))

def import_blueprints():
    """Import BPs"""
    from action.client import client_bp

    application.register_blueprint(client_bp)

@application.before_request
def authentify():
    """Authentify request before treatment"""
    pass

def set_http_handlers():
    @application.errorhandler(Exception)
    def silent_death(error=None):
        """Forbidden handler"""
        print traceback.print_exc()
        resp = make_response('')
        resp.status_code = 200
        return resp

    @application.errorhandler(403)
    def forbidden(error=None):
        """Forbidden handler"""
        resp = make_response('Forbidden Access')
        resp.status_code = 403
        return resp

    @application.after_request
    def after_request(response):
        """Executed after every request"""
        # Set a custom header
        try:
            response.headers['X-Boe-Header'] = Configurator().boe_header
        except:
            pass

        return response

set_http_handlers()
import_blueprints()