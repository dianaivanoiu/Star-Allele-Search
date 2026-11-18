from unittest.mock import Mock, patch

from star_allele_search.module.fetch_guidelines import (
    extract_links,
    get_guideline,
    build_guideline_catalog,
)


###############################################################################
#                           AI use declaration                                #
# Copilot powered by GPT-5 was used to draft portions of these tests.         #
###############################################################################


def test_extract_links():
    """
    Test extraction of hyperlinks from HTML.
    """

    html = """
    <p>
        <a href="https://example.com/a">Link A</a>
        <a href="https://example.com/b">Link B</a>
    </p>
    """

    expected = [
        {
            "text": "Link A",
            "url": "https://example.com/a",
        },
        {
            "text": "Link B",
            "url": "https://example.com/b",
        },
    ]

    assert extract_links(html) == expected


def test_extract_links_empty_html():
    """
    Test empty HTML returns no links.
    """

    assert extract_links("") == []


@patch(
    "star_allele_search.module.fetch_guidelines.requests.get"
)
def test_get_guideline(mock_get):
    """
    Test retrieval of a GuidelineAnnotation object.
    """
    get_guideline.cache_clear()
    expected_data = {
        "id": "PA166104948",
        "name": "CPIC Guideline",
    }

    mock_response = Mock()

    mock_response.json.return_value = {
        "data": expected_data
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_guideline(
        "PA166104948"
    )

    assert result == expected_data


@patch(
    "star_allele_search.module.fetch_guidelines.requests.get"
)
def test_get_guideline_uses_correct_url(
    mock_get
):
    """
    Test correct ClinPGx URL is queried.
    """
    get_guideline.cache_clear()
    mock_response = Mock()

    mock_response.json.return_value = {
        "data": {}
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    get_guideline(
        "PA166104948"
    )

    mock_get.assert_called_once_with(
        (
            "https://api.clinpgx.org/v1/"
            "data/guidelineAnnotation/"
            "PA166104948"
        ),
        timeout=30,
    )


@patch(
    "star_allele_search.module.fetch_guidelines.get_guideline"
)
def test_build_guideline_catalog(
    mock_get_guideline
):
    """
    Test guideline catalogue creation.
    """

    mock_get_guideline.return_value = {
        "summaryMarkdown": {
            "html": (
                '<a href="https://example.com">'
                'Guideline PDF'
                "</a>"
            )
        },
        "textMarkdown": {
            "html": ""
        },
    }

    clinpgx_response = {
        "data": [
            {
                "accessionId":
                    "PA166225621",

                "relatedGuidelines": [
                    {
                        "id":
                            "PA166104948",

                        "name":
                            "CPIC Guideline"
                    }
                ]
            }
        ]
    }

    result = build_guideline_catalog(
        clinpgx_response
    )

    accession = result[
        "accessions"
    ][0]

    guideline = accession[
        "guidelines"
    ][0]

    assert accession[
        "accessionId"
    ] == "PA166225621"

    assert guideline[
        "id"
    ] == "PA166104948"

    assert guideline[
        "name"
    ] == "CPIC Guideline"

    assert guideline[
        "links"
    ] == [
        {
            "text": "Guideline PDF",
            "url": "https://example.com",
        }
    ]


@patch(
    "star_allele_search.module.fetch_guidelines.get_guideline"
)
def test_build_guideline_catalog_multiple_accessions(
    mock_get_guideline
):
    """
    Test multiple accessions are grouped
    correctly.
    """
    get_guideline.cache_clear()

    mock_get_guideline.return_value = {
        "summaryMarkdown": {
            "html": ""
        },
        "textMarkdown": {
            "html": ""
        },
    }

    clinpgx_response = {
        "data": [
            {
                "accessionId": "PA1",

                "relatedGuidelines": [
                    {
                        "id": "G1",
                        "name": "Guideline 1",
                    }
                ]
            },
            {
                "accessionId": "PA2",

                "relatedGuidelines": [
                    {
                        "id": "G2",
                        "name": "Guideline 2",
                    }
                ]
            },
        ]
    }

    result = build_guideline_catalog(
        clinpgx_response
    )

    assert (
        len(
            result["accessions"]
        )
        == 2
    )

    assert (
        result["accessions"][0]
        ["accessionId"]
        == "PA1"
    )

    assert (
        result["accessions"][1]
        ["accessionId"]
        == "PA2"
    )


@patch(
    "star_allele_search.module.fetch_guidelines.get_guideline"
)
def test_build_guideline_catalog_no_guidelines(
    mock_get_guideline
):
    """
    Test accessions with no guidelines.
    """
    get_guideline.cache_clear()
    clinpgx_response = {
        "data": [
            {
                "accessionId":
                    "PA166280001",

                "relatedGuidelines": []
            }
        ]
    }

    result = build_guideline_catalog(
        clinpgx_response
    )

    assert (
        result["accessions"][0]
        ["guidelines"]
        == []
    )

    mock_get_guideline.assert_not_called()


@patch(
    "star_allele_search.module.fetch_guidelines.get_guideline"
)
def test_build_guideline_catalog_error_handling(
    mock_get_guideline
):
    """
    Test guideline retrieval failures
    are captured.
    """
    get_guideline.cache_clear()
    mock_get_guideline.side_effect = (
        Exception("API failure")
    )

    clinpgx_response = {
        "data": [
            {
                "accessionId":
                    "PA1",

                "relatedGuidelines": [
                    {
                        "id": "G1",
                        "name": "Guideline 1",
                    }
                ]
            }
        ]
    }

    result = build_guideline_catalog(
        clinpgx_response
    )

    guideline = (
        result["accessions"][0]
        ["guidelines"][0]
    )

    assert guideline[
        "id"
    ] == "G1"

    assert guideline[
        "name"
    ] == "Guideline 1"

    assert guideline[
        "error"
    ] == "API failure"

def test_get_guideline_integration():
    """
    Integration test against the real ClinPGx API.

    Uses a known CYP2C19 guideline annotation.
    """

    result = get_guideline(
        "PA166104948"
    )

    assert isinstance(
        result,
        dict
    )

    assert (
        result["id"]
        == "PA166104948"
    )

    assert (
        "summaryMarkdown"
        in result
    )

    assert (
        "textMarkdown"
        in result
    )