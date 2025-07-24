import requests

def suggest_drugs_based_on_tmb(tmb_value, cancer_type):
    """
    Suggest immunotherapy drugs based on TMB value and cancer type.
    :param tmb_value: float - Tumor Mutational Burden (TMB)
    :param cancer_type: str - Type of cancer (e.g., "Lung Cancer", "Melanoma")
    :return: List of suggested drugs
    """
    drug_guidelines = {
        'Lung Cancer': {
            'threshold': 10,
            'drugs': ['Nivolumab', 'Pembrolizumab']
        },
        'Melanoma': {
            'threshold': 12,
            'drugs': ['Ipilimumab', 'Nivolumab']
        },
        'Colorectal Cancer': {
            'threshold': 10,
            'drugs': ['Pembrolizumab']
        },
        'Bladder Cancer': {
            'threshold': 10,
            'drugs': ['Atezolizumab']
        },
        'Cervical Cancer': {
            'threshold': 10,
            'drugs': ['Pembrolizumab']
        },
        'Other': {
            'threshold': 10,
            'drugs': ['Nivolumab (general)', 'Durvalumab (general)']
        }
    }

    cancer_type = str(cancer_type).strip().title()
    guidelines = drug_guidelines.get(cancer_type, drug_guidelines['Other'])

    if tmb_value >= guidelines['threshold']:
        return guidelines['drugs']
    else:
        return []

def fetch_trials(cancer_type, drug_name='', limit=5):
    """
    Fetch matching clinical trials from ClinicalTrials.gov API v2
    based on cancer type and optionally a drug name.
    :param cancer_type: str
    :param drug_name: str (optional)
    :param limit: int
    :return: List of trial dictionaries with ID, Title, Phase, Status, and Link
    """
    query = f"{cancer_type} {drug_name}".strip()
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={query}&pageSize={limit}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return [{"Title": "Error fetching trials", "Trial ID": "N/A", "Phase": "N/A", "Status": "N/A", "Link": "#"}]

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

    except Exception as e:
        return [{"Title": f"Error: {e}", "Trial ID": "N/A", "Phase": "N/A", "Status": "N/A", "Link": "#"}]


# ✅ Test block (for standalone testing only)
if __name__ == "__main__":
    tmb_value = 13.5
    cancer = "lung cancer"

    print("💊 Suggested Immunotherapy Drugs:")
    drugs = suggest_drugs_based_on_tmb(tmb_value, cancer)
    if drugs:
        for drug in drugs:
            print(f" - {drug}")
    else:
        print("No drugs suggested for the given TMB and cancer type.")

    print("\n🧪 Matching Clinical Trials:")
    trials = fetch_trials(cancer, drugs[0] if drugs else "")
    for trial in trials:
        print(f" - {trial['Title']} ({trial['Trial ID']}) — {trial['Phase']} | {trial['Status']}")
        print(f"   🔗 {trial['Link']}\n")
