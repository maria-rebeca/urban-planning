import os
import cdsapi
import xarray as xr
import pandas as pd
import numpy as np
import rasterio
import rioxarray as rxr
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

# Fişiere de date geo-spațiale (Numele pe care scriptul le așteaptă)
LANDUSE_PATH = os.path.join(BASE_DIR, 'landuse.tif')
NO2_NC_FILE = os.path.join(BASE_DIR, "no2_cams_data.nc")   # <- Fișierul NO2 de 900 MB (schimbați numele dacă e necesar!)
TEMP_NC_FILE = os.path.join(BASE_DIR, "temp_era5_data.nc") # <- Fișierul de Temperatură
NO2_TIF_FILE = os.path.join(BASE_DIR, "no2_cams_processed.tif")
TEMP_TIF_FILE = os.path.join(BASE_DIR, "temp_era5_processed.tif")

# Parametri de Agregare
PIXEL_SIZE = 30 # metri (rezoluția Land Use)
GRID_SIZE = 1000 # metri (1km)

# Fișierul final de training și Modelul
OUTPUT_CSV_FILE = os.path.join(BASE_DIR, 'no2_training_data.csv')
MODEL_FILENAME = os.path.join(BASE_DIR, 'urban_no2_model.joblib')

# Inițializare CDSAPI
try:
    client = cdsapi.Client()
except Exception as e:
    print(f"❌ Eroare la inițializarea CDSAPI. Asigurați-vă că fișierul .cdsapirc este corect.")
    sys.exit(1)

# --------------------------------------------------------------------------------------
## ETAPA 1: DESCĂRCAREA DATELOR DIN COPENICUS (Rulată doar dacă fișierul lipsește)
# --------------------------------------------------------------------------------------

def download_data():
    """Descarcă datele de NO2 și Temperatură dacă nu există deja."""
    
    # 1. Descărcarea NO₂ (CAMS Reanalyses)
    if not os.path.exists(NO2_NC_FILE):
        print("\n--- 1. Descărcarea Datelor NO₂ (CAMS) ---")
        request_no2 = {
            "variable": ["nitrogen_dioxide"], "model": ["ensemble"], "level": ["0"], 
            "type": ["validated_reanalysis"], "year": ["2023"], "month": ["06"], 
            "day": [f'{d:02d}' for d in range(1, 31)], 
            "time": ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
            "area": BUCHAREST_AREA, "format": "netcdf"
        }
        try:
            client.retrieve("cams-europe-air-quality-reanalyses", request_no2, NO2_NC_FILE)
            print(f"✅ Fișierul NO₂ salvat ca: {NO2_NC_FILE}")
        except Exception as e:
            print(f"❌ Eroare la descărcarea NO₂. Rulați manual sau verificați parametrii: {e}")
            sys.exit(1)
    else:
        print(f"✅ Fișierul NO₂ ({NO2_NC_FILE}) există. Salt peste descărcare.")

    # 2. Descărcarea Temperaturii (ERA5)
    if not os.path.exists(TEMP_NC_FILE):
        print("\n--- 2. Descărcarea Datelor de Temperatură (ERA5) ---")
        request_temp = {
            'product_type': 'reanalysis', 'format': 'netcdf', 'variable': '2m_temperature',
            'year': '2023', 'month': '06', 
            'day': [f'{d:02d}' for d in range(1, 31)],
            'time': ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
            'area': BUCHAREST_AREA,
        }
        try:
            client.retrieve('reanalysis-era5-single-levels', request_temp, TEMP_NC_FILE)
            print(f"✅ Fișierul de Temperatură salvat ca: {TEMP_NC_FILE}")
        except Exception as e:
            print(f"❌ Eroare la descărcarea Temperaturii. Rulați manual sau verificați parametrii: {e}")
            sys.exit(1)
    else:
        print(f"✅ Fișierul T ({TEMP_NC_FILE}) există. Salt peste descărcare.")
        

# --------------------------------------------------------------------------------------
## ETAPA 2: PRE-PROCESAREA DATELOR NETCDF ȘI CONVERSIE LA TIF
# --------------------------------------------------------------------------------------

def process_netcdf_to_tif(input_nc, output_tif, var_name):
    """Calculează media temporală, re-eșantionează și salvează ca GeoTIFF."""
    if not os.path.exists(input_nc) or not os.path.exists(LANDUSE_PATH):
        print(f"Skipping {output_tif}: fișiere lipsă ({input_nc} sau {LANDUSE_PATH}).")
        return False
        
    print(f"\n--- Procesare Geo-Spațială: {var_name} ---")
    
    if not os.path.exists(LANDUSE_PATH):
        print(f"❌ Eroare fatală: Fișierul Land Use ({LANDUSE_PATH}) nu a fost găsit. Oprire.")
        return False

    # 1. Încărcare și Media Temporală
    # Deschideți fișierul NC (se așteaptă fișierul de 900MB)
    ds = rxr.open_rasterio(input_nc, mask_and_scale=True)
    if 'band' in ds.dims:
        ds = ds.squeeze('band') 
        
    time_dim = 'time'
    if var_name == '2m_temperature' and 'valid_time' in ds.dims:
        time_dim = 'valid_time'
    
    # 2. Calculează media folosind dimensiunea corectă
    mean_data = ds.mean(dim=time_dim) 
    # 🛑 ADAUGAT: Setarea CRS-ului WGS84 (EPSG:4326)
    if mean_data.rio.crs is None:
        mean_data = mean_data.rio.write_crs("EPSG:4326", inplace=True)
        print("CRS setat forțat la EPSG:4326.")
    # 2. Convertirea Unităților (T în Kelvin -> Celsius)
    if var_name == '2m_temperature':
        mean_data = mean_data - 273.15
        print("Unități T: Kelvin -> Celsius.")
    
    # 3. Re-eșantionare la 30m (folosind Land Use ca referință)
    try:
        with rxr.open_rasterio(LANDUSE_PATH) as lu:
            # Re-eșantionăm la aceeași grilă, CRS și rezoluție (30m) ca Land Use
            mean_data = mean_data.rio.reproject_match(lu, resampling=Resampling.average)
            
        # 4. Salvare ca GeoTIFF
        mean_data.rio.to_raster(output_tif, nodata=-9999)
        print(f"✅ {var_name} salvat și re-eșantionat ca: {output_tif}")
        return True
    except Exception as e:
        print(f"❌ Eroare la re-eșantionare/salvare pentru {var_name}: {e}")
        return False


