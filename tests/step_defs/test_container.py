"""Use TestInfraBDD to test the container produced."""
import testinfra_bdd
from pytest_bdd import scenarios

scenarios('../features/container.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES
