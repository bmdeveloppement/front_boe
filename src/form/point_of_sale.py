# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, FloatField, validators


class MainForm(Form):
    """Main form"""
    client_id = SelectField(
        u'Client',
        validators=[validators.Required("This field is required.")],
        coerce=int)
    delivery_price = FloatField(
        u'Delivery Price',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : 0.57 €"})
    address = TextField(
        u'Address',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : 3 rue Voltaire"})
    zip_code = TextField(
        u'Zip Code',
        validators=[validators.Required(u"This field is required"),
                    validators.NumberRange(min=0, max=None,
                                           message="Must be a number")],
        description={'placeholder': u"Ex : 75010"})
    city = TextField(
        u'City',
        validators=[validators.Required(u"This field is required")],
        description={'placeholder': u"Ex : Paris, London, New York ..."})
    additional_data = TextField(
        u'Additional Data',
        description={'placeholder': u""})


class AddForm(MainForm):
    """Inherit of MainForm"""


class EditForm(MainForm):
    """Inherit of MainForm"""
