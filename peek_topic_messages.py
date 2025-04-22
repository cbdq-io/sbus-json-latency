#!/usr/bin/env python
"""
Peek messages on an Azure Service Bus namespace.

Given a connection string this is a basic connectivity test.
"""
import argparse
import logging
import sys

from azure.servicebus import ServiceBusClient

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-d', '--debug',
    help='Set logging to debug level.',
    action='store_true'
)
group.add_argument(
    '-v', '--verbose',
    help='Set logging to info level.',
    action='store_true'
)
parser.add_argument(
    '-c', '--connection-string',
    help='The connection string for the Azure Service Bus namespace.',
    required=True
)
parser.add_argument(
    '-t', '--topic',
    help='The topic to peek messages on.',
    required=True
)
parser.add_argument(
    '-s', '--subscription',
    help='The subscription for the topic to peek messages on.',
    required=True
)

args = parser.parse_args()
logging.basicConfig()
logger = logging.getLogger(parser.prog)

if args.debug:
    logger.setLevel(logging.DEBUG)
elif args.verbose:
    logger.setLevel(logging.INFO)

logger.debug(f'Log level is {logging.getLevelName(logger.getEffectiveLevel())}')
topic = args.topic
subscription = args.subscription
logger.info(f'Peek messages on {topic}/{subscription}.')
status = 0

try:
    with ServiceBusClient.from_connection_string(args.connection_string) as client:
        with client.get_subscription_receiver(topic, subscription) as receiver:
            messages = receiver.peek_messages(max_message_count=1)

            if messages:
                logger.info('Connection successful: Message peeked from topic.')
            else:
                logger.info('Connection successful: No messages')
except Exception as e:
    logger.error(f'Connection failed: {e}')
    status = 1

sys.exit(status)
