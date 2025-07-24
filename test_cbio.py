import requests

url = "https://www.cbioportal.org/api/mutations/fetch"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    "sampleIds": ["TCGA-A1-A0SB-01"],  # ✅ Known valid sample
    "studyId": "brca_tcga"             # ✅ TCGA Breast Cancer
}

response = requests.post(url, headers=headers, json=data)
print(f"Status Code: {response.status_code}")
print("Response Text:\n", response.text)

try:
    result = response.json()
    print("✅ JSON Parsed!")
    print(f"🔬 Mutation count: {len(result)}")
except Exception as e:
    print(f"❌ Failed to parse JSON: {e}")
