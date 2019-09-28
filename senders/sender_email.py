#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Sends an email. Called from app.py."""

from builtins import range
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time


def email_sender(user_email, password_email, smtp_server,
                 smtp_port, recipient_email, number_of_emails,
                 time_interval_between_emails, email_subject, email_body):
    """
    Send the email.

    Source: http://naelshiab.com/tutorial-send-email-python/
    Currently doesn't support attachments.
    """
    msg = MIMEMultipart()

    msg['From'] = user_email
    msg['To'] = recipient_email
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_body, 'plain'))

    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    # server.starttls()
    server.login(user_email, password_email)
    text = msg.as_string()
    for counter in range(0, number_of_emails):
        server.sendmail(user_email, recipient_email, text)
        time.sleep(time_interval_between_emails)
    server.quit()
