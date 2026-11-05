"""
Query ClinPGx clinical annotations by gene
"""

import json
import requests
import re


BASE_URL = "https://api.clinpgx.org/v1/data/summaryAnnotation"

HEADERS = {
    "accept": "application/json",
}


def get_clinpgx_annotation_json(allele):
    """
    Query ClinPGx and return JSON for the gene the star allele correspond to.

    Parameters
    ----------
    allele : str
         Gene to query (e.g. "CYP2C19").

    Returns
    -------
    list
        JSON response from ClinPGx.
    """

    gene_symbol = allele.strip().upper().split("*")[0]

    url = f"{BASE_URL}"

    PARAMS = {
        "location.genes.symbol": gene_symbol,
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=PARAMS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def get_filtered_annotations(allele):
    """
      Filter summary annotations to keep only the ones containing the requested allele

      Parameters
      ----------
      allele : str
           Allele to query (e.g. "CYP2C19*2").

      Returns
      -------
      list
          Filtered JSON response from get_clinpgx_annotation_json function.
      """
    annotation_data = get_clinpgx_annotation_json(allele)
    allele = allele.strip().upper()
    matching_annotations = []

    pattern = re.compile(
        re.escape(allele) + r"(?![A-Z0-9])"
    ) # code generated using AI; to change to run faster

    for record in annotation_data.get("data", []):
        record_text = str(record).upper()

        if pattern.search(record_text):
            matching_annotations.append(record) #code generated using AI

    return {"data": matching_annotations}

def main():
    result = get_filtered_annotations("CYP2C19*2")

    with open(
        "CYP2C19_filtered_annotations.json",
        "w",
        encoding="utf-8",
    ) as file: json.dump(result, file, indent=2)

if __name__ == "__main__":
    main()
#test for *23
#test for *1/*2
