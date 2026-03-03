from flask import Blueprint, jsonify, request
from services.gee_service import get_lst_mapid, get_landuse_mapid, calculate_stats
from config import Config
from services.ai_service import ai_service

api_bp = Blueprint('api', __name__)

@api_bp.route('/get-LST')
def route_get_lst():
    try:
        data = get_lst_mapid()
        return jsonify({'mapid': data['mapid'], 'token': data['token']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/get-landuse-tiles')
def route_get_landuse():
    try:
        data = get_landuse_mapid()
        return jsonify({'mapid': data['mapid'], 'token': data['token']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/get-stats')
def route_get_stats():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        results = calculate_stats(lat, lng)
        return jsonify({
            'mean_temp': results[0],
            'land_use_dist': results[1]
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/predict-temperature', methods=['POST'])
def route_predict():
    try:
        data = request.get_json()
        distribution = data.get('distribution', {})

        if not distribution:
            return jsonify({"error": "No distribution provided"}), 400

        # Mapează distribuția în formatul 'pct_CODE' de care are nevoie ai_service
        mapped_distribution = {f"pct_{k}": v for k, v in distribution.items()}

        # 1. Predicția de Temperatură
        predicted_temp = ai_service.predict_temperature(mapped_distribution)
        
        # 2. Predicția de Poluare
        predicted_pollution = ai_service.predict_pollution(mapped_distribution)

        return jsonify({
            "status": "success",
            "predicted_temp": predicted_temp,
            "predicted_pollution": predicted_pollution  # NOU: Inclusă Poluarea
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500