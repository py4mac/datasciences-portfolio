from __future__ import division
import pandas as pd

def display_dataframe_stats(df):
	my_df = pd.DataFrame(columns = df.columns)
	# types of column
	my_df.loc[len(my_df)] = df.dtypes
	my_df = my_df.rename(index={0:'type'})
	# number of unique values
	my_df.loc[len(my_df)] = df.nunique()
	my_df = my_df.rename(index={1:'number of unique values'})
	# missing values
	my_df.loc[len(my_df)] = df.isnull().sum()
	my_df = my_df.rename(index={2:'number of missing values'})
	# % of missing values
	my_df.loc[len(my_df)] = (df.isnull().sum() / df.shape[0]) * 100
	my_df = my_df.rename(index={3:'% of missing values'})
	return my_df