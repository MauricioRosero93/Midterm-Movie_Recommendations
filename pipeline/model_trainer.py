from surprise import KNNBasic, SVD
import pickle
import time
import os

def train_model(model_type, trainset):
    start_time = time.time()
    
    if model_type == 'knn':
        model = KNNBasic()
    elif model_type == 'svd':
        model = SVD()
    else:
        raise ValueError("Model type not supported")
    
    model.fit(trainset)
    training_time = time.time() - start_time
    
    # Guardar modelo
    model_path = f'models/{model_type}_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    return model, training_time, os.path.getsize(model_path)