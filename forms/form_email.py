#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Defines the Email form. Called from app.py."""

from wtforms import DecimalField
from wtforms import Form
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import validators


class EmailMessageForm(Form):
    """Sets the main style for Email form."""

    # Login details for users
    user_email = StringField('Your E-Mail',
                             [validators.Length(min=1, max=100),
                              validators.DataRequired()])
    password_email = PasswordField('E-Mail Password',
                                   [validators.Length(min=1, max=100),
                                    validators.DataRequired()])
    smtp_server = StringField('SMTP Server',
                              [validators.DataRequired()])
    smtp_port = IntegerField('SMTP Port',
                             [validators.DataRequired()])
    # Recipients email
    recipient_email = StringField('Recipient E-Mail',
                                  [validators.DataRequired()])
    # Message itself
    number_of_emails = IntegerField('Number of messages to send',
                                    [validators.DataRequired()])
    time_interval_between_emails = DecimalField('Seconds between messages',
                                                [validators.DataRequired()])
    email_subject = StringField('E-Mail Subject',
                                [validators.DataRequired()])
    email_body = TextAreaField('E-Mail Body',
                               [validators.Length(min=1, max=100)])
