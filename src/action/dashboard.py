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

    # Get a sum of metrics for the period
    global_metrics = BackUtils().dashboard(date_begin,
                                           date_end)
    print global_metrics
    # Get day per day metrics
    # per_day_metrics = BackUtils().get_full(view, reference_id)

    # Render the view
    return render_template('dashboard/view.html')
