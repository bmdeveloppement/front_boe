# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template
from lib.back_utils import BackUtils
from form.point_of_sale import AddForm, EditForm

view = 'point-of-sale'
point_of_sale_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'delivery_price', 'address', 'zip_code', 'city', 'additional_data']
translations = ['#', 'Delivery Price', 'Address', 'Zip Code', 'City', 'Additional Data']

@point_of_sale_bp.route('/<int:reference_id>')
def get(reference_id):
    """Get full item"""
    item = BackUtils().get_full('point_of_sale', reference_id)

    # Update keys to show client details
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

@point_of_sale_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add an item"""
    form = AddForm(csrf_enabled=False)

    # Get client list
    clients = BackUtils().list_field('client', 'company_name')
    form.client_id.choices = clients
    
    # Update keys to send client_id to Core
    keys = ['client_id', 'delivery_price', 'address', 'zip_code', 'city', 'additional_data']

    # Submit
    if form.validate_on_submit():
        data = {}
        for key in keys:
            if key is not 'id':
                data[key] = getattr(form, key).data
        item = BackUtils().add(view, data)
        return redirect(url_for('%s.list' % view))
    return render_template('%s/add.html' % view, view=view, form=form)
