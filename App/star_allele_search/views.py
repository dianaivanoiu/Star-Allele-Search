import requests
from django.shortcuts import render


from .module.pharmvar_json import get_pharmvar_json
from .module.hgnc_id import main_hgnc
from .module.vv_validation import validate_pharmvar_result



def home(request):
    query = request.GET.get('search')
    allele_info = None
    hgnc_id = None
    transcript = None

    if query:
        try:
            allele_info = get_pharmvar_json(query)
        except requests.exceptions.RequestException:
            allele_info = None

        try:
            hgnc_id = main_hgnc(query)
        except (requests.exceptions.RequestException, KeyError):
            hgnc_id = None

        try:
            vv = validate_pharmvar_result(allele_info)
            for value in vv.values():
                transcript = value["hgvs_transcript_variant"]
                break
        except requests.exceptions.RequestException:
            transcript = None
            
    return render(request, 'home.html', {'query': query,
                                         'info': allele_info,
                                         'hgnc_id': hgnc_id,
                                         'transcript': transcript})


# import json
# from pathlib import Path
# #The below function takes in a json file
# def home(request):
#     query = request.GET.get('search')
#     allele_info = None

#     if query:
#         allele_file = Path(__file__).resolve().parent/f"{query}.json"
#         if allele_file.is_file():
#             with open(allele_file, encoding="utf-8") as f:
#                 allele_info = json.load(f)

#     return render(request, 'home.html', {'query': query, 'info': allele_info})


# Claude suggestions for more robust code

#    if allele_info:
#         try:
#             vv = validate_pharmvar_result(allele_info)
#             for value in vv.values():
#                 if isinstance(value, dict) and "hgvs_transcript_variant" in value:
#                     hgvs_transcript = value["hgvs_transcript_variant"]
#                     break
#         except (requests.exceptions.RequestException, KeyError, AttributeError):
#             hgvs_transcript = None
