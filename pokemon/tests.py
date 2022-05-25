from django.test import TestCase


class TestInitialDataMigration(TestCase):
    # Test migrations work correctly.
    # As migrations run before the test suite, some mocking willl be required
    # or perhaps the use of https://github.com/wemake-services/django-test-migrations
    # or similar
    pass


class TestPokemonAPI(TestCase):

    # Tests to ensure we're handling the data from the Pokemon API correctly
    # Mocking will be required here
    # PACT testing may be a good idea if it happens to be available
    pass


class TestOutputAPI(TestCase):
    # Tests to make sure we're presenting the right thing.
    # There's no real logic being added, so we'd essentially be re-testing
    # the rest_framework. Probably doesn't require a huge amount of unit testing
    # provided we're happy with the framework.
    pass
