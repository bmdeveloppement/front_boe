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
        self.per_page_result = int(Configurator().get_setting('crud')['result_per_page'])
        self.list_limit = int(Configurator().get_setting('crud')['list_limit'])

    @load_response
    def get(self, key, reference_id):
        """Get an item by key & ref_id"""
        uri = '%s/%s/%s' % (self.url_back_boe,
                            key.replace('-', '_'),
                            reference_id)
        return requests.get(uri, data='')

    @load_response
    def get_full(self, key, reference_id):
        """Get a full item by key & ref_id"""
        uri = '%s/%s/get_full/%s' % (self.url_back_boe,
                                     key.replace('-', '_'),
                                     reference_id)
        return requests.get(uri, data='')

    @load_response
    def list(self, key, page, order_by):
        """Get a list by key"""
        uri = '%s/%s/' % (self.url_back_boe, key.replace('-', '_'))
        return requests.post(uri, data={u'order_by': order_by,
                                        u'limit': self.per_page_result,
                                        u'offset': (page - 1) * self.per_page_result})

    @load_response
    def list_field(self, key, field_name):
        """Get a field list by key"""
        uri = '%s/%s/field_name/%s' % (self.url_back_boe,
                                       key.replace('-', '_'),
                                       field_name)
        return requests.post(uri, data={u'order_by': field_name + ' asc',
                                        u'limit': self.list_limit})

    @load_response
    def add(self, key, data):
        """Add a new item"""
        uri = '%s/%s/' % (self.url_back_boe, key.replace('-', '_'))
        return requests.put(uri, data=data)

    @load_response
    def edit(self, key, reference_id, data):
        """Edit an item"""
        uri = '%s/%s/%s' % (self.url_back_boe,
                            key.replace('-', '_'),
                            reference_id)
        return requests.post(uri, data=data)

    @load_response
    def delete(self, key, reference_id):
        """Delete an item"""
        uri = '%s/%s/%s' % (self.url_back_boe,
                            key.replace('-', '_'),
                            reference_id)
        return requests.delete(uri)

    @load_response
    def dashboard(self, date_begin, date_end):
        """Overview for dashboard statistics"""
        uri = '%s/dashboard/' % (self.url_back_boe)
        return requests.post(uri, data={u'date_begin': date_begin,
                                        u'date_end': date_end})
