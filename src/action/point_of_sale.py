# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils
from form.point_of_sale import AddForm, EditForm
from action.crud import CrudAction

view = 'point-of-sale'
point_of_sale_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'delivery_price', 'address', 'zip_code', 'city',
        'additional_data']
translations = ['#', 'Delivery Price', 'Address', 'Zip Code', 'City',
                'Additional Data']
key_name = 'address'


@point_of_sale_bp.route('/<int:reference_id>')
def get(reference_id):
    """Get full item"""
    item = BackUtils().get_full('point_of_sale', reference_id)

    # Update keys to show client details
    keys = ['id', 'client', 'delivery_price', 'address', 'zip_code', 'city',
            'additional_data']
    translations = ['#', 'Client', 'Delivery Price', 'Address', 'Zip Code',
                    'City', 'Additional Data']

    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)


@point_of_sale_bp.route('/', methods=['GET'])
@point_of_sale_bp.route('/page/<int:page>', methods=['GET'])
@point_of_sale_bp.route('/page/<int:page>/order_by/<string:order_by>/sort/<string:sort>', methods=['GET'])
def list(page=1, order_by='address', sort='asc'):
    """List items"""
    return CrudAction().list(view, keys, translations, page, order_by, sort)


@point_of_sale_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add an item"""
    form = AddForm(csrf_enabled=False)

    # Get list
    clients = BackUtils().list_field('client', 'company_name')
    form.client_id.choices = clients

    # Update keys to send id to Back
    keys = ['client_id', 'delivery_price', 'address', 'zip_code', 'city',
            'additional_data']

    return CrudAction().add(view, form, keys, key_name)


@point_of_sale_bp.route('/edit/<int:reference_id>', methods=['GET', 'POST'])
def edit(reference_id):
    """Edit an item"""
    form = AddForm(csrf_enabled=False)

    # Get list
    clients = BackUtils().list_field('client', 'company_name')
    form.client_id.choices = clients

    # Update keys to send id to Back
    keys = ['client_id', 'delivery_price', 'address', 'zip_code', 'city',
            'additional_data']

    return CrudAction().edit(view, form, keys, key_name, reference_id)


@point_of_sale_bp.route('/delete/<int:reference_id>', methods=['GET'])
@point_of_sale_bp.route('/delete/<int:reference_id>/confirmed/<int:confirmed>', methods=['GET'])
def delete(reference_id, confirmed=False):
    """Delete items"""
    return CrudAction().delete(view, key_name, reference_id, confirmed)
