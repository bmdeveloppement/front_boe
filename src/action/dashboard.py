# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash, g
from lib.back_utils import BackUtils

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

    # Render the view
    return render_template('dashboard/view.html',
                           global_metric=metrics['newspaper_global_metrics'],
                           date_metrics=metrics['newspaper_date_metrics'])
