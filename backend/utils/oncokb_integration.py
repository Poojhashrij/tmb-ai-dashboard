import os
import requests

ONCOKB_TOKEN = os.getenv("ONCOKB_TOKEN")
HEADERS = {"Authorization": f"Bearer {ONCOKB_TOKEN}"}

def fetch_oncokb_treatment(gene, alteration):
    url = f"https://www.oncokb.org/api/v1/annotate/mutations/byGene/{gene}/{alteration}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    treatments = []
    for rec in data.get("oncokbAnnotatedAlterations", []):
        for evidence in rec.get("clinicalEvidence", []):
            treatments.append({
                "drug": evidence["drugName"],
                "level": evidence["level"],
                "description": evidence.get("description", "")
            })
    return treatments
