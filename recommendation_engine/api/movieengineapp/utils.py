# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import Normalizer, scale
import json
from difflib import SequenceMatcher
from sklearn.neighbors import NearestNeighbors

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

class MovieEngine:

    __criteria_selection = ['color', 'director_name','actor_2_name', 'actor_1_name', 'actor_3_name',
                      'content_rating', 'budget', 'title_year', 'imdb_score', 'english_lang', 'french_lang', 'spanish_lang',
                      'other_lang', 'Action', 'Adventure', 'Fantasy', 'Sci-Fi', 'Thriller', 'Romance', 'Animation', 'Comedy', 
                      'Family', 'Musical', 'Mystery', 'Western', 'Drama', 'History', 'Sport', 'Crime', 'Horror', 'War', 'Biography', 
                      'Music', 'Documentary', 'Film-Noir']

    def __init__(self):
        self.df = pd.read_csv(os.path.join('movieengineapp', 'static', 'movies.csv'), sep=',')
        self.list_film = json.loads(self.df['movie_title'].to_json(orient='records'))

    def getListFilm(self):
        return self.list_film

    def getListFilmWithIndex(self):
        return [dict(id=i, name=self.list_film[i]) for i in range(len(self.list_film))]

    def getListFilmIndex(self, film):
        return self.list_film.index(film)

    def lookSimilarById(self, index, sequel):
        title = self.df.iloc[index].movie_title
        col = list(self.df.columns)
        col.pop()
        X_norm = scale(self.df[col])
        X_norm_ponderate = self.__ponderate(X_norm, self.__get_pond1_weights())
        film_selection = self.__recommand(X_norm_ponderate, self.df, index)
        if (sequel):
            film_selection = self.__del_sequels(film_selection)
        return [dict(id=self.__find_entry(self.df, film), name=film) for film in film_selection[:5]]

    def lookSimilarByTitle(self, title, sequel):
        index = self.__find_entry(self.df, title)
        col = list(self.df.columns)
        col.pop()
        X_norm = scale(self.df[col])
        X_norm_ponderate = self.__ponderate(X_norm, self.__get_pond1_weights())
        film_selection = self.__recommand(X_norm_ponderate, self.df, index)
        if sequel:
            film_selection = self.__del_sequels(film_selection)
        return [dict(id=self.__find_entry(self.df, film), name=film) for film in film_selection[:5]]

    # _________________________ PRIVATE FUNCTIONS _____________________________
    # Keep color, actor_1_name, country, imdb_score, xxx_lang, genres
    # Give highest priority to genres
    def __get_pond1_weights(self):
        #        ['color','director_name', 'duration', 'actor_2_name', 'actor_1_name', 'actor_3_name', 'country', 
        return   [ 1, 0, 0, 0, 1, 0, 1,
        #        'content_rating', 'budget', 'title_year', 'imdb_score', 'english_lang', 'french_lang', 'spanish_lang',
                0, 0, 0, 0, 1, 1, 1,
        #        'other_lang', 'Action', 'Adventure', 'Fantasy', 'Sci-Fi', 'Thriller', 'Romance', 'Animation', 'Comedy', 
                1, 1, 1, 1, 1, 1, 1, 1, 1,
        #        'Family', 'Musical', 'Mystery', 'Western', 'Drama', 'History', 'Sport', 'Crime', 'Horror', 'War', 'Biography', 
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #        'Music', 'Documentary', 'Film-Noir']
                1, 1, 1]

    def __ponderate(self, x, matrix):
        z = np.copy(x)
        for i in range(len(self.__criteria_selection)):
            z[:,i] *= matrix[i]
        return z

    def __similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def __sequel(self, titre1, titre2):
        if (self.__similar(titre1, titre2) > 0.6):
            return True
        else:
            return False

    def __del_sequels(self, film_list):  
        # First element is considered with higher priority
        keeped = []
        removed = []
        for film_1 in enumerate(film_list):
            keeped.append(film_1[1])
            for film_2 in enumerate(film_list):
                if (film_1[1] != film_2[1]):
                    if self.__sequel(film_1[1], film_2[1]) and (not film_2[1] in keeped): 
                        removed.append(film_2[1])

        film_list = [film for film in film_list if film not in removed]

        return film_list

    def __find_entry(self, df, titre):
        index =  df[df.movie_title == titre].index
        if (len(index) == 0):
            return -1
        else:
            return index[0]
    
    def __recommand(self, x, df, id_entry):
        nbrs = NearestNeighbors(n_neighbors=20, algorithm='auto', metric='euclidean').fit(x)
        X_test = x[id_entry,:].reshape(1, -1)
        distances, indices = nbrs.kneighbors(X_test)
        list_films = []
        for i in range(1, 20):
            list_films.append(df.get_value(indices[0][i], 'movie_title'))
        return list_films