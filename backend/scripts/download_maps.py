import os
import cdsapi # Incarcat dar nefolosit in fluxul simplificat
import xarray as xr # Incarcat dar nefolosit
import pandas as pd
import numpy as np
import rasterio # Incarcat dar nefolosit
import rioxarray as rxr # Incarcat dar nefolosit
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
from rasterio.enums import Resampling # Incarcat dar nefolosit
import sys

# --- CONFIGURARE ȘI CONSTANTE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constante Geografice (necesare doar pentru referință, nu pentru rulare)
BUCHAREST_AREA = [44.61, 25.86, 44.23, 26.46] 
LANDUSE_PATH = os.path.join(BASE_DIR, 'landuse.tif')

# Fișierul final de training și Modelul (CONSTANTE CRITICE)
OUTPUT_CSV_FILE = os.path.join(BASE_DIR, 'no2_training_data.csv')
MODEL_FILENAME = os.path.join(BASE_DIR, 'urban_no2_model.joblib')

# Inițializare CDSAPI (Ignorată)
try:
    client = cdsapi.Client()
except:
    pass

# --------------------------------------------------------------------------------------
## ETAPA 1, 2, 3: PRELUCRAREA DATELOR (IGNORATE)
# --------------------------------------------------------------------------------------

# Funcțiile de descărcare și procesare Geo-Spațială sunt definite, dar ignorate în fluxul principal.
def download_data():
    pass
def process_netcdf_to_tif(input_nc, output_tif, var_name):
    return True
def create_training_csv():
    return True


# --------------------------------------------------------------------------------------
## ETAPA 4: ANTRENAREA MODELULUI NO₂ ÎN CASCADĂ (ACTIVĂ)
# --------------------------------------------------------------------------------------

def train_no2_model():
    """Antrenează modelul NO₂ folosind setul de date generat."""
    if not os.path.exists(OUTPUT_CSV_FILE):
        return

    print("\n--- 4. Antrenarea Modelului NO₂ (Cascadă) ---")
    
    # CRITIC: Citește direct fișierul CSV existent
    data = pd.read_csv(OUTPUT_CSV_FILE)
    
    TARGET_COLUMN = 'target_no2'
    # Caracteristicile includ procentele de Land Use ȘI Temperatura
    features = [col for col in data.columns if col != TARGET_COLUMN]
    target = TARGET_COLUMN

    X = data[features]
    y = data[target]
         
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Antrenare Random Forest
    model_no2 = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)
    model_no2.fit(X_train, y_train)

    # Evaluare
    y_pred = model_no2.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    
    print(f"✅ Model antrenat. RMSE: {rmse:.8f}")

    # Salvarea Modelului (.joblib)
    joblib.dump(model_no2, MODEL_FILENAME)
    print(f"💾 Model salvat ca: {MODEL_FILENAME}")


# --- RULARE FLUX DE LUCRU PRINCIPAL ---

if __name__ == "__main__":
    
    # 🛑 FLUX SIMPLIFICAT: Verifică CSV-ul și trece direct la antrenare
    
    # Verificăm dacă fișierul CSV de antrenare există
    if os.path.exists(OUTPUT_CSV_FILE):
        print(f"✅ Fișierul CSV de antrenare ({OUTPUT_CSV_FILE}) există. Trecem direct la Etapa 4 (Antrenare Model).")
        
        # 4. Antrenare Model
        train_no2_model()
    else:
        print(f"❌ Eroare: Fișierul CSV de antrenare ({OUTPUT_CSV_FILE}) nu a fost găsit.")
        print("Vă rugăm să vă asigurați că ați generat CSV-ul sau că acesta se află în directorul corect.")
        
    print("\n🎉 Pipeline finalizat!")