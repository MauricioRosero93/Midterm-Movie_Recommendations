import unittest
import pandas as pd
from pipeline.data_loader import load_data

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data, movies = load_data()
        
        # Verificar que los datos se cargan correctamente
        self.assertIsNotNone(data)
        self.assertIsInstance(movies, pd.DataFrame)
        self.assertTrue('title' in movies.columns)
        
if __name__ == '__main__':
    unittest.main()