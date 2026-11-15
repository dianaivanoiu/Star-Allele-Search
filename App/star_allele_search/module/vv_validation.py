import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

###############################################################################################################
#                           AI use declaration                                                                #
# Copilot powered by GPT-5 was used to develop most of the functions and was ammended manually in some places.#
###############################################################################################################

def validate_pharmvar_result(pharmvar_result):
    """
    Validate variants returned by the PharmVar API using VariantValidator.

    For each variant, this function:

    - Submits the genomic HGVS description to VariantValidator.
    - Retrieves the corresponding transcript-level HGVS description.

    Parameters
    ----------
    pharmvar_result : list
        JSON response returned by the PharmVar allele endpoint.

    Returns
    -------
        JSON response from VariantValidator
    """

    email = os.getenv("TERRACIPHER_EMAIL")
    password = os.getenv("TERRACIPHER_PASSWORD")

    if not email or not password:
        raise ValueError(
            "Please set login details to terra"
        )

    session = requests.Session()

    auth_response = session.get(
        "https://shaipup.com/market/token",
        auth=(email, password),
        timeout=30,
    )
    auth_response.raise_for_status()

    authorization_header = auth_response.headers.get("Authorization")

    if not authorization_header:
        raise ValueError(
            "No Authorization header was returned by TerraCipher."
        )

    if authorization_header.lower().startswith("bearer "):
        id_token = authorization_header.split(" ", 1)[1]
    else:
        id_token = authorization_header

    for allele in pharmvar_result:

        for variant in allele["variants"]:

            genomic_hgvs = variant["hgvs"].replace(
                "&amp;amp;gt;",
                "&gt;",
            )

            payload = [
                {
                    "variant_description": [
                        genomic_hgvs
                    ],
                    "genome_build": "GRCh38",
                    "select_transcripts": [
                        "mane_select"
                    ],
                }
            ]

            response = session.post(
                (
                    "https://shaipup.com/market/shaip/variantvalidator"
                    "?owner=VariantValidator"
                    "&shaip=rest-variantvalidator2"
                ),
                headers={
                    "Authorization": f"Bearer {id_token}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )
            response.raise_for_status()

            vv_result = response.json()
            if not isinstance(vv_result, dict):
                return {}

            return {
                key: value
                for key, value in vv_result.items()
                if isinstance(value, dict)
                and "hgvs_transcript_variant" in value
            }

    return {}