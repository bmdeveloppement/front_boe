# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, FloatField, validators


class MainForm(Form):
    """Main form"""
    deliverer_id = SelectField(
        u'Deliverer',
        validators=[validators.Required("This field is required.")],
        coerce=int)
    name = TextField(
        u'Name',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : Turn Barbes to Eiffel Tower"})
    cost = FloatField(
        u'Cost',
        description={'placeholder': u"Ex : 14 €"})
    unitary_cost = FloatField(
        u'Unitary Cost',
        description={'placeholder': u"Ex : 0.35 € - Cost per delivery"})
    schedule = TextField(
        u'Schedule',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : {'monday': '9', 'tuesday': '8'}"})


class AddForm(MainForm):
    """Inherit of MainForm"""


class EditForm(MainForm):
    """Inherit of MainForm"""
