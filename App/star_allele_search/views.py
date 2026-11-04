import requests
from django.shortcuts import render


from .module.pharmvar_json import get_pharmvar_json
from .module.hgnc_id import get_hgnc_json, get_hgnc_id



def home(request):
    query = request.GET.get('search')
    allele_info = None
    hgnc_id = None

    if query:
        try:
            allele_info = get_pharmvar_json(query)
        except requests.exceptions.RequestException:
            allele_info = None

        try:
            hgnc_data = get_hgnc_json(query)
            hgnc_id = get_hgnc_id(hgnc_data)
        except:
            hgnc_id = None
        
    return render(request, 'home.html', {'query': query, 'info': allele_info, 'hgnc_id': hgnc_id})


#The below function takes in a json file
#def home(request):
    query = request.GET.get('search')
    allele_info = None

    if query:
        allele_file = Path(__file__).resolve().parent/"data"/f"{query}.json"
        if allele_file.is_file():
            with open(allele_file, encoding="utf-8") as f:
                allele_info = json.load(f)

    return render(request, 'home.html', {'query': query, 'info': allele_info})

