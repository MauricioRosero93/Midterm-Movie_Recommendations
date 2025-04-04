from surprise import accuracy
import time

def evaluate_model(model, testset):
    # Evaluación offline
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    
    # Medir tiempo de inferencia
    start_time = time.time()
    for _ in range(1000):
        model.predict(testset[0][0], testset[0][1])
    inference_time = (time.time() - start_time) / 1000
    
    return rmse, inference_time