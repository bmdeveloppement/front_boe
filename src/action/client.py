# -*- coding: utf-8 *-*
from flask import Blueprint, render_template
from lib.back_utils import BackUtils

view = 'client'
client_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'company_name', 'email_address']
translations = ['#', 'Company Name', 'Email Address']

@client_bp.route('/<int:reference_id>')
def get(reference_id):
    """Get full item"""
    item = BackUtils().get_full(view, reference_id)
    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)

@client_bp.route('/')
def list():
    """List items"""
    items = BackUtils().list(view)
    return render_template('crud/list.html', view=view, items=items,
                           keys=keys, translations=translations)

@client_bp.route('/add')
def add():
    """Add an item"""
    return 'add'

@client_bp.route('/edit')
def edit():
    """Edit items"""
    item = BackUtils().get('client', reference_id)
    return render_template('crud/edit.html', item=item)
