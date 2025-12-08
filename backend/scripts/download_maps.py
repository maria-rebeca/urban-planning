import os
import cdsapi # Incarcat dar nefolosit in fluxul simplificat
import xarray as xr # Incarcat dar nefolosit in fluxul simplificat
import pandas as pd
import numpy as np
import rasterio # Incarcat dar nefolosit in fluxul simplificat
import rioxarray as rxr # Incarcat dar nefolosit in fluxul simplificat
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
from rasterio.enums import Resampling
import sys

# --- CONFIGURARE ȘI CONSTANTE ---
# Directorul de bază al scriptului
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Zona de interes (lat_max, lon_min, lat_min, lon_max) - București extins
BUCHAREST_AREA = [44.61, 25.86, 44.23, 26.46] 

# Fişiere de date geo-spațiale (Constante necesare doar pentru citire/scriere path-uri)
LANDUSE_PATH = os.path.join(BASE_DIR, 'landuse.tif')
NO2_NC_FILE = os.path.join(BASE_DIR, "no2_cams_data.nc")
TEMP_NC_FILE = os.path.join(BASE_DIR, "temp_era5_data.nc")
NO2_TIF_FILE = os.path.join(BASE_DIR, "no2_cams_processed.tif")
TEMP_TIF_FILE = os.path.join(BASE_DIR, "temp_era5_processed.tif")

# Parametri de Agregare (Constante necesare doar pentru Etapa 3, acum ignorate)
PIXEL_SIZE = 30 
GRID_SIZE = 1000 

# Fișierul final de training și Modelul (CONSTANTE CRITICE)
OUTPUT_CSV_FILE = os.path.join(BASE_DIR, 'no2_training_data.csv')
MODEL_FILENAME = os.path.join(BASE_DIR, 'urban_no2_model.joblib')

# Inițializare CDSAPI (Ignorată, deoarece nu facem descărcare)
try:
    client = cdsapi.Client()
except:
    pass

# --------------------------------------------------------------------------------------
## ETAPA 1: DESCĂRCAREA DATELOR DIN COPENICUS (IGNORATĂ)
# --------------------------------------------------------------------------------------

def download_data():
    """Funcție ignorată: Presupunem că fișierele NC există deja."""
    # if not os.path.exists(NO2_NC_FILE):
    #     ... (logica de descărcare NO2)
    # if not os.path.exists(TEMP_NC_FILE):
    #     ... (logica de descărcare Temperatură)
    print("Etapa 1 (Descărcare .nc) ignorată.")
    pass
        
# --------------------------------------------------------------------------------------
## ETAPA 2: PRE-PROCESAREA DATELOR NETCDF ȘI CONVERSIE LA TIF (IGNORATĂ)
# --------------------------------------------------------------------------------------

def process_netcdf_to_tif(input_nc, output_tif, var_name):
    """Funcție ignorată: Presupunem că GeoTIFF-urile au fost deja create."""
    # if not os.path.exists(input_nc):
    #     ...
    # mean_data = ds.mean(dim=time_dim) 
    # mean_data.rio.to_raster(output_tif, nodata=-9999)
    print("Etapa 2 (Conversie .tif) ignorată.")
    return True # Returnăm True pentru a simula succesul

# --------------------------------------------------------------------------------------
## ETAPA 3: GENERAREA SETULUI DE DATE CSV (IGNORATĂ)
# --------------------------------------------------------------------------------------

def create_training_csv():
    """Funcție ignorată: Presupunem că fișierul CSV de antrenare există."""
    # df = pd.DataFrame(dataset).fillna(0)
    # df.to_csv(OUTPUT_CSV_FILE, index=False)
    print("Etapa 3 (Creare .csv) ignorată.")
    return True # Returnăm True pentru a simula succesul


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
        print("Vă rugăm să rulați pipeline-ul complet (Etapa 1-3) pentru a genera CSV-ul.")
        
    print("\n🎉 Pipeline finalizat!")