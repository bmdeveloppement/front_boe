# -*- coding: utf-8 -*-
import json
import requests

from lib.configurator import Configurator
from lib.singleton import Singleton
from lib.http_utils import load_response


class BackUtils(Singleton):
    def __init__(self):
        """Initilize mandatories attributes"""
        self.url_back_boe = Configurator().get_setting('application')['url_back_boe']

    @load_response
    def get(self, key, reference_id):
        """Get an item by key & ref_id"""
        uri = '%s/%s/%s' % (self.url_back_boe, key, reference_id)
        return requests.get(uri, data='')

    @load_response
    def get_full(self, key, reference_id):
        """Get a full item by key & ref_id"""
        uri = '%s/%s/get_full/%s' % (self.url_back_boe, key, reference_id)
        return requests.get(uri, data='')

    @load_response
    def list(self, key):
        """Get a list by key"""
        uri = '%s/%s/' % (self.url_back_boe, key)
        return requests.post(uri, data='')
