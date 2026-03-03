import joblib
import pandas as pd
import json
import os
import sys

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
model_path = os.path.join(current_dir, 'urban_heat_model.joblib') # Check if it's .pkl or .joblib
columns_path = os.path.join(current_dir, 'model_columns.json')

print(f"🔍 Loading model from: {model_path}")

try:
    model = joblib.load(model_path)
    with open(columns_path, 'r') as f:
        expected_columns = json.load(f)
except Exception as e:
    print(f"❌ Error loading files: {e}")
    sys.exit(1)

print("✅ Model loaded.")

# --- TEST FUNCTION ---
def test_scenario(name, active_code):
    # Create a row of all ZEROS
    input_data = {col: 0.0 for col in expected_columns}
    
    # Set the target code to 100%
    target_col = f"pct_{active_code}"
    
    if target_col in input_data:
        input_data[target_col] = 100.0
        
        # Predict
        df = pd.DataFrame([input_data])
        # Force column order
        df = df[expected_columns]
        
        temp = model.predict(df)[0]
        print(f"🧪 100% {name} ({active_code}): {temp:.2f} °C")
    else:
        print(f"⚠️ Column {target_col} not found in model!")

print("\n--- 🧠 MODEL LOGIC CHECK ---")
test_scenario("Continuous Urban (Concrete)", 11100)
test_scenario("Forest", 31000)
test_scenario("Water", 50000)
test_scenario("Industry", 12100)