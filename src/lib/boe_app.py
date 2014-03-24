# -*- coding: utf-8 -*-
from flask import Flask, request
import sys
import logging

from .configurator import Configurator


class BoeFlaskApplication(Flask):
    """
    Custom extension of Flask class, with modified logging handling.
    Currently, only HTTP Exception manually raised or exception are handled by
    the system.
    """

    def __init__(self, import_name, handlers=(), **kwargs):
        """
        :param import_name:
        :param kwargs:
        """
        super(BoeFlaskApplication, self).__init__(import_name, **kwargs)

        _conf = Configurator().get_setting('flask')
        self.debug = _conf.get('debug', False)
        self.profiling = _conf.get('profiling', False)
        if self.profiling:
            self.debug = True
            from werkzeug.contrib.profiler import ProfilerMiddleware
            self.wsgi_app = ProfilerMiddleware(self.wsgi_app, restrictions=[.1],
                                               sort_by=('tottime', 'calls'))

        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)
        self.logger.setLevel(logging.getLogger().getEffectiveLevel())

        for handler in handlers:
            self.logger.addHandler(handler)

    def log_exception(self, exc_info, status_code=500):
        """Overrides the standartd Flask exception logging system.
        Add request data to the log ent
        :param exc_info: The traceback information
        :param status_code: HTTP code of the logged exception
        Logs the exception on the :attr:`logger`, as an error if status_code is 500,
        as an info otherwise.
        """

        request_data = {
            'application': 'Flask',
            'request_form': request.form,
            'request_args': request.args,
            'request_headers': dict(request.headers),
            'request_remote_addr': request.remote_addr,
            'request_url': request.url,
            'request_status_code': status_code
        }

        if status_code == 500:
            self.logger.error('Exception on %s [%s]' % (request.path,
                                                        request.method),
                              exc_info=exc_info,
                              extra=request_data)
        elif status_code >= 400:
            self.logger.info('HTTPException on {0:s} [{1:s}]: {2:s}'.format(
                                    request.path,
                                    request.method,
                                    exc_info[1].message),
                             extra=request_data)

        else:
            self.logger.debug('HTTPException on {0:s} [{1:s}]: {2:s}'.format(
                                    request.path,
                                    request.method,
                                    exc_info[1].message),
                             extra=request_data)

    def handle_http_exception(self, e):
        """
            Override the standart Flask HTTPExceptionHandling, in order to log the exception
            as info.
        """
        status_code = getattr(e, 'code', 500)
        self.log_exception(sys.exc_info(), status_code)
        return super(BoeFlaskApplication, self).handle_http_exception(e)