import requests

def fetch_mutation_data(study_id, sample_id):
    print(f"🔍 Fetching from cBioPortal → Study: {study_id}, Sample: {sample_id}")
    
    url = "https://www.cbioportal.org/api/mutations/fetch"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "sampleIds": [sample_id],
        "studyId": study_id
    }

    response = requests.post(url, headers=headers, json=data)

    print("Status Code:", response.status_code)
    print("Response Text:\n", response.text[:200])  # Preview only

    if response.status_code != 200:
        raise RuntimeError(f"❌ Failed to fetch mutation data. HTTP {response.status_code}")
    
    try:
        result = response.json()
        if not isinstance(result, list):
            raise RuntimeError("❌ Unexpected response format from cBioPortal")
        return result
    except Exception as e:
        raise RuntimeError(f"❌ Error parsing JSON: {e}")
