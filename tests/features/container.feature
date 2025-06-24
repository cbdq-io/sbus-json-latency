Feature: Container
    In order to validate the container
    As a container maintainer
    I want verify the container

    Scenario Outline: Files
        Given the TestInfra host with URL "docker://sbus-json-latency" is ready within 10 seconds
        When the TestInfra file is <file_name>
        Then the TestInfra file is <file_state>
        And the TestInfra file type is <file_type>
        And the TestInfra file mode is <file_mode>

        Examples:
            | file_name                 | file_state | file_type | file_mode |
            | /usr/local/bin/app.py     | present    | file      | 0o755     |
            | /var/tmp/requirements.txt | present    | file      | 0o644     |

    Scenario Outline: Python Modules
        Given the TestInfra host with URL "docker://sbus-json-latency" is ready
        When the TestInfra pip package is <pip_package>
        Then the TestInfra pip package is present
        And the TestInfra pip check is OK

        Examples:
            | pip_package      |
            | azure-servicebus |
            | jmespath         |

    Scenario: Commands on Path
        Given the TestInfra host with URL "docker://sbus-json-latency" is ready
        Then the TestInfra command <command_expected_on_path> exists in path

        Examples:
            | command_expected_on_path |
            | nslookup                 |
