import requests

def get_clinical_trials(cancer_type, limit=5):
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={cancer_type}&pageSize={limit}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    trials = []
    for study in response.json().get("studies", []):
        id_module = study.get("protocolSection", {}).get("identificationModule", {})
        design_module = study.get("protocolSection", {}).get("designModule", {})
        status_module = study.get("protocolSection", {}).get("statusModule", {})

        trial_id = id_module.get("nctId", "N/A")
        title = id_module.get("officialTitle", "N/A")
        phase = design_module.get("phase", {}).get("phase", "N/A")
        status = status_module.get("overallStatus", "N/A")
        link = f"https://clinicaltrials.gov/study/{trial_id}"

        trials.append({
            "Trial ID": trial_id,
            "Title": title,
            "Phase": phase,
            "Status": status,
            "Link": link
        })

    return trials
