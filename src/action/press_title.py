# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils
from form.press_title import AddForm, EditForm
from action.crud import CrudAction

view = 'press-title'
press_title_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'name', 'supplier_cost', 'royalty_cost', 'paging']
translations = ['#', 'Name', 'Supplier Cost', 'Royalty Cost', 'Paging']


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


@press_title_bp.route('/')
def list():
    """List items"""
    items = BackUtils().list('press_title')
    return render_template('crud/list.html', view=view, items=items,
                           keys=keys, translations=translations)


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

    return CrudAction().add(view, form, keys, 'name')


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

    return CrudAction().edit(view, form, keys, 'name', reference_id)