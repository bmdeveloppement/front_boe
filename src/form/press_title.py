# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, FloatField, validators


class MainForm(Form):
    """Main form"""
    supplier_id = SelectField(
        u'Supplier',
        validators=[validators.Required("This field is required.")],
        coerce=int)
    name = TextField(
        u'Name',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : Le Monde"})
    supplier_cost = FloatField(
        u'Supplier Cost',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : 0.57 €"})
    royalty_cost = FloatField(
        u'Royalty Cost',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : 0.15 € - Cost per copy"})
    paging = FloatField(
        u'Paging',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : 30"})


class AddForm(MainForm):
    """Inherit of MainForm"""


class EditForm(MainForm):
    """Inherit of MainForm"""
