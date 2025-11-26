import ee
from config import Config

def initialize_gee():
    try:
        service_account = 'gee-backend@engaged-kite-443917-f9.iam.gserviceaccount.com'
        key_file = 'service-account.json'  

        credentials = ee.ServiceAccountCredentials(service_account, key_file)
        ee.Initialize(credentials)
        print("Gee initialized")
    except Exception as e:
        print(f"Error:{e}")

def get_lst_mapid():
    lst = ee.Image(Config.LST_IMAGE_ID)
    vis = {
            'min': 20,
            'max': 45,
            'palette': ['blue', 'yellow', 'red']
    }
    return  lst.getMapId(vis)

def get_landuse_mapid():
    lu = ee.Image(Config.LAND_USE_RASTER_ID)
    original_codes = [11100, 14100, 13300, 50000] 
    mapped_values  = [0,     1,     2,     3]
    palette = [
        'E60000', # 0: Urban Fabric (Red)
        '1bd618', # 1: Green Urban Areas (Green)
        'e0bb19', # 2: Construction (Yellow)
        '00baf3'  # 3: Water (Blue)
    ]
        
    remapped_image = lu.remap(original_codes, mapped_values)
    
    vis = {
        'min': 0,
        'max': 3,
        'palette' : palette
    }
    return remapped_image.getMapId(vis)

def calculate_stats(lat, lng):
    point = ee.Geometry.Point(lng, lat)
    region = point.buffer(1000)
    
    lst_image = ee.Image(Config.LST_IMAGE_ID)
    urban_image = ee.Image(Config.LAND_USE_RASTER_ID).unmask()
    
    urban_stats = urban_image.reduceRegion(
        reducer= ee.Reducer.frequencyHistogram().unweighted(),
        geometry=region,
        scale=30,
        maxPixels=1e9
    )

    lst_stats_img = lst_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=30,
        maxPixels=1e9
    )
    mean_temp = lst_stats_img.get('LST_final').getInfo()
    histogram = urban_stats.get('landuse_code').getInfo()
    
    distribution = []
    total_pixels = sum(histogram.values())
    
    for type in histogram:
        code = int(float(type))
        if code in Config.LAND_USE_MAP:
            percentage = histogram[type] / total_pixels * 100
            distribution.append({Config.LAND_USE_MAP[code]['name']: round(percentage, 1)})
    return (mean_temp, distribution)