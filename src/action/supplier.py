# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils
from form.supplier import AddForm, EditForm
from action.crud import CrudAction

view = 'supplier'
supplier_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'company_name', 'email_address', 'report', 'reporting_hour']
translations = ['#', 'Company Name', 'Email Address', 'Report', 'Reporting hour']


@supplier_bp.route('/<int:reference_id>', methods=['GET'])
def get(reference_id, methods=['GET']):
    """Get full item"""
    item = BackUtils().get_full(view, reference_id)
    return render_template('crud/view.html', view=view, item=item,
                           keys=keys, translations=translations)


@supplier_bp.route('/', methods=['GET'])
@supplier_bp.route('/page/<int:page>', methods=['GET'])
@supplier_bp.route('/page/<int:page>/order_by/<string:order_by>/sort/<string:sort>', methods=['GET'])
def list(page=1, order_by='company_name', sort='asc'):
    """List items"""
    return CrudAction().list(view, keys, translations, page, order_by, sort)


@supplier_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add an item"""
    form = AddForm(csrf_enabled=False)
    return CrudAction().add(view, form, keys, 'company_name')


@supplier_bp.route('/edit/<int:reference_id>', methods=['GET', 'POST'])
def edit(reference_id):
    """Edit items"""
    form = EditForm(csrf_enabled=False)
    return CrudAction().edit(view, form, keys, 'company_name', reference_id)
