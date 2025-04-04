import unittest
import os
from surprise import Dataset
from surprise.model_selection import train_test_split
from pipeline.model_trainer import train_model
import pandas as pd

class TestModelTrainer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Datos de prueba
        ratings = pd.DataFrame({
            'userId': [1, 1, 2, 2],
            'movieId': [1, 2, 1, 2],
            'rating': [4, 3, 5, 2]
        })
        reader = Reader(rating_scale=(1, 5))
        cls.data = Dataset.load_from_df(ratings, reader)
        cls.trainset, _ = train_test_split(cls.data, test_size=0.2)
    
    def test_train_knn(self):
        model, time, size = train_model('knn', self.trainset)
        self.assertIsNotNone(model)
        self.assertGreater(time, 0)
        self.assertGreater(size, 0)
        self.assertTrue(os.path.exists('models/knn_model.pkl'))
    
    def test_train_svd(self):
        model, time, size = train_model('svd', self.trainset)
        self.assertIsNotNone(model)
        self.assertGreater(time, 0)
        self.assertGreater(size, 0)
        self.assertTrue(os.path.exists('models/svd_model.pkl'))

if __name__ == '__main__':
    unittest.main()