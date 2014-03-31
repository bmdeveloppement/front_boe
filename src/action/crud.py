# -*- coding: utf-8 -*-
import logging
from flask import redirect, url_for, Blueprint, render_template, flash
from lib.back_utils import BackUtils

logger = logging.getLogger(__name__)


class CrudAction(object):

    def add(self, view, form, keys, key_name):
        """Add item"""
        # Submit
        if form.validate_on_submit():

            # Populate keys
            data = {}
            for key in keys:
                if key is not 'id':
                    data[key] = getattr(form, key).data
                    if data[key] is True:
                        data[key] = 1
                    elif data[key] is False:
                        data[key] = 0
            item = BackUtils().add(view, data)

            # Flash message
            item_name = getattr(form, key_name).data
            if type(item) == int:
                flash(u"Creation of %s %s successful !" %
                      (view.replace('-', ' '), item_name), 'success')
            else:
                flash(u"Creation of %s %s failed" %
                      (view.replace('-', ' '), item_name), 'warning')

            # Redirect to list
            return redirect(url_for('%s.list' % view))

        # Render form
        return render_template('%s/add-or-edit.html' % view, view=view,
                               form=form, action='add')

    def edit(self, view, form, keys, key_name, reference_id):
        """Edit items"""
        # Get the reference item
        item = BackUtils().get(view, reference_id)

        if form.validate_on_submit():

            # Populate keys
            data = {}
            for key in keys:
                if key is not 'id':
                    data[key] = getattr(form, key).data
                    if data[key] is True:
                        data[key] = 1
                    elif data[key] is False:
                        data[key] = 0
            item = BackUtils().edit(view, reference_id, data)

            # Flash message
            item_name = getattr(form, key_name).data
            if type(item) == int:
                flash(u"Edition of %s %s successful !" %
                      (view.replace('-', ' '), item_name), 'success')
            else:
                flash(u"Edition of %s %s failed" %
                      (view.replace('-', ' '), item_name), 'warning')

            # Redirect to list
            return redirect(url_for('%s.list' % view))
        else:
            # Build and populate form
            for key in keys:
                if key is not 'id':
                    getattr(form, key).data = item.get(key, None)

        # Render form
        return render_template('%s/add-or-edit.html' % view, view=view,
                               form=form, action='edit')
