import unittest
from surprise import Dataset, KNNBasic
from surprise.model_selection import train_test_split
import pandas as pd
from pipeline.evaluator import evaluate_model

class TestEvaluator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Datos de prueba
        ratings = pd.DataFrame({
            'userId': [1, 1, 2, 2, 3, 3],
            'movieId': [1, 2, 1, 2, 1, 2],
            'rating': [4, 3, 5, 2, 3, 4]
        })
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings, reader)
        cls.trainset, cls.testset = train_test_split(data, test_size=0.2)
        cls.model = KNNBasic()
        cls.model.fit(cls.trainset)
    
    def test_evaluate_model(self):
        rmse, inf_time = evaluate_model(self.model, self.testset)
        self.assertIsInstance(rmse, float)
        self.assertGreater(rmse, 0)
        self.assertGreater(inf_time, 0)

if __name__ == '__main__':
    unittest.main()