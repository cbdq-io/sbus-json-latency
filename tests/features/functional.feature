Feature: Functional Tests
    In order to verify the functionality
    As a maintainer
    I want functionality tests to run against the artefact

    Scenario Outline: Input Test Data
        Given the TestInfra host with URL "local://" is ready
        When the TestInfra command is "./tests/resources/data_gen.py"
        Then the TestInfra command return code is 0

        Examples:
            | command                       |
            | ./tests/resources/data_gen.py |
            | ./tests/resources/data_gen.py |

    Scenario: Check Container Logs
        Given a host with URL "local://" after an initial sleep
        When the TestInfra command is "docker compose logs sbus-json-latency"
        Then the TestInfra command return code is 0
        And the TestInfra command stdout contains "WARNING:sbus-json-latency:Expecting value: line 1 column 1 (char 0)"
        And the TestInfra command stdout contains the regex "INFO:sbus-json-latency:messageCount .* averageLatencyMilliSeconds .* maxLatencyMilliSeconds .* minLatencyMilliSeconds .*"
