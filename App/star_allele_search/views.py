import json
from django.shortcuts import render
from pathlib import Path


def home(request):
    query = request.GET.get('search')
    allele_info = None

    if query:
        allele_file = Path(__file__).resolve().parent/"data"/f"{query}.json"
        if allele_file.is_file():
            with open(allele_file, encoding="utf-8") as f:
                allele_info = json.load(f)

    return render(request, 'home.html', {'query': query, 'info': allele_info})