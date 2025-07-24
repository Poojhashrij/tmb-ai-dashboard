import gzip
import re
import os
from utils.cbio_fetcher import fetch_mutation_data


def calculate_tmb(vcf_path):
    """
    Calculate Tumor Mutational Burden (TMB) from a local VCF (.vcf or .vcf.gz) file.

    Args:
        vcf_path (str): Path to the VCF file.

    Returns:
        float: TMB score (mutations per megabase).
    """
    try:
        if not os.path.exists(vcf_path):
            raise FileNotFoundError(f"VCF file not found: {vcf_path}")

        open_func = gzip.open if vcf_path.endswith('.gz') else open
        mutations = 0

        with open_func(vcf_path, 'rt') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                fields = line.strip().split('\t')
                if len(fields) > 6 and re.match(r'PASS', fields[6], re.IGNORECASE):
                    mutations += 1

        exome_size_mb = 38  # Approximate size of human exome
        tmb = round(mutations / exome_size_mb, 2)

        print(f"✅ TMB from file: {mutations} mutations → {tmb} mutations/MB")
        return tmb

    except Exception as e:
        raise RuntimeError(f"❌ Error calculating TMB from VCF: {e}")


def calculate_tmb_from_cbio(study_id, sample_id):
    """
    Calculate TMB from cBioPortal using study_id and sample_id.

    Args:
        study_id (str): ID of the study on cBioPortal.
        sample_id (str): Sample ID within the study.

    Returns:
        float: TMB score (mutations per megabase).
    """
    try:
        mutations = fetch_mutation_data(study_id, sample_id)

        if not isinstance(mutations, list):
            raise ValueError("❌ Unexpected mutation data format from cBioPortal.")

        mutation_count = len(mutations)
        exome_size_mb = 38
        tmb = round(mutation_count / exome_size_mb, 2)

        print(f"✅ TMB from cBioPortal: {mutation_count} mutations → {tmb} mutations/MB")
        return tmb

    except Exception as e:
        raise RuntimeError(f"❌ Error calculating TMB from cBioPortal: {e}")
