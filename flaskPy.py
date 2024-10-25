from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trip.db'
db = SQLAlchemy(app)

# Google Maps API key
GOOGLE_API_KEY = 'AIzaSyBlajbPhDYoKEiz0lkhXRjFdj-IIS2eNRs'

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    locations = db.Column(db.Text, nullable=False)

# 手動初始化資料庫
def create_tables():
    with app.app_context():
        db.create_all()

# 儲存行程
@app.route('/save_trip', methods=['POST'])
def save_trip():
    data = request.json
    trip = Trip(name=data['name'], locations=json.dumps(data['locations']))
    db.session.add(trip)
    db.session.commit()
    return jsonify({"message": "Trip saved successfully"}), 201

# 規劃行程
@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    data = request.json
    locations = data['locations']
    travel_mode = data.get('travel_mode', 'driving')

    # 建立 Directions API 請求
    waypoints = '|'.join([f"{loc['lat']},{loc['lng']}" for loc in locations[1:-1]])
    origin = f"{locations[0]['lat']},{locations[0]['lng']}"
    destination = f"{locations[-1]['lat']},{locations[-1]['lng']}"

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&mode={travel_mode}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    route_data = response.json()

    if 'routes' in route_data:
        return jsonify(route_data)
    else:
        return jsonify({"error": "Failed to plan trip"}), 500

if __name__ == '__main__':
    create_tables()  # 啟動應用程式時初始化資料庫
    app.run(debug=True)

#GOOGLE_API_KEY ='AIzaSyBlajbPhDYoKEiz0lkhXRjFdj-IIS2eNRs'