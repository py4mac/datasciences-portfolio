# -*- coding: utf-8 -*-
"""

This module is in charge of model management use for customer segmentation.
It provides API to predict class belonging to customer based on his
information.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import os
import pandas as pd
from sklearn.externals import joblib
from sklearn import preprocessing


class Model:
    """Model class definition.
    """

    def __init__(self):
        self.__model = joblib.load(os.path.join('static', 'model.pkl'))
        """__model: Loaded model.
        """
        self.__scaler = joblib.load(os.path.join('static', 'scaler.pkl'))
        """__scaler: Scaling using for transforming input matrix.
        """

    def predict(self, X):
        # Normalize input X frame
        X_norm = self.__scaler.transform(X.reshape(1, -1))
        # Predict X input
        y = self.__model.predict(X_norm)
        return y[0]
