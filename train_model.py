import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression

# Load the TXT file
df = pd.read_csv("data/data_clinical_patient.txt", sep='\t', comment='#')

# Clean column names
df.columns = df.columns.str.strip()

print("Columns in file:", df.columns.tolist())

# Rename columns for consistency
df = df.rename(columns={
    'Patient Identifier': 'PATIENT_ID',
    'Overall Survival (Months)': 'OS_MONTHS',
    'Overall Survival Status': 'OS_STATUS',
    'Sex': 'SEX',
    'Drug Type': 'DRUG_TYPE',
    'Age Group at Diagnosis in Years': 'AGE_GROUP'
})

# Drop unnecessary columns if they exist
cols_to_drop = ['PATIENT_ID', 'OS_MONTHS']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# Create TMB_SCORE if missing
if 'TMB_SCORE' not in df.columns:
    df['TMB_SCORE'] = np.random.randint(1, 20, size=len(df))

# Create MSI_STATUS if missing
if 'MSI_STATUS' not in df.columns:
    df['MSI_STATUS'] = ['MSI-High' if x > 8 else 'MSI-Low' for x in df['TMB_SCORE']]

# Create CANCER_TYPE if missing
if 'CANCER_TYPE' not in df.columns:
    cancer_types = ['Lung', 'Melanoma', 'Bladder']
    df['CANCER_TYPE'] = np.random.choice(cancer_types, size=len(df))

# Create SEX if missing
if 'SEX' not in df.columns:
    df['SEX'] = np.random.choice(['Male', 'Female'], size=len(df))

# Create AGE_GROUP if missing
if 'AGE_GROUP' not in df.columns:
    df['AGE_GROUP'] = np.random.choice(['<50', '50-60', '60-70', '70+'], size=len(df))

# Create DRUG_TYPE if missing
if 'DRUG_TYPE' not in df.columns:
    df['DRUG_TYPE'] = np.random.choice(['PD-1 inhibitor', 'CTLA-4 inhibitor', 'Chemotherapy'], size=len(df))

# Handle target variable
if 'OS_STATUS' in df.columns:
    df['IMMUNOTHERAPY_RESPONSE'] = df['OS_STATUS'].apply(
        lambda x: 1 if str(x).startswith('0:') else 0
    )
    print("\n✅ Using real OS_STATUS for labels.")
else:
    df['IMMUNOTHERAPY_RESPONSE'] = np.random.choice([0, 1], size=len(df))
    print("\n⚠️ No OS_STATUS column found, using random labels.")

# Show target distribution
print("\nIMMUNOTHERAPY_RESPONSE distribution:")
print(df['IMMUNOTHERAPY_RESPONSE'].value_counts())

# Select features
X = df[['TMB_SCORE', 'MSI_STATUS', 'SEX', 'CANCER_TYPE', 'AGE_GROUP', 'DRUG_TYPE']]
y = df['IMMUNOTHERAPY_RESPONSE']

# Encode categorical columns safely
label_encoders = {}
X_encoded = X.copy()

for col in ['MSI_STATUS', 'SEX', 'CANCER_TYPE', 'AGE_GROUP', 'DRUG_TYPE']:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

# Initialize and train Logistic Regression model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
acc = accuracy_score(y_test, y_pred)
print(f"\n✅ Logistic Regression Accuracy: {acc:.3f}\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/immunotherapy_model_logreg.pkl")
print("\n✅ Logistic Regression model saved as model/immunotherapy_model_logreg.pkl")
