# -*- coding: utf-8 *-*
from flask import Blueprint, render_template, flash, g, session
from lib.back_utils import BackUtils
from lib.format_utils import view_formatter

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET', 'POST'])
def view():
    """View"""
    import time
    from flask import request
    from datetime import date, timedelta, datetime
    # Set the current menu
    g.active_menu = 'dashboard'

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

    # Get metrics from date to date
    metrics = BackUtils().dashboard(session['date_begin'], session['date_end'])

    # Preprocess global metrics
    newspaper_sold = 0
    turnover = 0
    cost = 0
    if 'newspaper' in metrics['global_metrics']:
        newspaper_sold += metrics['global_metrics']['newspaper']['count'] \
            if metrics['global_metrics']['newspaper']['count'] is not None else 0
        turnover += metrics['global_metrics']['newspaper']['price'] \
            if metrics['global_metrics']['newspaper']['price'] is not None else 0
        supplier_cost = metrics['global_metrics']['newspaper']['supplier_cost'] \
            if metrics['global_metrics']['newspaper']['supplier_cost'] is not None else 0
        royalty_cost = metrics['global_metrics']['newspaper']['royalty_cost'] \
            if metrics['global_metrics']['newspaper']['royalty_cost'] is not None else 0
        cost += supplier_cost + royalty_cost
    if 'delivery' in metrics['global_metrics']:
        turnover += metrics['global_metrics']['delivery']['price'] \
            if metrics['global_metrics']['delivery']['price'] is not None else 0
    if 'distribution_round' in metrics['global_metrics']:
        cost += metrics['global_metrics']['distribution_round']['cost'] \
            if metrics['global_metrics']['distribution_round']['cost'] is not None else 0
    margin = turnover - cost
    global_metrics = {'newspaper_sold': newspaper_sold,
                      'turnover': turnover,
                      'cost': cost,
                      'margin': margin}

    # Preprocess date metrics
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

    # Render the view
    return render_template('dashboard/view.html',
                           view_formatter=view_formatter,
                           date_begin=session['date_begin'],
                           date_end=session['date_end'],
                           global_metrics=global_metrics,
                           date_metrics=date_metrics)
