"""Use TestInfraBDD to test the container produced."""
import time

import testinfra_bdd
from pytest_bdd import given, scenarios
from testinfra_bdd import TestinfraBDD

scenarios('../features/container.feature')
scenarios('../features/functional.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES


@given('a host with URL "local://" after an initial sleep', target_fixture='testinfra_bdd_host')
def _():
    """a host with URL "local://" after an initial sleep."""
    host = TestinfraBDD('local://')
    time.sleep(60)
    assert host.is_host_ready()
    return host
