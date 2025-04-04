import sqlite3
import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np

def calculate_online_metrics():
    # Conectar a la base de datos
    conn = sqlite3.connect('monitoring/recommendations.db')
    
    # 1. Métricas del servicio
    service_metrics = {}
    
    # Tiempo de respuesta promedio
    df_resp = pd.read_sql("SELECT response_time FROM recommendations", conn)
    service_metrics['avg_response_time'] = df_resp['response_time'].mean()
    
    # 2. Métricas del modelo (si hay ratings)
    try:
        df_ratings = pd.read_sql("SELECT user_id, movie_id, rating FROM ratings", conn)
        if not df_ratings.empty:
            # Aquí podrías implementar una métrica más sofisticada
            # Esto es solo un ejemplo simple
            avg_rating = df_ratings['rating'].mean()
            service_metrics['avg_user_rating'] = avg_rating
    except:
        pass
    
    conn.close()
    
    return service_metrics

if __name__ == '__main__':
    metrics = calculate_online_metrics()
    print("Online Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")