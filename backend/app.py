from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

# Util imports
from utils.tmb_calculator import calculate_tmb
from utils.msi_score import calculate_msi
from utils.ai_model import predict_response
from utils.clinical_guidelines import suggest_drugs_based_on_tmb, fetch_trials

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('backend', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('vcf_file')
    metadata = {
        "patient_id": request.form.get('patient_id', ''),
        "cancer_type": request.form.get('cancer_type', 'Melanoma'),
        "gender": request.form.get('gender', '')
    }

    if not file:
        return "❌ No VCF file uploaded.", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Step 1: TMB and MSI calculation
        tmb = calculate_tmb(filepath)
        msi = calculate_msi(filepath)

        # Step 2: AI prediction (based on your model)
        prediction = predict_response(tmb, msi)

        # Step 3: Drug suggestion
        drugs = suggest_drugs_based_on_tmb(tmb, msi)

        # Step 4: Clinical trial matching (use first suggested drug and cancer type)
        trials = fetch_trials(metadata['cancer_type'], drugs[0] if drugs else "")
        
    except Exception as e:
        return f"❌ Internal Server Error: {e}", 500

    return render_template(
        'dashboard.html',
        tmb=tmb,
        msi=msi,
        prediction=prediction,
        meta=metadata,
        drugs=drugs,
        trials=trials
    )

if __name__ == '__main__':
    app.run(debug=True)
