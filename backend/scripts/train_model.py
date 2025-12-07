import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib 

# 1. Load the dataset
try:
    data = pd.read_csv('c:/ROSPIN/urban-planning/backend/scripts/final_training_data.csv')
    print("CSV file loaded successfully.")
except FileNotFoundError:
    print("Error: 'final_training_data.csv' not found. Make sure the file is in the same directory.")
    exit()

# 2. Define Features (X) and Target (y)
features = [col for col in data.columns if col != 'target_temp']
target = 'target_temp'

X = data[features]
y = data[target]

# 3. Split the data into training and testing sets
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")

# 4. Initialize and Train the Model
# A RandomForestRegressor is a good starting point for many tabular data problems.
model = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)

print("\nTraining the model...")
model.fit(X_train, y_train)
print("Model training complete.")

# 5. Evaluate the Model
# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f"\nModel Performance on Test Set:")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"  This means on average, the model's predictions are off by about {rmse:.4f} degrees.")
# You can also check the Out-of-Bag score, which is an internal validation metric
print(f"Out-of-Bag (OOB) Score: {model.oob_score_:.4f}")


# 6. Save the Trained Model
# After training, you can save the model to a file to use it later for predictions
# without having to retrain it.
model_filename = 'urban_heat_model.joblib'
joblib.dump(model, model_filename)
print(f"\nModel saved to '{model_filename}'")


# 7. Create and Save a Predictions CSV
# Create a new DataFrame to compare actual vs. predicted values
predictions_df = pd.DataFrame({
    'Actual_Temperature': y_test,
    'Predicted_Temperature': y_pred
})

# Round the values for easier reading
predictions_df['Predicted_Temperature'] = predictions_df['Predicted_Temperature'].round(2)

# Save the DataFrame to a new CSV file
predictions_filename = 'predictions.csv'
predictions_df.to_csv(predictions_filename, index=False)

print(f"\nPredictions saved to '{predictions_filename}'")
