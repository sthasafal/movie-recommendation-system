import pandas as pd
from recommenders.utils.paths import FINAL_MOVIES, FINAL_RATINGS


def load_data():
    movies = pd.read_csv(FINAL_MOVIES)
    ratings = pd.read_csv(FINAL_RATINGS)
    return movies, ratings


def create_user_movie_matrix(ratings):
    matrix = ratings.pivot_table(
        index="user_id",
        columns="movie_id",
        values="rating"
    )
    return matrix
