#!/usr/bin/env python3
"""
fetch_guidelines.py

Build a guideline catalogue from a ClinPGx gene-search response.

Workflow
--------
1. Receive a ClinPGx JSON response object.
2. Iterate through every accession in the response.
3. Extract all related GuidelineAnnotation IDs.
4. Retrieve each GuidelineAnnotation from ClinPGx.
5. Extract:
    - summaryMarkdown
    - textMarkdown
    - hyperlinks contained in the HTML
6. Group guidelines under their originating accession.
7. Return a JSON-serialisable dictionary.

"""

import requests
from functools import lru_cache
from bs4 import BeautifulSoup

BASE_URL = "https://api.clinpgx.org/v1"

@lru_cache()
def extract_links(html):
    """
    Extract hyperlinks from HTML.

    Parameters
    ----------
    html : str

    Returns
    -------
    list[dict]

    Example
    -------
    [
        {
            "text": "2022 supplement",
            "url": "https://..."
        }
    ]
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = []

    for link in soup.find_all(
        "a",
        href=True
    ):

        links.append(
            {
                "text": link.get_text(
                    strip=True
                ),
                "url": link["href"],
            }
        )

    return links

@lru_cache()
def get_guideline(
    guideline_id,
):
    """
    Retrieve a ClinPGx GuidelineAnnotation.

    Parameters
    ----------
    guideline_id : str

    Returns
    -------
    dict
        GuidelineAnnotation JSON.
    """

    response = requests.get(
        f"{BASE_URL}/data/guidelineAnnotation/{guideline_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["data"]

def build_guideline_catalog(
    clinpgx_response,
):
    """
    Build a guideline catalogue grouped
    by accession.

    Parameters
    ----------
    clinpgx_response : dict
        JSON response supplied by the
        ClinPGx gene/allele search function.

    Returns
    -------
    dict
        JSON-serialisable structure
        grouped by accession.
    """

    results = {
        "accessions": []
    }

    for record in clinpgx_response.get(
        "data",
        []
    ):

        accession_id = record.get(
            "accessionId"
        )

        accession_result = {
            "accessionId": accession_id,
            "guidelines": [],
        }

        for guideline_ref in record.get(
            "relatedGuidelines",
            []
        ):

            guideline_id = (
                guideline_ref["id"]
            )

            guideline_name = (
                guideline_ref["name"]
            )

            print(
                f"Fetching "
                f"{guideline_id}"
            )

            try:

                guideline = (
                    get_guideline(
                        guideline_id
                    )
                )

                summary = guideline.get(
                    "summaryMarkdown",
                    {},
                )

                text = guideline.get(
                    "textMarkdown",
                    {},
                )

                summary_html = (
                    summary.get(
                        "html",
                        ""
                    )
                )

                text_html = (
                    text.get(
                        "html",
                        ""
                    )
                )

                links = (
                    extract_links(
                        summary_html
                    )
                    +
                    extract_links(
                        text_html
                    )
                )

                accession_result[
                    "guidelines"
                ].append(
                    {
                        "id":
                            guideline_id,

                        "name":
                            guideline_name,

                        "summaryMarkdown":
                            summary,

                        "textMarkdown":
                            text,

                        "links":
                            links,
                    }
                )

            except Exception as exc:

                accession_result[
                    "guidelines"
                ].append(
                    {
                        "id":
                            guideline_id,

                        "name":
                            guideline_name,

                        "error":
                            str(exc),
                    }
                )

        results[
            "accessions"
        ].append(
            accession_result
        )

    return results
