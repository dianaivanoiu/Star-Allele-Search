import requests

BASE_URL = "https://rest.genenames.org/fetch/symbol/"

HEADERS = {
    "accept": "application/json",
}

def get_hgnc_json(gene_symbol):
    hgnc_symbol = gene_symbol.strip().upper().split("*")[0]

    url = f"{BASE_URL}{hgnc_symbol}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_hgnc_id(data):
    docs = data["response"]["docs"]

    for entry in docs:
        return entry["hgnc_id"]
    return None