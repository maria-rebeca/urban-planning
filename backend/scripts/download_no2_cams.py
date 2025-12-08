import cdsapi
import os
import sys

# --- CONFIGURARE ---
# Coordonatele pentru București: [lat_max, lon_min, lat_min, lon_max]
BUCHAREST_AREA = [44.61, 25.86, 44.23, 26.46]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Numele fișierului pe care scriptul complet îl așteaptă:
NO2_NC_FILE = os.path.join(BASE_DIR, "no2_cams_data.nc") 

try:
    client = cdsapi.Client()
except Exception as e:
    print(f"❌ Eroare la inițializarea CDSAPI: {e}")
    sys.exit(1)

# --- CEREREA DE DATE (NO₂) ---
print(f"🚀 Pornire descărcare NO₂ (CAMS) pentru zona: {BUCHAREST_AREA}...")

# 🛑 NOTĂ: Folosim 'cams-europe-air-quality-forecasts' ca soluție de ocolire pentru eroarea 404
dataset = "cams-europe-air-quality-forecasts" 

request_no2 = {
    "variable": ["nitrogen_dioxide"], 
    "model": ["ensemble"], 
    "level": ["0"], 
    "type": ["validated_reanalysis"], # Specificăm că vrem date de reanaliză
    "year": ["2023"], 
    "month": ["06"], 
    "day": [
        '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'
    ], 
    "time": [
        '00:00', '03:00', '06:00', '09:00', 
        '12:00', '15:00', '18:00', '21:00'
    ],
    "area": BUCHAREST_AREA, 
    "format": "netcdf"
}

try:
    client.retrieve(dataset, request_no2, NO2_NC_FILE)
    print(f"✅ Descărcare finalizată! Fișierul NO₂ a fost salvat ca: {NO2_NC_FILE}")
except Exception as e:
    print(f"❌ Eroare la descărcarea NO₂. Verificați conexiunea sau parametri: {e}")