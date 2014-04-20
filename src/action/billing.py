# -*- coding: utf-8 *-*
from flask import Blueprint, render_template, session, g
from lib.back_utils import BackUtils
from lib.dashboard_utils import DashboardUtils
from lib.format_utils import view_formatter, fill_zero_if_unset

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')


@billing_bp.route('/client', methods=['GET', 'POST'])
def client():
    """View"""
    from flask import request

    # Set the current menu
    g.active_menu = 'billing'

    # Refresh date_begin and date_end
    DashboardUtils().refresh_date_range(request)

    # Get metrics from date to date
    metrics = BackUtils().dashboard(session['date_begin'], session['date_end'])

    # Preprocess metrics
    global_metrics = DashboardUtils().preprocess_global_metrics(metrics)
    date_metrics = DashboardUtils().preprocess_date_metrics(metrics)

    # Get billing
    billing = BackUtils().billing('client',
                                  session['date_begin'],
                                  session['date_end'])
    # Render the view
    return render_template('billing/client.html',
                           view_formatter=view_formatter,
                           date_begin=session['date_begin'],
                           date_end=session['date_end'],
                           global_metrics=global_metrics,
                           date_metrics=date_metrics,
                           billing=billing)


@billing_bp.route('/supplier', methods=['GET', 'POST'])
def supplier():
    """View"""
    from flask import request


@billing_bp.route('/deliverer', methods=['GET', 'POST'])
def deliverer():
    """View"""
    from flask import request