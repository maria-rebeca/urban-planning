import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge  # <--- CHANGED: Use Linear Regression
from sklearn.metrics import mean_squared_error, r2_score
import joblib 
import json
import os

# 1. Load the dataset
try:
    # Try current directory first, then parent directory (standard safety check)
    if os.path.exists('final_training_data.csv'):
        data = pd.read_csv('final_training_data.csv')
    elif os.path.exists('../../final_training_data.csv'):
        data = pd.read_csv('../../final_training_data.csv')
    else:
        raise FileNotFoundError("final_training_data.csv")
    
    print("✅ CSV file loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'final_training_data.csv' not found.")
    exit()

# 2. Define Features (X) and Target (y)
features = [col for col in data.columns if col != 'target_temp']
target = 'target_temp'

X = data[features]
y = data[target]

## Save the column names list so the backend knows what order to use
feature_columns = list(X.columns)
with open('model_columns.json', 'w') as f:
    json.dump(feature_columns, f)
print("✅ Saved model_columns.json")

# 3. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")

# 4. Initialize and Train the Model (LINEAR RIDGE)
print("\n⏳ Training Linear (Ridge) Model...")
# alpha=1.0 is standard regularization. You can increase it (e.g. 5.0) if the model is still too jumpy.
model = Ridge(alpha=1.0) 
model.fit(X_train, y_train)
print("✅ Model training complete.")

# 5. Evaluate
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print(f"\n📊 Model Performance on Test Set:")
print(f"   Root Mean Squared Error (RMSE): {rmse:.4f} °C")
print(f"   R² Score: {r2:.4f}")

# 6. EXPLAIN THE LOGIC (Coefficients)
# This will show you exactly what heats vs cools the city
print("\n🧠 MODEL LOGIC (Impact per 1% change):")
print("-" * 60)
coefs = pd.DataFrame({
    'Feature': X.columns,
    'Impact': model.coef_
}).sort_values(by='Impact', ascending=False)

for index, row in coefs.iterrows():
    print(f"   {row['Feature']:<15} : {row['Impact']:+.4f}")
print("-" * 60)

# Check Industry vs Housing specific logic
try:
    urban_impact = coefs[coefs['Feature'] == 'pct_11100']['Impact'].values[0]
    industry_impact = coefs[coefs['Feature'] == 'pct_12100']['Impact'].values[0]
    print(f"\n🔍 Comparison:")
    print(f"   Housing (11100) : {urban_impact:+.4f}")
    print(f"   Industry (12100): {industry_impact:+.4f}")
    if industry_impact > urban_impact:
        print("   ✅ Logic Check: Industry is HOTTER than Housing.")
    else:
        print("   ⚠️ Data Reality: Housing is HOTTER than Industry in this dataset.")
except:
    pass

# 7. Save Model
model_filename = 'urban_heat_model.joblib' # Changed to standard name for backend
joblib.dump(model, model_filename)
print(f"\n💾 Model saved to '{model_filename}'")