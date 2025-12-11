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
                print("Warning: model_columns.json not found!")

        except Exception as e:
            print(f"❌ Error loading AI model: {e}")

    def predict_temperature(self, user_land_use):
        if not self.model:
            raise Exception("Model is not loaded.")


        input_data = {col: 0.0 for col in self.expected_columns}
        for code, percent in user_land_use.items():
            clean_code = str(code).replace('pct_', '')
            col_name = f"pct_{clean_code}"
            if col_name in input_data:
                input_data[col_name] = float(percent)
        
        total_sum = sum(input_data.values())
        print(f"📊 Input Data Sum: {total_sum:.2f}%")
        
        if abs(total_sum - 100) > 1:
            print("The data sums to less/more than 100%. This breaks the physics!")
            print("The model thinks the city is partially 'Empty Space'.")

        df = pd.DataFrame([input_data])
        df = df[self.expected_columns]
        return self.model.predict(df)[0]

ai_service = AIService()