import joblib
from sklearn.linear_model import LogisticRegression
import os

# Sample training data
X = [
    [5.0, 0.2],
    [15.0, 0.5],
    [25.0, 0.9],
    [30.0, 0.8]
]
y = [0, 1, 1, 1]  # Labels

# Train model
model = LogisticRegression()
model.fit(X, y)

# Ensure models folder exists
model_dir = "backend/models"
os.makedirs(model_dir, exist_ok=True)

# Save model
model_path = os.path.join(model_dir, "tmb_predictor.joblib")
joblib.dump(model, model_path)

print(f"✅ Model saved to {model_path}")
