# -*- coding: utf-8 -*-
"""Customer Segmentation Prediction example.

Example:
    The way to use the API is the following::

        $ python main.py [OPTIONS] csv_path

    Some example input patterns can be used to test the model for each one of
    the 4 classes (cold, discrete, loyal and gold):

        test_cold.csv
        test_discrete.csv
        test_loyal.csv
        test_gold.csv

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import sys
import logging
import argparse
from optparse import OptionParser
import pandas as pd
from sklearn import preprocessing
import numpy as np
from customer import Category
from model import Model

cat_object = Category()
"""cat_object: Category Class Object.

Instance of Category Class
"""
model_object = Model()
"""model_object: Model Class Object.

model_object of Model Class
"""


def load_csv(csv_path):
    """Function loading input CSV file containing temporal sequence for a customer.

    Args:
        csv_path (str): The first parameter.

    Returns:
        df: The return loaded dataframe. df for success, None otherwise.
    """
    df = pd.read_csv(csv_path, sep='\t')
    expected_column_name = ['InvoiceNo',
                            'StockCode',
                            'Description',
                            'Quantity',
                            'InvoiceDate',
                            'UnitPrice',
                            'CustomerID',
                            'Country']
    # Check if input csv file is correctly formated
    if (df.columns == expected_column_name).all():
        return df
    else:
        return None


def dataframe_segmentedDataframe(df):
    """Function creating a segmented DataFrame based on the input
    dataframe df.

    Args:
        df (DataFrame): The first parameter.

    Returns:
        df: The return Segmented Customer dataframe.
    """
    column = ['day_0', 'day_1', 'day_2', 'day_3',
              'day_4', 'day_5', 'day_6', 'qty_mean', 'qty_min',
              'qty_max', 'unitprice_mean', 'unitprice_max',
              'unitprice_min', 'totalprice_mean', 'totalprice_max',
              'totalprice_min']
    segmented_customer = np.zeros(len(column))
    # Fill day of week fields
    date_lst = pd.to_datetime(df['InvoiceDate'].unique().tolist())
    weekday_lst = pd.to_datetime(date_lst).weekday.tolist()
    for day in weekday_lst:
        segmented_customer[column.index('day_0') + day] = 1
    # Fill quantity fields
    segmented_customer[column.index('qty_mean')] = df.Quantity.mean()
    segmented_customer[column.index('qty_min')] = df.Quantity.min()
    segmented_customer[column.index('qty_max')] = df.Quantity.max()
    # Fill unit price fields
    segmented_customer[column.index('unitprice_mean')] = df.UnitPrice.mean()
    segmented_customer[column.index('unitprice_max')] = df.UnitPrice.min()
    segmented_customer[column.index('unitprice_min')] = df.UnitPrice.max()
    # Fill total price fields
    segmented_customer[column.index('totalprice_mean')] = df.TotalPrice.mean()
    segmented_customer[column.index('totalprice_max')] = df.TotalPrice.min()
    segmented_customer[column.index('totalprice_min')] = df.TotalPrice.max()
    return segmented_customer


def dataframe_featureEngineering(df):
    """Function adding features QuantityCanceled/TotalPrice column to the input
    dataframe df.

    Args:
        df (DataFrame): The first parameter.

    Returns:
        df: The return loaded dataframe with features added.

    """
    df_copy = df.copy(deep=True)
    df_copy['QuantityCanceled'] = 0
    entry_with_cancelation = []
    entry_without_cancelation = []

    for index, col in df.iterrows():
        if (col['Quantity'] > 0):
            continue
        df_test = df[(df['CustomerID'] == col['CustomerID']) &
                     (df['StockCode'] == col['StockCode']) &
                     (df['InvoiceDate'] < col['InvoiceDate']) &
                     (df['Quantity'] > 0)].copy()
        if (df_test.shape[0] == 0):
            entry_without_cancelation.append(index)
        elif (df_test.shape[0] == 1):
            entry_with_cancelation.append(index)
            df_copy.QuantityCanceled.loc[df_test.index[0]] = -col['Quantity']
        else:
            df_test = df_test.sort_values('InvoiceDate')
            for ind, val in df_test.iterrows():
                if val['Quantity'] < -col['Quantity']:
                    continue
                df_copy.QuantityCanceled.loc[ind] = -col['Quantity']
                entry_with_cancelation.append(index)
                break
    # Remove order with cancelation
    df_copy.drop(entry_with_cancelation, axis=0, inplace=True)
    # Remove order without cancelation
    df_copy.drop(entry_without_cancelation, axis=0, inplace=True)
    # Create TotalPrice column
    df_copy['TotalPrice'] = (df_copy['Quantity'] - df_copy['QuantityCanceled'])
    df_copy['TotalPrice'] = df_copy['TotalPrice'] * df_copy['UnitPrice']
    return df_copy


def dataframe_cleaning(df):
    """Function loading input CSV file containing temporal sequence for a customer.

    Args:
        df (DataFrame): The first parameter.

    Returns:
        df: The return loaded dataframe. df for success, None otherwise.

    """
    # Import InvoiceDate as datetime first
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    # Remove entry with undefined 'CustomerID'
    df.dropna(subset=['CustomerID'], how='all', inplace=True)
    # Remove duplicate entry
    df.drop_duplicates(inplace=True)
    # Remove description field
    del df['Description']
    # Manage Country encoding
    del df['Country']
    return df


if __name__ == '__main__':
    """Main program entry.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=str,
                        help="CSV Path File")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")

    args = parser.parse_args()

    log_level = logging.WARNING
    if (args.verbose):
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    logging.debug(args.csv_path)

    # Open and Import CSV File
    logging.debug("Importing CSV File...")
    df = load_csv(args.csv_path)
    if df is None:
        logging.error("Error while importing CSV file.")
        sys.exit(1)

    # Clean dataframe
    df = dataframe_cleaning(df)

    # Create additional feature
    df = dataframe_featureEngineering(df)

    # Create segmented dataframe
    X = dataframe_segmentedDataframe(df)

    # Predict customer class
    customer_class = model_object.predict(X)

    # Convert predicted customer class into 'real class name'
    customer_class = cat_object.get_name(customer_class)

    logging.warning("Customer class prediction: " + str(customer_class))
