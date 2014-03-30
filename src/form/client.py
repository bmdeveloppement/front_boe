# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, validators


class MainForm(Form):
    """Main form"""
    company_name = TextField(
        u'Company Name',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : My Company"})
    email_address = TextField(
        u'Email Address',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : name@mycompany.com"})


class AddForm(MainForm):
    """Inherit of MainForm"""


class EditForm(MainForm):
    """Inherit of MainForm"""
