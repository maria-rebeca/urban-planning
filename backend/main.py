import ee
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    service_account = 'gee-backend@engaged-kite-443917-f9.iam.gserviceaccount.com'
    key_file = 'service-account.json'  

    credentials = ee.ServiceAccountCredentials(service_account, key_file)
    ee.Initialize(credentials)
    print("Gee initialized")
except Exception as e:
    print(f"Error:{e}")


@app.route('/api/get-stats')
def get_stats():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        point = ee.Geometry.Point(lng, lat)
        region = point.buffer(1000)
        
        image = ee.Image('users/filippintea/LST_Summer_Median1')
        stats_img = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=30,
            maxPixels=1e9
        )
        mean_temp = stats_img.get('LST_final').getInfo()
        return jsonify({'mean_temp': mean_temp})
        
    except Exception as e:
        print(f"Error getting stats:{e}")
        return jsonify({"error":str(e)}), 500
        

@app.route('/api/get-LST')
def get_LST():
    try:
        lst = ee.Image('users/filippintea/LST_Summer_Median1')
        vis = {
            'min': 20,
            'max': 45,
            'palette': ['blue', 'yellow', 'red']
        }

        mapid_dict = lst.getMapId(vis)
        return jsonify({'mapid': mapid_dict['mapid'],
                        'token': mapid_dict['token']})
    except Exception as e:
        print(f"Error getting MapID: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
