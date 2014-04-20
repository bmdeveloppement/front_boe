# -*- coding: utf-8 -*-


class DashboardUtils(object):

    def refresh_date_range(self, request):
        """Refresh date_begin and date_end in session"""
        import time
        from flask import request, session
        from datetime import date, timedelta, datetime
        # Default date range
        if 'date_begin' not in session:
            session['date_begin'] = date(date.today().year, date.today().month, 1)\
                .strftime('%Y-%m-%d')
        if 'date_end' not in session:
            session['date_end'] = date.today().strftime('%Y-%m-%d')
        # Override dates
        if 'date_begin' in request.args:
            session['date_begin'] = request.args['date_begin']
        if 'date_end' in request.args:
            session['date_end'] = request.args['date_end']
        # Specific cases for selection errors
        timestamp_begin = int(time.mktime(datetime.strptime(
            session['date_begin'], '%Y-%m-%d').timetuple()))
        timestamp_end = int(time.mktime(datetime.strptime(
            session['date_end'], '%Y-%m-%d').timetuple()))
        if timestamp_end < timestamp_begin:
            session['date_end'] = date.today().strftime('%Y-%m-%d')
            session['date_begin'] = date(date.today().year, date.today().month, 1)\
                .strftime('%Y-%m-%d')

    def preprocess_global_metrics(self, metrics):
        """Format global metrics for dashboard views"""
        from lib.format_utils import fill_zero_if_unset
        newspaper_sold = 0
        turnover = 0
        cost = 0
        if 'newspaper' in metrics['global_metrics']:
            newspaper_sold += fill_zero_if_unset(metrics['global_metrics']
                                                 ['newspaper']['count'])
            turnover += fill_zero_if_unset(metrics['global_metrics']
                                           ['newspaper']['price'])
            supplier_cost = fill_zero_if_unset(metrics['global_metrics']
                                               ['newspaper']['supplier_cost'])
            royalty_cost = fill_zero_if_unset(metrics['global_metrics']
                                              ['newspaper']['royalty_cost'])
            cost += supplier_cost + royalty_cost
        if 'delivery' in metrics['global_metrics']:
            turnover += fill_zero_if_unset(metrics['global_metrics']
                                           ['delivery']['price'])
        if 'distribution_round' in metrics['global_metrics']:
            cost += fill_zero_if_unset(metrics['global_metrics']
                                       ['distribution_round']['cost'])
        margin = turnover - cost
        global_metrics = {'newspaper_sold': newspaper_sold,
                          'turnover': turnover,
                          'cost': cost,
                          'margin': margin}
        return global_metrics

    def preprocess_date_metrics(self, metrics):
        """Format date metrics for dashboard views"""
        date_metrics = []
        for date, date_metric in metrics['date_metrics']:
            newspaper_sold = 0
            turnover = 0
            cost = 0
            for metric in date_metric:
                if 'newspaper' in metric:
                    newspaper_sold += metric['newspaper']['count']
                    turnover += metric['newspaper']['price']
                    cost += metric['newspaper']['supplier_cost'] \
                        + metric['newspaper']['royalty_cost']
                if 'delivery' in metric:
                    turnover += metric['delivery']['price']
                if 'distribution_round' in metric:
                    cost += metric['distribution_round']['cost']
            margin = turnover - cost
            date_metrics.append({'date': date,
                                 'newspaper_sold': newspaper_sold,
                                 'turnover': turnover,
                                 'cost': cost,
                                 'margin': margin})
        return date_metrics