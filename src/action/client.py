# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils
from form.client import AddForm, EditForm
from action.crud import CrudAction

view = 'client'
client_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'company_name', 'email_address']
translations = ['#', 'Company Name', 'Email Address']


@client_bp.route('/<int:reference_id>', methods=['GET'])
def get(reference_id, methods=['GET']):
    """Get full item"""
    item = BackUtils().get_full(view, reference_id)
    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)


@client_bp.route('/', methods=['GET'])
def list():
    """List items"""
    items = BackUtils().list(view)
    return render_template('crud/list.html', view=view, items=items,
                           keys=keys, translations=translations)


@client_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add an item"""
    form = AddForm(csrf_enabled=False)
    return CrudAction().add(view, form, keys, 'company_name')


@client_bp.route('/edit/<int:reference_id>', methods=['GET', 'POST'])
def edit(reference_id):
    """Edit items"""
    form = EditForm(csrf_enabled=False)

    return CrudAction().edit(view, form, keys, 'company_name', reference_id)
