# -*- coding: utf-8 *-*
from flask import Blueprint, render_template
from lib.back_utils import BackUtils

client_bp = Blueprint('client', __name__, url_prefix='/client')


@client_bp.route('/get/<int:reference_id>')
def get(reference_id):
    """Get item"""
    item = BackUtils().get('client', reference_id)
    return render_template('get.html', item=item)

@client_bp.route('/get_full/<int:reference_id>')
def get_full(reference_id):
    """Get full item"""
    item = BackUtils().get_full('client', reference_id)
    return render_template('get.html', item=item)

@client_bp.route('/list')
def list():
    """List items"""
    items = BackUtils().list('client')
    return render_template('list.html', items=items)

@client_bp.route('/add')
def add():
    """Add an item"""
    return 'add'

@client_bp.route('/edit')
def edit():
    """Edit items"""
    return 'edit'
