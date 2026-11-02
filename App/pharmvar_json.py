#Query and filter PharmVar
import os
import requests
#install package (pip install requests) requests https://dev.to/kiprotichterer/extracting-data-from-an-api-using-python-requests-4h5
import json

# curl -X GET "https://www.pharmvar.org/api-service/alleles/CYP2C19*2?reference-collection=GRCh38&exclude-sub-alleles=false&include-reference-variants=false&include-retired-alleles=false&include-retired-reference-sequences=false" \
#   -H "accept: application/json" \
#   -H "Api-Key: e1779867df584c4e9bcca87bcf3a61b3"

base_url = "https://www.pharmvar.org/api-service/alleles"

def get_pharmvar_json(allele):
    """
    Calls PharmVar and return JSON for star allele
    :param allele:
    :return:
    """
    url = f"{base_url}/{allele}"
    headers = {
        "accept": "application/json",
        "Api-Key": "e1779867df584c4e9bcca87bcf3a61b3",
    }

    params = {
        "reference-collection": "GRCh38",
        "exclude-sub-alleles": "false",
        "include-reference-variants": "false",
        "include-retired-alleles": "false",
        "include-retired-reference-sequences": "false",
    }

    response=requests.get(url,headers=headers, params=params)
    return response.json()

def filter_pharmvar_json(result):
    """
    Filtering JSON result for star allele
    :param result:
    :return:
    """
    filtered_result = []
    for allele in result:
        filtered_result.append({
            "geneSymbol": allele.get("geneSymbol"),
            "alleleName": allele.get("alleleName"),
            "references": allele.get("references"),
            "variants": allele.get("variants"),
        })
    return filtered_result

result = get_pharmvar_json("CYP2C19*2")
print(result)

with open("CYP2C19_2.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=2)

filtered_result = filter_pharmvar_json(result)
print(result)

with open("filtered_CYP2C19_2.json", "w",encoding="utf-8") as file:
    json.dump(filtered_result, file, indent=2)