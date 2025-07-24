import requests

BASE_URL = "https://www.cbioportal.org/api"
HEADERS = {"Accept": "application/json"}

def get_studies():
    res = requests.get(f"{BASE_URL}/studies", headers=HEADERS)
    return res.json()

def get_case_ids(study_id):
    url = f"{BASE_URL}/studies/{study_id}/cases"
    res = requests.get(url, headers=HEADERS)
    return [case['caseId'] for case in res.json()]

def get_mutations(study_id, sample_id):
    url = f"{BASE_URL}/mutations/fetch"
    data = {
        "molecularProfileIds": [f"{study_id}_mutations"],
        "sampleIds": [sample_id]
    }
    res = requests.post(url, headers=HEADERS, json=data)
    return res.json()
