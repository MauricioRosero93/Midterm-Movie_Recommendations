import pandas as pd
import numpy as np
from datetime import datetime

def check_data_quality():
    issues = []
    
    # Cargar datos
    try:
        ratings = pd.read_csv('data/ratings.csv')
        movies = pd.read_csv('data/movies.csv')
    except Exception as e:
        issues.append(f"Error loading data: {str(e)}")
        return issues
    
    # 1. Verificar esquema
    required_rating_cols = {'userId', 'movieId', 'rating', 'timestamp'}
    if not required_rating_cols.issubset(set(ratings.columns)):
        issues.append("Ratings data schema mismatch")
    
    required_movie_cols = {'movieId', 'title', 'genres'}
    if not required_movie_cols.issubset(set(movies.columns)):
        issues.append("Movies data schema mismatch")
    
    # 2. Verificar valores faltantes
    if ratings.isnull().any().any():
        issues.append("Missing values in ratings data")
    
    if movies.isnull().any().any():
        issues.append("Missing values in movies data")
    
    # 3. Verificar rangos de ratings
    if not ratings['rating'].between(0.5, 5).all():
        issues.append("Invalid rating values (out of 0.5-5 range)")
    
    # 4. Verificar drift (comparar con datos históricos)
    # Esto es un ejemplo simple - en producción usarías datos históricos reales
    avg_rating = ratings['rating'].mean()
    if avg_rating < 2.5 or avg_rating > 4.5:  # Umbrales arbitrarios
        issues.append(f"Possible rating drift - average rating is {avg_rating:.2f}")
    
    return issues

if __name__ == '__main__':
    issues = check_data_quality()
    if issues:
        print("Data quality issues found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No data quality issues found")