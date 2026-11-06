import requests

BASE_URL = "https://rest.genenames.org/fetch/symbol/"

HEADERS = {
    "accept": "application/json",
}

def get_hgnc_json(gene_symbol):
    """
    Retrieves JSON from HGNC
    """
    
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
    """
    Retrieves HGNC from JSON
    """

    docs = data["response"]["docs"]

    for entry in docs:
        return entry["hgnc_id"]
    return None


def main_hgnc(query):
    """
    Retrieves HGNC ID from query
    """

    json = get_hgnc_json(query)
    id = get_hgnc_id(json)
    return id