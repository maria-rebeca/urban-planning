import joblib
import pandas as pd
import json
import os
import numpy as np

class AIService:
    def __init__(self):
        self.model = None
        self.expected_columns = None
        self.load_model()

    def load_model(self):
        """Loads the model and column names into memory ONCE."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'scripts', 'urban_heat_model.joblib')
            columns_path = os.path.join(base_dir, 'scripts', 'model_columns.json')

            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print("AI Model Loaded Successfully")
            else:
                print("Warning: urban_heat_model.joblib not found!")

            if os.path.exists(columns_path):
                with open(columns_path, 'r') as f:
                    self.expected_columns = json.load(f)
            else:
                print("⚠️ Warning: model_columns.json not found!")

        except Exception as e:
            print(f"❌ Error loading AI model: {e}")

    def predict_temperature(self, user_land_use):
        """
        Args:
            user_land_use (dict): { "11100": 50.5, "14100": 20.0, ... }
        Returns:
            float: Predicted Temperature
        """
        if not self.model or not self.expected_columns:
            raise Exception("Model is not loaded.")

        # 1. Create a dictionary with ALL zeros for every expected column
        # This ensures we have the 24 columns the model expects
        input_data = {col: 0.0 for col in self.expected_columns}

        # 2. Fill in the values provided by the user
        for code, percent in user_land_use.items():
            col_name = f"pct_{code}" # Match the training name (e.g., pct_11100)
            if col_name in input_data:
                input_data[col_name] = float(percent)

        total_input = sum(input_data.values())
        print(f"🤖 AI Input Sum: {total_input}%")
        # 3. Convert to DataFrame (1 row)
        df = pd.DataFrame([input_data])

        # 4. Predict
        prediction = self.model.predict(df)[0]
        return round(prediction, 2)

# Create a single instance to be imported
ai_service = AIService()