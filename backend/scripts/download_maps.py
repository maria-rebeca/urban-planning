import sys
import os
import requests
import ee

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config import Config

try:
    credentials = ee.ServiceAccountCredentials(Config.SERVICE_ACCOUNT, Config.KEY_FILE)
    ee.Initialize(credentials)
except Exception as e:
    print(f"❌ Init Failed: {e}")
    sys.exit(1)

# 1. Setup - Bucharest Center
CITY_CENTER = [26.096306, 44.439663]
print(f"📍 Target: {CITY_CENTER}")

# 2. Define a strict 20km box (Meters)
# We use EPSG:3857 (Web Mercator) so our 30m scale is accurate
PROJ = 'EPSG:3857'
point = ee.Geometry.Point(CITY_CENTER)
region = point.buffer(10000).bounds() # 20km box

# 3. Load Images
# Unmask ensures we get data even if there are small holes
lst = ee.Image(Config.LST_IMAGE_ID).select('LST_final').unmask(-999)
lu = ee.Image(Config.LAND_USE_RASTER_ID).select('landuse_code').unmask(0)

# 4. Download Function
def download_tif(image, filename):
    print(f"⏳ Downloading {filename}...")
    url = image.getDownloadURL({
        'name': filename,
        'scale': 30, # 30 meters per pixel
        'crs': PROJ, # Force alignment
        'region': region,
        'format': 'GEO_TIFF'
    })
    response = requests.get(url)
    with open(os.path.join(current_dir, filename), 'wb') as f:
        f.write(response.content)
    print(f"✅ Saved {filename}")

# 5. Execute
download_tif(lst, 'lst.tif')
download_tif(lu, 'landuse.tif')

print("\n🎉 Done! You now have 'lst.tif' and 'landuse.tif'.")