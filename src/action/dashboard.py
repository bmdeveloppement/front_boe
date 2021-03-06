# -*- coding: utf-8 *-*
from flask import Blueprint, render_template, session, g
from lib.back_utils import BackUtils
from lib.dashboard_utils import DashboardUtils
from lib.format_utils import view_formatter

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET', 'POST'])
def view():
    """View"""
    from flask import request

    # Set the current menu
    g.active_menu = 'dashboard'

    # Refresh date_begin and date_end
    DashboardUtils().refresh_date_range(request)

    # Get metrics from date to date
    metrics = BackUtils().dashboard(session['date_begin'], session['date_end'])

    # Preprocess global metrics
    global_metrics = DashboardUtils().preprocess_global_metrics(metrics)

    # Preprocess date metrics
    date_metrics = DashboardUtils().preprocess_date_metrics(metrics)

    # Render the view
    return render_template('dashboard/view.html',
                           view_formatter=view_formatter,
                           date_begin=session['date_begin'],
                           date_end=session['date_end'],
                           global_metrics=global_metrics,
                           date_metrics=date_metrics)
