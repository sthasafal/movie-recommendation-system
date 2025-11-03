import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # corrected import
import os

ratings = pd.read_csv(
    'Backend/data/u.data', 
    sep='\t', 
    names=["user_id", "movie_id", "rating", "timestamp"])

columns = ["movie_id", "title", "release_date", "IMDb_URL"]
movies = pd.read_csv(
    'Backend/data/u.item',
    sep='|',
    encoding='latin-1',
    names=columns,
    usecols=[0, 1, 2, 4],

    header=None
)
print(ratings.head())
print(movies.head())


data = pd.merge(ratings, movies, on="movie_id")
print(data.head())
