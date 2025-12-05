
import os

class Config:
    SERVICE_ACCOUNT = 'gee-backend@engaged-kite-443917-f9.iam.gserviceaccount.com'
    KEY_FILE = 'service-account.json'


    LST_IMAGE_ID = 'users/filippintea/LST_Summer_Median1'
    LAND_USE_RASTER_ID = 'users/filippintea/land_use_raster'
    
    # Constants
    LAND_USE_MAP = {
        11100: {"name": "Continuous Urban Fabric", "color": "#E60000"},
        11210: {"name": "Discontinuous Dense Urban Fabric", "color": "#FF0000"},
        11220: {"name": "Discontinuous Medium Urban Fabric", "color": "#FF4D4D"},
        11230: {"name": "Discontinuous Low Density Urban", "color": "#FE6161"},
        11240: {"name": "Discontinuous Very Low Density Urban", "color": "#FD8181"},
        12100: {"name": "Industrial, Commercial, Public", "color": "#CC4DF2"},
        12220: {"name": "Road and Rail Networks", "color": "#CC4DF2"},
        13300: {"name": "Construction Sites", "color": "#e0bb19"},
        14100: {"name": "Green Urban Areas", "color": "#1bd618"},
        14200: {"name": "Sports and Leisure Facilities", "color": "#FFA6FF"},
        20000: {"name": "Agricultural + Semi-natural", "color": "#FFFFA8"},
        30000: {"name": "Forests", "color": "#4dff00"},
        50000: {"name": "Water Bodies", "color": "#00baf3"}
    }