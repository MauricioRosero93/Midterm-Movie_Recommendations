from surprise.model_selection import train_test_split
from data_loader import load_data
from model_trainer import train_model
from evaluator import evaluate_model
import pickle

def run_pipeline():
    # Cargar datos
    data, movies = load_data()
    trainset, testset = train_test_split(data, test_size=0.2)
    
    # Entrenar modelos
    knn_model, knn_time, knn_size = train_model('knn', trainset)
    svd_model, svd_time, svd_size = train_model('svd', trainset)
    
    # Evaluar modelos
    knn_rmse, knn_inf_time = evaluate_model(knn_model, testset)
    svd_rmse, svd_inf_time = evaluate_model(svd_model, testset)
    
    # Guardar resultados
    results = {
        'knn': {
            'rmse': knn_rmse,
            'training_time': knn_time,
            'inference_time': knn_inf_time,
            'model_size': knn_size
        },
        'svd': {
            'rmse': svd_rmse,
            'training_time': svd_time,
            'inference_time': svd_inf_time,
            'model_size': svd_size
        }
    }
    
    with open('models/results.pkl', 'wb') as f:
        pickle.dump(results, f)
    
    return results

if __name__ == '__main__':
    run_pipeline()