from flask import Flask, jsonify, request
import pickle
import pandas as pd
import sqlite3
import time
from datetime import datetime

# Configuración de la base de datos para telemetría
def init_db():
    conn = sqlite3.connect('monitoring/recommendations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
                 (timestamp TEXT, user_id INTEGER, model_version TEXT, response_time REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ratings
                 (timestamp TEXT, user_id INTEGER, movie_id INTEGER, rating INTEGER)''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

# Cargar modelo
with open('models/svd_model.pkl', 'rb') as f:
    model = pickle.load(f)
model_version = "svd_v1"

movies = pd.read_csv('data/movies.csv')

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    start_time = time.time()
    
    # Generar recomendaciones
    all_movies = movies['movieId'].unique()
    predictions = [model.predict(user_id, movie_id) for movie_id in all_movies[:100]]  # Limitado para demo
    top_movies = sorted(predictions, key=lambda x: x.est, reverse=True)[:20]
    recommendations = [int(pred.iid) for pred in top_movies]
    
    # Registrar telemetría
    response_time = time.time() - start_time
    log_recommendation(user_id, response_time)
    
    return jsonify(recommendations)

def log_recommendation(user_id, response_time):
    conn = sqlite3.connect('monitoring/recommendations.db')
    c = conn.cursor()
    c.execute("INSERT INTO recommendations VALUES (?, ?, ?, ?)",
              (datetime.now().isoformat(), user_id, model_version, response_time))
    conn.commit()
    conn.close()

@app.route('/rate/<int:movie_id>=<int:rating>', methods=['GET'])
def rate_movie(movie_id, rating):
    user_id = request.args.get('user_id', type=int)
    if user_id:
        log_rating(user_id, movie_id, rating)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "user_id required"}), 400

def log_rating(user_id, movie_id, rating):
    conn = sqlite3.connect('monitoring/ratings.db')
    c = conn.cursor()
    c.execute("INSERT INTO ratings VALUES (?, ?, ?, ?)",
              (datetime.now().isoformat(), user_id, movie_id, rating))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)