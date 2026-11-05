from unittest.mock import Mock, patch  # Tools for creating fake objects and mocking functions

# Import the functions we want to test
from App.star_allele_search.module.pharmvar_json import (
    get_pharmvar_json,
    filter_pharmvar_json,
)
###############################################################################
#                           AI use declaration                                #
# Copilot  model GPT-5.6 was used to develop some of the test functions below # 
###############################################################################


# Replace requests.get() in App.pharmvar_json with a mock object
@patch("App.star_allele_search.module.pharmvar_json.requests.get")
def test_get_pharmvar_json(mock_get):
    """
    Test that get_pharmvar_json returns the JSON data
    provided by the API response.
    """

    # Fake JSON that the mocked API will return
    expected_json = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
            "references": ["PMID12345"],
            "variants": [{"hgvs": "c.681G>A"}],
        }
    ]

    mock_response = Mock()

    mock_response.json.return_value = expected_json

    # Simulate a successful HTTP request
    mock_response.raise_for_status.return_value = None

    # When requests.get() is called, return the fake data we made
    mock_get.return_value = mock_response

    result = get_pharmvar_json("CYP2C19*2")

    # Check that the returned value matches our fake API response
    assert result == expected_json


@patch("App.star_allele_search.module.pharmvar_json.requests.get")
def test_get_pharmvar_json_uses_correct_url(mock_get):
    """
    Test that the correct PharmVar URL is constructed.
    """
    expected_json = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
        }
    ]

    # Create fake response
    mock_response = Mock()

    mock_response.json.return_value = expected_json

    # Simulate successful response
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    get_pharmvar_json("CYP2C19*2")

    # Verify requests.get() was called exactly once
    mock_get.assert_called_once()

    # Extract positional and keyword arguments used in the call
    args, kwargs = mock_get.call_args

    # First positional argument should be the API URL
    assert args[0] == (
        "https://www.pharmvar.org/api-service/alleles/CYP2C19*2"
    )


@patch("App.star_allele_search.module.pharmvar_json.requests.get")
def test_get_pharmvar_json_called_with_correct_parameters(mock_get):
    """
    Test that the correct URL, headers, params and timeout
    are sent to requests.get().
    """

    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    get_pharmvar_json("CYP2C19*2")

    # Verify requests.get() was called exactly as expected
    mock_get.assert_called_once_with(
        "https://www.pharmvar.org/api-service/alleles/CYP2C19*2",
        headers={
            "accept": "application/json",
            "Api-Key": "e1779867df584c4e9bcca87bcf3a61b3",
        },
        params={
            "reference-collection": "GRCh38",
            "exclude-sub-alleles": "false",
            "include-reference-variants": "false",
            "include-retired-alleles": "false",
            "include-retired-reference-sequences": "false",
        },
        timeout=30,
    )


def test_filter_pharmvar_json():
    """
    Test that extra fields are removed and only
    required fields are kept.
    """

    # Input JSON containing extra fields
    input_json = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
            "references": ["PMID12345"],
            "variants": [{"hgvs": "c.681G>A"}],
            "extraField": "remove me",
        }
    ]

    # Expected result after filtering
    expected = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
            "references": ["PMID12345"],
            "variants": [{"hgvs": "c.681G>A"}],
        }
    ]

    # Verify filtering works correctly
    assert filter_pharmvar_json(input_json) == expected


def test_filter_pharmvar_json_empty_list():
    """
    Test that an empty input list returns
    an empty output list.
    """

    assert filter_pharmvar_json([]) == []


def test_filter_pharmvar_json_missing_fields():
    """
    Test behaviour when optional fields
    are missing from the JSON.
    """

    # Input missing alleleName, references and variants
    input_json = [
        {
            "geneSymbol": "CYP2C19",
        }
    ]

    # .get() should return None for missing keys
    expected = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": None,
            "references": None,
            "variants": None,
        }
    ]

    # Verify missing values become None
    assert filter_pharmvar_json(input_json) == expected

def test_get_pharmvar_json_integration():
    """
    Integration test against the real PharmVar API.
    """

    result = get_pharmvar_json("CYP2C19*2") #Using an actual API call to test the endpoint it ok. If it fails, manually check connection.

    assert isinstance(result, list)
    assert len(result) > 0

    assert result[0]["geneSymbol"] == "CYP2C19"
    assert result[0]["alleleName"] == "CYP2C19*2"
