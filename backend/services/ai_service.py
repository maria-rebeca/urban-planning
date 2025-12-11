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

    def predict_pollution(self, user_land_use):
        if not self.expected_columns:
            raise Exception("Model columns not loaded.")

        pollution_impact = {
            '12100': 1.8,    
            '11100': 0.8,    
            '12210': 0.7,    
            '12220': 0.5,    
            '12400': 0.6,    
            '31000': -1.2,   
            '14100': -0.5,   
            '50000': -0.1,   
            '13400': 0.2,    
        }
        
        base_pollution_index = 30.0 
        total_pollution_change = 0.0

        for col_name, percent in user_land_use.items():
            key = col_name.replace('pct_', '') 
            impact = pollution_impact.get(key, 0.0)
            
            total_pollution_change += percent * impact
        
        final_pollution = base_pollution_index + (total_pollution_change / 100)
        
        return max(1.0, final_pollution)

    def predict_temperature(self, user_land_use):
        if not self.model:
            raise Exception("Model is not loaded.")

        input_data = {col: 0.0 for col in self.expected_columns}
        for col_name, percent in user_land_use.items():
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