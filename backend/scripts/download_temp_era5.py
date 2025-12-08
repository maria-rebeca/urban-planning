import cdsapi
import os

# --- CONFIGURARE ---
BUCHAREST_AREA = [44.61, 25.86, 44.23, 26.46]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_NC_FILE = os.path.join(BASE_DIR, "temp_era5_data.nc") 

client = cdsapi.Client()

# --- CEREREA DE DATE (TEMPERATURĂ ERA5) ---
print(f"🚀 Pornire descărcare Temperatură (ERA5)...")

client.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis', 'format': 'netcdf', 'variable': '2m_temperature',
        'year': '2023', 'month': '06', 
        'day': [f'{d:02d}' for d in range(1, 31)], 
        'time': ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
        'area': BUCHAREST_AREA,
    },
    TEMP_NC_FILE
)

print(f"✅ Descărcare finalizată! Fișierul de temperatură a fost salvat ca: {TEMP_NC_FILE}")