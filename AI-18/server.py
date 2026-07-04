# flask_server.py
from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('heatmap.html')  # heatmap template

@app.route('/crowd-data')
def crowd_data():
    base_lat = 17.4065
    base_lon = 78.5504
    points = []
    for _ in range(random.randint(10, 20)):
        lat = base_lat + random.uniform(-0.0005, 0.0005)
        lon = base_lon + random.uniform(-0.0005, 0.0005)
        points.append([lat, lon])
    return jsonify(points)

if __name__ == '__main__':
    app.run(port=5001, debug=True)   # <--- Important: Different port (5001)
