# Example of tests

class TestCatchThemAllManagementCommand(object):
    def test_get_with_next_url(self):
        """
        Mock the API request which returns `next` page and make
        sure `get_pokemon_details` and `update_or_create_pokemon` are called
        with right params.
        """
        pass

    def test_get_without_next_url(self):
        """
        Mock the API request which returns `next` as None and make
        sure `get_pokemon_details` and `update_or_create_pokemon` are called
        with right params.
        """
        pass

    # We could also have an integration tests which test the command end to end run,
    # e.g. based on the mocked API responses, make sure that all pokemons are created
    # and updated


def test_update_or_create_pokemon_details_new_pokemon():
    """
    Test update_or_create_pokemon() function
    """


def test_update_or_create_pokemon_details_existing_pokemon():
    """
    Test update_or_create_pokemon() function
    """


def test_get_pokemon_details():
    """
    Test get_pokemon_details() function with mocked API response
    """


def test_get_pokemon_error():
    """
    Test get_pokemon_details() and various error scenarious, e.g. non 200 API
    responses etc.
    """

# Same as above for get_pokemon_description() function.
