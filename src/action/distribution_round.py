# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils
from form.distribution_round import AddForm, EditForm
from action.crud import CrudAction

view = 'distribution-round'
distribution_round_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'name', 'cost', 'unitary_cost']
translations = ['#', 'Name', 'Cost', 'Unitary Cost']


@distribution_round_bp.route('/<int:reference_id>')
def get(reference_id):
    """Get full item"""
    item = BackUtils().get_full('distribution_round', reference_id)

    # Update keys to show deliverer details
    keys = ['id', 'deliverer', 'name', 'cost', 'unitary_cost', 'schedule']
    translations = ['#', 'Deliverer', 'Name', 'Cost', 'Unitary Cost',
                    'Schedule']

    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)


@distribution_round_bp.route('/', methods=['GET'])
@distribution_round_bp.route('/page/<int:page>', methods=['GET'])
@distribution_round_bp.route('/page/<int:page>/order_by/<string:order_by>/sort/<string:sort>', methods=['GET'])
def list(page=1, order_by='name', sort='asc'):
    """List items"""
    items = BackUtils().list(view, page, order_by + ' ' + sort)
    return render_template('crud/list.html', view=view, items=items,
                           keys=keys, translations=translations,
                           page=page, order_by=order_by, sort=sort)


@distribution_round_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add an item"""
    form = AddForm(csrf_enabled=False)

    # Get list
    deliverers = BackUtils().list_field('deliverer', 'company_name')
    form.deliverer_id.choices = deliverers

    # Update keys to send id to Back
    keys = ['id', 'deliverer_id', 'name', 'cost', 'unitary_cost', 'schedule']

    return CrudAction().add(view, form, keys, 'name')


@distribution_round_bp.route('/edit/<int:reference_id>', methods=['GET', 'POST'])
def edit(reference_id):
    """Edit an item"""
    form = AddForm(csrf_enabled=False)

    # Get list
    deliverers = BackUtils().list_field('deliverer', 'company_name')
    form.deliverer_id.choices = deliverers

    # Update keys to send id to Back
    keys = ['id', 'deliverer_id', 'name', 'cost', 'unitary_cost', 'schedule']

    return CrudAction().edit(view, form, keys, 'name', reference_id)