# -*- coding: utf-8 *-*
from flask import redirect, url_for, Blueprint, render_template
from lib.back_utils import BackUtils
from form.client import AddForm, EditForm

view = 'client'
client_bp = Blueprint(view, __name__, url_prefix='/%s' % view)
keys = ['id', 'company_name', 'email_address']
translations = ['#', 'Company Name', 'Email Address']

@client_bp.route('/<int:reference_id>', methods=['GET'])
def get(reference_id):
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
    if form.validate_on_submit():
        data = {}
        for key in keys:
            if key is not 'id':
                data[key] = getattr(form, key).data
        item = BackUtils().add(view, data)
        return redirect(url_for('%s.list' % view))
    return render_template('%s/add.html' % view, view=view, form=form)

@client_bp.route('/edit')
def edit():
    """Edit items"""
    item = BackUtils().get('client', reference_id)
    return render_template('crud/edit.html', item=item)
