#!/usr/bin/python3
# -*- coding: utf-8 -*-

from wtforms import DecimalField
from wtforms import Form
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import validators
from wtforms import SelectField


class AddressForm(Form):

    address = StringField("What is your address?",
                          [validators.Length(min=1, max=300),
                           validators.DataRequired()])

    size = SelectField(u'What scanned area should we use for evaluation?', choices=[
                       ('small', "Small"), ('medium', "Medium"), ('large', "Large")])

    yearly_spending = StringField("How much do you spend on electricity per year? (CZK)", [
        validators.Length(min=1, max=10), validators.DataRequired()])

    yearly_usage = StringField("How much electricity do you roughly use per year? (kWh)", [
        validators.Length(min=1, max=10), validators.DataRequired()])
