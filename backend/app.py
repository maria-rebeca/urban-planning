from flask import Flask
from flask_cors import CORS
from services.gee_service import initialize_gee
from map_routes import api_bp

app = Flask(__name__)
CORS(app)

initialize_gee()

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5000, debug=True)