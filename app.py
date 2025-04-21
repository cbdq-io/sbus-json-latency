"""Report the latency between a JSON embedded ISO 8601 timestamp and an Azure Service Bus message enqueued time."""
import datetime
import json
import logging
import math
import os

import jmespath
from azure.servicebus import ServiceBusClient, ServiceBusMessage

logging.basicConfig()
logger = logging.getLogger('sbus-json-latency')
logger.setLevel(logging.INFO)
conn_str = os.environ['LATENCY_TEST_CONNECTION_STRING']
expression = os.environ['LATENCY_TEST_TIMESTAMP_JMESPATH']
subscription_name = os.environ['LATENCY_TEST_SUBSCRIPTION']
topic_name = os.environ['LATENCY_TEST_TOPIC']
last_info_message = datetime.datetime.now(datetime.UTC)
latencies = []


def get_latency_ms(message: ServiceBusMessage) -> int:
    """
    Get the latency of a message.

    Parameters
    ----------
    message : ServiceBusMessage
        The message to calculate the latency of.

    Returns
    -------
    int
        The difference between the enqueued time and the timestamp in the
        message content (in milliseconds).  Returns
    """
    try:
        enqueued_time = message.enqueued_time_utc
        body_bytes = b''.join(message.body)
        body = body_bytes.decode()
        data = json.loads(body)
        timestamp = jmespath.search(expression, data)

        if not timestamp:
            logger.warning(f'No timestamp found in decoded JSON message ({expression}).')
            return math.nan

        timestamp = datetime.datetime.fromisoformat(timestamp)
        delta = enqueued_time - timestamp
        return int(delta.microseconds / 1000)
    except Exception as e:
        logger.warning(e)
        return math.nan


def give_update(latencies: list[int]) -> None:
    """
    Report the average latencies.

    Parameters
    ----------
    latencies : list[int]
        A list of all the latency readings.
    """
    average = int(sum(latencies) / len(latencies)) if latencies else 0
    logger.info(f'messageCount {len(latencies)} averageLatencyMilliSeconds {average}')


with ServiceBusClient.from_connection_string(conn_str) as client:
    with client.get_subscription_receiver(topic_name, subscription_name) as receiver:
        while True:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)

            for message in messages:
                latency = get_latency_ms(message)
                receiver.complete_message(message)

                if latency is not math.nan:
                    latencies.append(latency)

            now = datetime.datetime.now(datetime.UTC)
            delta = now - last_info_message

            if delta.total_seconds() >= 60:
                give_update(latencies)
                latencies = []
                last_info_message = now
