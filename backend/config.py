
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
        11230: {"name": "Discontinuous Very Low Density Urban", "color": "#FD8181"},
        12100: {"name": "Industrial, Commercial, Public, Military and Private units", "color": "#CC4DF2"},
        12210: {"name": "Fast transit Roads", "color": "#771197"}, #adaugat azi
        12220: {"name": "Other Roads and associated land", "color": "#CC4DF2"},
        12230: {"name": "Railways and associated land", "color": "#B77DDD"}, #adaugat azi
        12400: {"name": "Airports", "color": "#9933FF"}, #adaugat azi
        13300: {"name": "Construction Sites", "color": "#e0bb19"},
        13400: {"name": "Land without current use", "color": "#B2B2B2"}, #adaugat azi (apare in tabel)
        14100: {"name": "Green Urban Areas", "color": "#1bd618"},
        14200: {"name": "Sports and Leisure Facilities", "color": "#74D7D7"},
        21000: {"name": "Arable land", "color": "#FFFFA8"},
        22000: {"name": "Permanent crops", "color": "#FFD700"},
        23000: {"name": "Pastures", "color": "#FFEA00"},
        24000: {"name": "Complex and mixed cultivations", "color": "#FFE066"},
        31000: {"name": "Forests", "color": "#4dff00"},
        32000: {"name": "Scrub and/or Herbaceous vegetation associations", "color": "#66ff66"},
        33000: {"name": "Open spaces with little or no vegetation", "color": "#99ff99"},
        40000: {"name": "Wetlands", "color": "#0099FF"},
        50000: {"name": "Water Bodies", "color": "#00baf3"},
        91000: {"name": "No data (Clouds and shadows)", "color": "#42678D"}, #optional since we don't have them in the .csv
        92000: {"name": "No data (Outside EU)", "color": "#42678D"}          #optional
    }