"""
Prepare ClinPGx results for a requested star allele.

Organize the results by summary annotation ID. Keep the annotation fields
needed for display and attach the summaries and full text of the related
guidelines from fetch_guidelines. Add URL fpr tje full text of guidelines.

Group records with the same complete combination of drugs. Return a
list of groups, each containing a drug list and its associated findings.
"""

import json
from typing import List, Dict
from App.star_allele_search.module.clinpgx_summary_annotation import get_filtered_annotations
from App.star_allele_search.module.fetch_guidelines import build_guideline_catalog

###############################################################################
#      I generated the code myself (Diana), unless specifically stated
###############################################################################

base_url = "https://www.clinpgx.org/guidelineAnnotation"

def build_clinpgx_results(allele:str) -> list[dict[str, object]]:
    """
    Build ClinPGx results for a requested star allele.

    Each summary annotation is represented by a dictionary containing its
    accession ID, matching phenotype text, drug names, disease names,
    categories, and related guidelines. Each guideline includes a URL
    to its ClinPGx annotation page.

    Parameters
    ----------
    allele : str
         Star allele to query (e.g. "CYP2C19*2").

    Returns
    -------
    list of dict
        One dictionary per summary annotation.
        Phenotype is None when no exact allele match is found.
        Missing optional collections are represented by empty lists.

    """

    clinpgx_response = get_filtered_annotations(allele)
    annotations = clinpgx_response["data"]
    guidelines = build_guideline_catalog(clinpgx_response)
    accessions = guidelines["accessions"]

    output_list: List[Dict[str, object]] = []

    allele = allele.strip().split("*")
    requested_allele = "*" + allele[1]

    for record in annotations:
        annotation_result: Dict[str, object] = {}
        annotation_result["annotation_id"] = record["accessionId"]
        annotation_result["phenotype"] = None
        annotation_result["drugs"] = []
        annotation_result["diseases"] = []
        annotation_result["guidelines"] = []

        for phenotype_entry in record.get("allelePhenotypes") or []:
            if requested_allele == phenotype_entry["allele"]:
                annotation_result["phenotype"] = phenotype_entry["phenotype"]
                break

        for chemical_entry in record.get("relatedChemicals") or []:
            annotation_result["drugs"].append(chemical_entry["name"])

        for disease_entry in record.get("relatedDiseases") or []:
            annotation_result["diseases"].append(disease_entry["name"])

        annotation_result["categories"] = record.get("types") or []

        for accession in accessions:
            if annotation_result["annotation_id"] == accession["accessionId"]:
                annotation_result["guidelines"] = accession["guidelines"]
                for guideline in annotation_result["guidelines"]:
                    guideline_id = guideline["id"]
                    url = f"{base_url}/{guideline_id}"
                    guideline["url"] = url
                break

        output_list.append(annotation_result)

    return output_list

def group_clinpgx_results (allele:str):
    """
    Group ClinPGx results by their complete combination of drugs.

    Annotations with the same drug names are collected into one group,
    regardless of the order of the names. Each annotation is retained
    as a separate finding within its group.

    Parameters
    ----------
    allele : str
        Star allele to query (e.g. "CYP2C19*2").

    Returns
    -------
    list of dict
        One dictionary per distinct drug combination, containing:
        - drugs: an alphabetically sorted list of drug names.
        - findings: a list of the associated annotation dictionaries.
        Annotations with no drugs are collected in a group with an
        empty drugs list. Returns an empty list when no annotations exist.
    """
    annotations = build_clinpgx_results(allele)
    groups_by_drugs: Dict[str, object] = {}

    for annotation in annotations:
        drugs_list = annotation["drugs"]
        sorted_drugs = sorted(drugs_list)
        drugs_keys = tuple(sorted_drugs)

        if drugs_keys not in groups_by_drugs:
            new_group = {}
            new_group["drugs"] = sorted_drugs
            new_group["findings"] = []
            groups_by_drugs[drugs_keys] = new_group

        groups_by_drugs[drugs_keys]["findings"].append(annotation)

    return list(groups_by_drugs.values())

def main():
    result = group_clinpgx_results("CYP2C19*2")
    print(result)

    with open("clinpgx_results.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

if __name__ == "__main__":
    main()