# --------------------------------------------------------------------------------------
## ETAPA 3: GENERAREA SETULUI DE DATE CSV (Agregare pe 1km)
# --------------------------------------------------------------------------------------

def create_training_csv():
    """Citește fișierele TIF și agregă datele pe grile de 1km."""
    if not all(os.path.exists(f) for f in [NO2_TIF_FILE, TEMP_TIF_FILE, LANDUSE_PATH]):
        print("\n❌ Eroare: Nu s-au găsit toate fișierele TIF procesate necesare. Oprire.")
        return False

    print("\n--- 3. Generarea Setului de Date CSV (Agregare pe 1km) ---")
    
    with rasterio.open(LANDUSE_PATH) as src_lu:
        lu_data = src_lu.read(1)
        PIXEL_SIZE = src_lu.profile['transform'][0]
    
    with rasterio.open(NO2_TIF_FILE) as src_no2:
        no2_data = src_no2.read(1)
    
    with rasterio.open(TEMP_TIF_FILE) as src_temp:
        temp_data = src_temp.read(1)

    rows, cols = lu_data.shape
    window_px = int(GRID_SIZE / abs(PIXEL_SIZE)) 

    dataset = []
    
    for r in range(0, rows, window_px):
        for c in range(0, cols, window_px):
            lu_window = lu_data[r:r+window_px, c:c+window_px]
            no2_window = no2_data[r:r+window_px, c:c+window_px]
            temp_window = temp_data[r:r+window_px, c:c+window_px]
            
            if lu_window.shape[0] < window_px or lu_window.shape[1] < window_px:
                continue

            # 1. Agregare NO2 (Ținta)
            valid_no2 = no2_window[no2_window > -9999] 
            mean_no2 = np.mean(valid_no2) if valid_no2.size > 0 else np.nan

            # 2. Agregare Temperatură (Feature)
            valid_temp = temp_window[temp_window > -9999]
            mean_temp = np.mean(valid_temp) if valid_temp.size > 0 else np.nan
            
            if np.isnan(mean_no2) or np.isnan(mean_temp):
                continue
            
            # 3. Agregare Land Use (Features)
            lu_flat = lu_window.flatten()
            lu_flat = lu_flat[lu_flat != 0] 
            
            if lu_flat.size == 0:
                continue

            unique, counts = np.unique(lu_flat, return_counts=True)
            total_pixels = lu_flat.size
            
            row_data = {
                'target_no2': round(mean_no2, 8),
                'temperature': round(mean_temp, 3)
            }
            
            for code, count in zip(unique, counts):
                percent = (count / total_pixels) * 100
                row_data[f"pct_{int(code)}"] = round(percent, 2)
                
            dataset.append(row_data)

    df = pd.DataFrame(dataset).fillna(0)
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    
    print(f"✅ {len(dataset)} înregistrări procesate. Setul de date salvat la: {OUTPUT_CSV_FILE}")
    print("Preview:\n", df.head())
    return True


# --------------------------------------------------------------------------------------
## ETAPA 4: ANTRENAREA MODELULUI NO₂ ÎN CASCADĂ
# --------------------------------------------------------------------------------------

def train_no2_model():
    """Antrenează modelul NO₂ folosind setul de date generat."""
    if not os.path.exists(OUTPUT_CSV_FILE):
        print("\n❌ Eroare: Fișierul CSV de training nu există. Oprire antrenare.")
        return

    print("\n--- 4. Antrenarea Modelului NO₂ (Cascadă) ---")
    data = pd.read_csv(OUTPUT_CSV_FILE)
    
    TARGET_COLUMN = 'target_no2'
    # Features includ Land Use (pct_...) ȘI Temperatura
    features = [col for col in data.columns if col != TARGET_COLUMN]
    target = TARGET_COLUMN

    X = data[features]
    y = data[target]
         
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Antrenare
    model_no2 = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)
    model_no2.fit(X_train, y_train)

    # Evaluare
    y_pred = model_no2.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    
    print(f"✅ Model antrenat. RMSE: {rmse:.8f}")

    # Salvarea Modelului
    joblib.dump(model_no2, MODEL_FILENAME)
    print(f"💾 Model salvat ca: {MODEL_FILENAME}")


# --- RULARE FLUX DE LUCRU PRINCIPAL ---

if __name__ == "__main__":
    
    # 1. Descărcare date (se va executa doar dacă fișierele .nc nu există)
    download_data()
    
    # 2. Conversie .nc -> .tif și Re-eșantionare (creează fișierele .tif)
    no2_ok = process_netcdf_to_tif(NO2_NC_FILE, NO2_TIF_FILE, 'nitrogen_dioxide')
    temp_ok = process_netcdf_to_tif(TEMP_NC_FILE, TEMP_TIF_FILE, '2m_temperature')
    
    if no2_ok and temp_ok:
        # 3. Creare CSV (Agregare)
        if create_training_csv():
            # 4. Antrenare Model
            train_no2_model()
    
    print("\n🎉 Pipeline finalizat!")