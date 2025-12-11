import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.model_selection import train_test_split, GridSearchCV #added
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor #added
from sklearn.metrics import mean_squared_error, r2_score #added
from sklearn.preprocessing import StandardScaler, PolynomialFeatures  #added

import joblib 

# 1. Load the dataset
try:
    data = pd.read_csv('C:/ROSPIN/urban-planning/backend/scripts/final_training_data.csv')
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
#model = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)
Gradient_model = GradientBoostingRegressor(random_state=42)

param_grid = {
    'n_estimators': [100, 200, 300],  #How many trees in the forest
    'learning_rate': [0.01, 0.05, 0.1], # How much each tree contributes to the overall prediction
    'max_depth': [3, 4, 5],  # Maximum depth of each tree
    'subsample': [0.8, 1.0]  # Fraction of samples to be used for fitting the individual base learners
}

print("\nStarting automated tuning (Grid Search)...")

grid_search = GridSearchCV(estimator=Gradient_model, param_grid=param_grid, 
                           cv=5, n_jobs=-1, verbose=1, scoring='neg_mean_squared_error')

print("\nTraining the model...")
grid_search.fit(X_train, y_train)
print("Model training complete.")

# 5. Evaluate the Model
# Make predictions on the test set
Best_model = grid_search.best_estimator_
print(f"\nBest Hyperparameters: {grid_search.best_params_}")
y_pred = Best_model.predict(X_test)

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
    'Predicted_Temperature': y_pred,
    'Difference': (y_test - y_pred).round(2)
})

# Round the values for easier reading
predictions_df['Predicted_Temperature'] = predictions_df['Predicted_Temperature'].round(2)

# Save the DataFrame to a new CSV file
predictions_filename = 'predictions.csv'
predictions_df.to_csv(predictions_filename, index=False)

print(f"\nPredictions saved to '{predictions_filename}'")
