import pytest

from App.star_allele_search.module.hgnc_id import get_hgnc_id, get_hgnc_json

def test_get_hgnc_id():
    gene_symbol = {"response": {"docs": [{"hgnc_id": "HGNC:2621"}]}}
    assert get_hgnc_id(gene_symbol) == "HGNC:2621"


def test_get_hgnc_json():
    