# -*- coding: utf-8 *-*
from flask import Blueprint, render_template
from lib.back_utils import BackUtils

view = 'point-of-sale'
point_of_sale_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'delivery_price', 'address', 'zip_code', 'city', 'additional_data']
translations = ['#', 'Delivery Price', 'Address', 'Zip Code', 'City', 'Additional Data']

@point_of_sale_bp.route('/<int:reference_id>')
def get(reference_id):
    """Get full item"""
    item = BackUtils().get_full('point_of_sale', reference_id)
    keys = ['id', 'client', 'delivery_price', 'address', 'zip_code', 'city', 'additional_data']
    translations = ['#', 'Client', 'Delivery Price', 'Address', 'Zip Code', 'City', 'Additional Data']
    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)

@point_of_sale_bp.route('/')
def list():
    """List items"""
    items = BackUtils().list('point_of_sale')
    return render_template('crud/list.html', view=view, items=items,
                           keys=keys, translations=translations)
