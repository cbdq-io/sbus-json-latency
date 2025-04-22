#!/usr/bin/env python
"""Generate data for testing against."""
import datetime
import json
import logging
import os

from azure.servicebus import (ServiceBusClient, ServiceBusMessage,
                              ServiceBusSender)

PROG = os.path.basename(__file__)
logging.basicConfig()
logger = logging.getLogger(PROG)
logger.setLevel(logging.DEBUG)


def generate_data(sender: ServiceBusSender) -> None:
    """
    Generate data to be sent as service bus messages.

    Parameters
    ----------
    sender : ServiceBusSender
        The sender for loading messages into Service Bus.
    """
    messages = []
    timestamp = datetime \
        .datetime \
        .now(datetime.UTC) \
        .isoformat() \
        .removesuffix('+00:00') \
        + 'Z'

    payload = {
        'timestamp': timestamp
    }
    message = ServiceBusMessage(body=json.dumps(payload))
    logger.debug(message)
    messages.append(message)
    messages.append(ServiceBusMessage(body='Not JSON.'))
    sender.send_messages(messages)


params_file = __file__
params_file = os.path.dirname(params_file) + os.path.sep + 'test.env'
logger.debug(f'Opening parameters file is "{params_file}"...')

with open(params_file) as stream:
    lines = stream.readlines()

params = {}

for line in lines:
    line = line.strip().replace('"', '')
    items = line.split('=')
    key = items[0]
    value = '='.join(items[1:])
    params[key] = value

connection_string = params['LATENCY_TEST_CONNECTION_STRING']\
    .replace('emulator', 'localhost')
topic_name = params['LATENCY_TEST_TOPIC']

with ServiceBusClient.from_connection_string(connection_string) as client:
    with client.get_topic_sender(topic_name) as sender:
        generate_data(sender)
