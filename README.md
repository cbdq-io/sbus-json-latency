# sbus-json-latency
Report the latency between a JSON embedded ISO 8601 timestamp and an Azure Service Bus message enqueued time.

## Environment Variables

- `LATENCY_TEST_CONNECTION_STRING` (required): The connection string to the
  Azure Service Bus Namespace.
- `LATENCY_TEST_SUBSCRIPTION` (required):  The name of the subscription on
  the topic to receive messages from.
- `LATENCY_TEST_TIMESTAMP_JMESPATH` (required): The
  [JMESPath](https://jmespath.org/) expression to extract the timestamp from
  the [JSON](https://en.wikipedia.org/wiki/JSON) decoded message.
- `LATENCY_TEST_TOPIC` (required): The name of the topic to recieve messages
  from.

## Reporting

If messages are being sent to Azure Log Analytics, the following Kusto
Query Language (KQL) to graph the latency would be:

```
SbusJsonLatency_CL
| where Level == "INFO"
| where Message has "averageLatencyMilliSeconds"
| parse Message with "messageCount " messageCount:int " averageLatencyMilliSeconds " avgLatency:int
| where messageCount > 0
| project TimeGenerated, messageCount, avgLatency
| render timechart avg(avgLatency)
```
