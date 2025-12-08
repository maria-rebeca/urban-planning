import pandas as pd
import joblib
import os

# --- 1. Load the Trained Model ---
# Get the absolute path to the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'urban_heat_model.joblib')

try:
    model = joblib.load('urban_heat_model.joblib')
    print("Model 'urban_heat_model.joblib' loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}.")
    print("Please run the 'train_model.py' script first to create the model file.")
    exit()

# --- 2. Prepare Your New Data ---
# IMPORTANT: The new data must have the exact same column names as the training data,
# in the same order, excluding the target variable.

# This is a sample row of new data.
# Replace these values with the actual data you want to predict on.
new_data_sample = {
    'pct_11240':0.0, 'pct_12100':0.0, 'pct_21000':0.0, 'pct_23000':0.0, 'pct_50000':0.0, 
    'pct_11100':0.0, 'pct_11220':0.0, 'pct_11230':0.0, 'pct_12220':0.0, 'pct_13300':0.0, 
    'pct_13400':10.08, 'pct_14100':67.9, 'pct_14200':0.0, 'pct_11210':0.0, 'pct_12230':0.0, 
    'pct_31000':0.0, 'pct_11300':0.0, 'pct_32000':0.0, 'pct_12210':0.0, 'pct_24000':0.0, 
    'pct_12400':0.0, 'pct_13100':0.0, 'pct_40000':20.3, 'pct_33000':0.0

    # Note: 'target_temp' is NOT included here, as it's what we want to predict.
}

################ This is the translation of what the new_data_sample means ##############
#new_data_sample = {
#    '*Discontinuous Very Low density Urban Fabric', 'Industrial, Commercial, Public, Military and Private units', 'Arable land', 'Pastures', 'Water Bodies',
#    'Continuous Urban Fabric', 'Discontinuous Medium Urban Fabric', 'Discontinuous Low Density Urban', 'Other roads and associated land', 'Construction Sites',
#    'Land without current use', 'Green Urban Areas', 'Sports and Leisure Facilities', 'Discontinuous Dense Urban Fabric', 'Railways and associated land',
#    'Forests', 'Isolated Structures', 'Scrub and/or Herbaceous vegetation associations', 'Fast transit Roads', 'Complex and mixed cultivations',
#    'Airports', '*Mineral extraction sites', 'Wetlands', 'Open spaces with little or no vegetation'
#}

# The model expects the data in a specific order of columns.
# We will load the original training data columns to ensure the order is correct.
try:
    training_data = pd.read_csv('final_training_data.csv')
    feature_columns = [col for col in training_data.columns if col != 'target_temp']
except FileNotFoundError:
    print("Error: 'final_training_data.csv' not found. Needed to get column order.")
    exit()


# Convert the sample data into a pandas DataFrame, ensuring the column order is correct.
new_data_df = pd.DataFrame([new_data_sample], columns=feature_columns)


# --- 3. Make the Prediction ---
predicted_temperature = model.predict(new_data_df)

# The output of predict() is an array, so we get the first (and only) item.
final_prediction = predicted_temperature[0]

print(f"\nPredicted Temperature: {final_prediction:.2f} degrees")
