#!/usr/bin/env python3
"""
Build a guideline catalogue from a ClinPGx JSON file containing
relatedGuidelines references.

For each related GuidelineAnnotation ID:
    1. Retrieve the guideline from ClinPGx.
    2. Extract summaryMarkdown.
    3. Extract textMarkdown.
    4. Extract all hyperlinks from both sections.
    5. Save everything into a single JSON file.
"""

import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://api.clinpgx.org/v1"


def collect_guideline_ids(data):
    """
    Extract all unique GuidelineAnnotation IDs from the input JSON.

    Returns
    -------
    dict
        Mapping of:
            guideline_id -> guideline_name
    """

    guideline_map = {}

    for record in data["data"]:

        for guideline in record.get(
            "relatedGuidelines",
            []
        ):

            guideline_map[
                guideline["id"]
            ] = guideline["name"]

    return guideline_map


def get_guideline(guideline_id):
    """
    Fetch a ClinPGx GuidelineAnnotation object.

    Parameters
    ----------
    guideline_id : str

    Returns
    -------
    dict
        GuidelineAnnotation record.
    """

    response = requests.get(
        f"{BASE_URL}/data/guidelineAnnotation/{guideline_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["data"]


def extract_links(html):
    """
    Extract hyperlinks from HTML.

    Parameters
    ----------
    html : str

    Returns
    -------
    list[dict]
        Example:
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


def build_guideline_catalog(
    input_file,
    output_file,
):
    """
    Build a local catalogue of guideline annotations.

    Parameters
    ----------
    input_file : str
        JSON file containing
        relatedGuidelines entries.

    output_file : str
        Output JSON filename.
    """

    with open(
        input_file,
        encoding="utf-8",
    ) as fh:

        phenotype_data = json.load(
            fh
        )

    guideline_map = (
        collect_guideline_ids(
            phenotype_data
        )
    )

    results = {
        "guidelines": []
    }

    for (
        guideline_id,
        guideline_name,
    ) in sorted(
        guideline_map.items()
    ):

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

            results[
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

            results[
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

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as fh:

        json.dump(
            results,
            fh,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved "
        f"{output_file}"
    )


if __name__ == "__main__":

    build_guideline_catalog(
        input_file="accession_1 1.json",
        output_file="guideline_catalog.json",
    )