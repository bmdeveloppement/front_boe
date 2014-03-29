# -*- coding: utf-8 *-*
from flask import Blueprint, render_template
from lib.back_utils import BackUtils

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/get_full/<int:reference_id>')
def get_full(reference_id):
    """Get full item"""
    item = BackUtils().get_full('client', reference_id)
    return render_template('crud/view.html', item=item)

@client_bp.route('/')
def list():
    """List items"""
    items = BackUtils().list('client')
    return render_template('crud/list.html', items=items)

@client_bp.route('/add')
def add():
    """Add an item"""
    return 'add'

@client_bp.route('/edit')
def edit():
    """Edit items"""
    item = BackUtils().get('client', reference_id)
    return render_template('crud/edit.html', item=item)
