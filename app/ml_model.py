import numpy as np
import pandas as pd
from .movie_rec import rec_films

class RecommendModel:
    def __init__(self):
        self.data = pd.read_csv('film_vietnamese.csv')
        print('Load recommend data: Done!')

    def predict(self, film_id_list, genre_count_vector):
        return rec_films(self.data, film_id_list, genre_count_vector)