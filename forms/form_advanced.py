#!/usr/bin/python3
# -*- coding: utf-8 -*-

from wtforms import DecimalField
from wtforms import Form
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import validators
from wtforms import SelectField
from wtforms import DateField


class AdvancedForm(Form):

    address = StringField("What is your address?",
                          [validators.Length(min=1, max=300),
                           validators.DataRequired()])

    size = SelectField(u'What scanned area should we use for evaluation?', choices=[
                       ('small', "Small"), ('medium', "Medium"), ('large', "Large")])

    start_point = DateField("Start date for satellite data analysis (yyyy-mm-dd):", [validators.DataRequired()])
    end_point = DateField("End date for satellite data analysis (yyyy-mm-dd):", [validators.DataRequired()])

    roof_75 = StringField('Roof area with 75% efficiency:')
    roof_90 = StringField('Roof area with 90% efficiency:')
    roof_100 = StringField('Roof area with 100% efficiency:')

