"""
Query and filter PharmVar allele data.
"""
import os
import json
import requests
from .vv_validation import validate_pharmvar_result
from .fetch_guidelines import build_guideline_catalog
from .clinpgx_summary_annotation import get_filtered_annotations
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://www.pharmvar.org/api-service/alleles"

HEADERS = {
    "accept": "application/json",
    "Api-Key": os.getenv(
        "PHARMVAR_API_KEY"
    ),
}

PARAMS = {
    "reference-collection": "GRCh38",
    "exclude-sub-alleles": "false",
    "include-reference-variants": "false",
    "include-retired-alleles": "false",
    "include-retired-reference-sequences": "false",
}

@lru_cache()
def get_pharmvar_json(allele):
    """
    Query PharmVar and return JSON for a star allele.

    Parameters
    ----------
    allele : str
        Star allele to query (e.g. "CYP2C19*2").

    Returns
    -------
    list
        JSON response from PharmVar.
    """
    url = f"{BASE_URL}/{allele}"

    response = requests.get(
        url,
        headers=HEADERS,
        params=PARAMS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def filter_pharmvar_json(result):
    """
    Filter PharmVar response down to required fields.

    Parameters
    ----------
    result : list
        PharmVar JSON response.

    Returns
    -------
    list
        Filtered JSON response.
    """
    return [
        {
            "geneSymbol": allele.get("geneSymbol"),
            "alleleName": allele.get("alleleName"),
            "references": allele.get("references"),
            "variants": allele.get("variants"),
        }
        for allele in result
    ]


def main():
    """Run PharmVar query and write output files."""

    allele = "CYP2C19*2"

    result = get_pharmvar_json(allele)

    validate_pharmvar_result(result) #This function validates that the gene symbol is correct and that it is the mane-select transcript.

    clinpgx_response = (get_filtered_annotations(allele))

    guideline_catalog = build_guideline_catalog(clinpgx_response)

    with open("guidelines.json", "w", encoding="utf-8") as file: #Add temporarily here in dev, Liyamu can use guideline_catalogue variable
        json.dump(
        guideline_catalog,
        file,
        indent=2
        )

    with open("CYP2C19_2.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    filtered_result = filter_pharmvar_json(result)

    with open("filtered_CYP2C19_2.json", "w", encoding="utf-8") as file:
        json.dump(filtered_result, file, indent=2)

    print(
        f"Retrieved {len(result)} record(s) "
        f"and saved filtered output."
    )


if __name__ == "__main__":
    main()