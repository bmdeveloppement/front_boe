# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash, g
from lib.back_utils import BackUtils
from lib.format_utils import view_formatter

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET', 'POST'])
def view():
    """View"""
    # Set the current menu
    g.active_menu = 'dashboard'

    date_begin = '2010-01-01'
    date_end = '2014-12-01'

    # Get metrics from date to date
    metrics = BackUtils().dashboard(date_begin, date_end)

    # Preprocess global metrics
    newspaper_sold = metrics['global_metrics']['newspaper']['count']
    turnover = metrics['global_metrics']['newspaper']['price'] + \
        metrics['global_metrics']['delivery']['price']
    cost = metrics['global_metrics']['newspaper']['supplier_cost'] + \
        metrics['global_metrics']['newspaper']['royalty_cost'] + \
        metrics['global_metrics']['distribution_round']['cost']
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
                           global_metrics=global_metrics,
                           date_metrics=date_metrics)
