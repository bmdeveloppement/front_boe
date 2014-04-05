# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils
from form.press_title import AddForm, EditForm
from action.crud import CrudAction

view = 'press-title'
press_title_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'name', 'supplier_cost', 'royalty_cost', 'paging']
translations = ['#', 'Name', 'Supplier Cost', 'Royalty Cost', 'Paging']
key_name = 'address'


@press_title_bp.route('/<int:reference_id>')
def get(reference_id):
    """Get full item"""
    item = BackUtils().get_full('press_title', reference_id)

    # Update keys to show details
    keys = ['id', 'supplier', 'name', 'supplier_cost',
            'royalty_cost', 'paging']
    translations = ['#', 'Supplier', 'Name', 'Supplier Cost',
                    'Royalty Cost', 'Paging']

    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)


@press_title_bp.route('/', methods=['GET'])
@press_title_bp.route('/page/<int:page>', methods=['GET'])
@press_title_bp.route('/page/<int:page>/order_by/<string:order_by>/sort/<string:sort>', methods=['GET'])
def list(page=1, order_by='name', sort='asc'):
    """List items"""
    return CrudAction().list(view, keys, translations, page, order_by, sort)


@press_title_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add an item"""
    form = AddForm(csrf_enabled=False)

    # Get list
    suppliers = BackUtils().list_field('supplier', 'company_name')
    form.supplier_id.choices = suppliers

    # Update keys to send id to Back
    keys = ['id', 'supplier_id', 'name', 'supplier_cost',
            'royalty_cost', 'paging']

    return CrudAction().add(view, form, keys, key_name)


@press_title_bp.route('/edit/<int:reference_id>', methods=['GET', 'POST'])
def edit(reference_id):
    """Edit an item"""
    form = AddForm(csrf_enabled=False)

    # Get list
    suppliers = BackUtils().list_field('supplier', 'company_name')
    form.supplier_id.choices = suppliers

    # Update keys to send id to Back
    keys = ['id', 'supplier_id', 'name', 'supplier_cost',
            'royalty_cost', 'paging']

    return CrudAction().edit(view, form, keys, key_name, reference_id)


@press_title_bp.route('/delete/<int:reference_id>', methods=['GET'])
@press_title_bp.route('/delete/<int:reference_id>/confirmed/<int:confirmed>', methods=['GET'])
def delete(reference_id, confirmed=False):
    """Delete items"""
    return CrudAction().delete(view, key_name, reference_id, confirmed)
