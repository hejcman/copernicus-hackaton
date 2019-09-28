#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Sends message to facebook messenger. Called from app.py."""

from builtins import range
from fbchat import Client
from fbchat.models import ThreadType

import time


def message_sender(user_login, user_password,
                   receiver_uid, number_of_messages,
                   time_interval_between_messages, message):
    """Message sender for Facebook Messenger."""
    client = Client(user_login, user_password)
    for counter in range(0, number_of_messages):
        time.sleep(time_interval_between_messages)
        client.sendMessage(
            message,
            thread_id=receiver_uid,
            thread_type=ThreadType.USER
        )
