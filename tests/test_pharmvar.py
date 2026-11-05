import pytest
import os
from unittest.mock import Mock, patch

# Provide a test API key before importing the module
os.environ["PHARMVAR_API_KEY"] = "test_api_key"

from star_allele_search.module.pharmvar_json import (
    get_pharmvar_json,
    filter_pharmvar_json,
    HEADERS,
    PARAMS,
)

###############################################################################
#                           AI use declaration                                #
# Copilot model GPT-5.6 was used to develop some of the test functions below. #
###############################################################################


@patch("star_allele_search.module.pharmvar_json.requests.get")
def test_get_pharmvar_json(mock_get):
    """
    Test that get_pharmvar_json returns the JSON data
    provided by the API response.
    """

    get_pharmvar_json.cache_clear()

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
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_pharmvar_json("CYP2C19*2")

    assert result == expected_json


@patch("star_allele_search.module.pharmvar_json.requests.get")
def test_get_pharmvar_json_uses_correct_url(mock_get):
    """
    Test that the correct PharmVar URL is constructed.
    """

    get_pharmvar_json.cache_clear()

    expected_json = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
        }
    ]

    mock_response = Mock()
    mock_response.json.return_value = expected_json
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    get_pharmvar_json("CYP2C19*2")

    mock_get.assert_called_once()

    args, kwargs = mock_get.call_args

    assert (
        args[0]
        == "https://www.pharmvar.org/api-service/alleles/CYP2C19*2"
    )


@patch("star_allele_search.module.pharmvar_json.requests.get")
def test_get_pharmvar_json_called_with_correct_parameters(
    mock_get,
):
    """
    Test that the correct URL, headers, params and timeout
    are sent to requests.get().
    """

    get_pharmvar_json.cache_clear()

    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    get_pharmvar_json("CYP2C19*2")

    mock_get.assert_called_once_with(
        "https://www.pharmvar.org/api-service/alleles/CYP2C19*2",
        headers=HEADERS,
        params=PARAMS,
        timeout=30,
    )


def test_filter_pharmvar_json():
    """
    Test that extra fields are removed and only
    required fields are kept.
    """

    input_json = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
            "references": ["PMID12345"],
            "variants": [{"hgvs": "c.681G>A"}],
            "extraField": "remove me",
        }
    ]

    expected = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": "CYP2C19*2",
            "references": ["PMID12345"],
            "variants": [{"hgvs": "c.681G>A"}],
        }
    ]

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

    input_json = [
        {
            "geneSymbol": "CYP2C19",
        }
    ]

    expected = [
        {
            "geneSymbol": "CYP2C19",
            "alleleName": None,
            "references": None,
            "variants": None,
        }
    ]

    assert filter_pharmvar_json(input_json) == expected

@pytest.mark.integration
def test_get_pharmvar_json_integration():
    """
    Integration test against the real PharmVar API.
    """

    get_pharmvar_json.cache_clear()

    result = get_pharmvar_json("CYP2C19*2")

    assert isinstance(result, list)
    assert len(result) > 0

    assert result[0]["geneSymbol"] == "CYP2C19"
    assert result[0]["alleleName"] == "CYP2C19*2"