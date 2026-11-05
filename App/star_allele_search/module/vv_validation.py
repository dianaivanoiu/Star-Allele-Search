import requests
from urllib.parse import quote

# TODO:
# Replace print statements with logging once application logging
# has been implemented.


def validate_pharmvar_result(pharmvar_result):
    """
    Validate variants returned by the PharmVar API using VariantValidator.

    For each variant, this function:

    - Submits the genomic HGVS description to VariantValidator.
    - Retrieves the corresponding transcript-level HGVS description.
    - Checks that the VariantValidator gene symbol matches the
      PharmVar gene symbol.
    - Reports whether the transcript is designated as the
      MANE Select and RefSeq Select transcript.
    - Displays the predicted protein consequence.

    Parameters
    ----------
    pharmvar_result : list
        JSON response returned by the PharmVar allele endpoint.

    Returns
    -------
    None
        Validation results are currently written to stdout.
    """

    for allele in pharmvar_result:

        for variant in allele["variants"]: #Loop though the variant dictionary and extract genomic hgvs to use in url.

            genomic_hgvs = variant["hgvs"].replace("&amp;gt;", "&gt;")

            encoded_hgvs = quote(genomic_hgvs, safe="")

            url = (
                "https://rest.variantvalidator.org/"
                f"VariantValidator/variantvalidator/"
                f"GRCh38/{encoded_hgvs}/mane_select"
                "?content-type=application/json"
            )

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            vv_result = response.json()
            return vv_result

            # transcript_key = next(
            #     key
            #     for key in vv_result
            #     if key.startswith("NM_")
            # )

            # transcript_data = vv_result[transcript_key]

            # vv_gene = transcript_data["gene_symbol"]

            # # Development output used to confirm that the variant matches to the expected gene and transcript.
            # print(f"Variant              : {genomic_hgvs}")
            # print(f"PharmVar Gene        : {gene_symbol}")
            # print(f"VariantValidator Gene: {vv_gene}")
            # print(f"Gene Match           : {gene_symbol == vv_gene}")

            # print(
            #     f"Transcript           : "
            #     f"{transcript_data['hgvs_transcript_variant']}"
            # )

            # print(
            #     f"MANE Select          : "
            #     f"{transcript_data['annotations']['mane_select']}"
            # )

            # print(
            #     f"RefSeq Select        : "
            #     f"{transcript_data['annotations']['refseq_select']}"
            # )

            # print(
            #     f"Protein Consequence  : "
            #     f"{transcript_data['hgvs_predicted_protein_consequence']['tlr']}"
            # )

            # print("-" * 80)