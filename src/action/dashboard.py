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
    newspaper_sold = metrics['newspaper_global_metrics']['count']
    turnover = metrics['newspaper_global_metrics']['price'] + \
        metrics['delivery_global_metrics']['price']
    cost = metrics['newspaper_global_metrics']['supplier_cost'] + \
        metrics['newspaper_global_metrics']['royalty_cost'] + \
        metrics['distribution_round_global_metrics']['cost']
    margin = turnover - cost
    global_metrics = {'newspaper_sold': newspaper_sold,
                      'turnover': turnover,
                      'cost': cost,
                      'margin': margin}

    # Render the view
    return render_template('dashboard/view.html',
                           view_formatter=view_formatter,
                           global_metrics=global_metrics,
                           newspaper_global_metrics=metrics['newspaper_global_metrics'],
                           newspaper_date_metrics=metrics['newspaper_date_metrics'],
                           delivery_global_metrics=metrics['delivery_global_metrics'],
                           delivery_date_metrics=metrics['delivery_date_metrics'],
                           distribution_round_global_metrics=metrics['distribution_round_global_metrics'],
                           distribution_round_date_metrics=metrics['distribution_round_date_metrics'])
