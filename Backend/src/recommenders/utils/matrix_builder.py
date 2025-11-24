import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

FINAL_MOVIES = os.path.join(PROCESSED_DIR, "final_movies.csv")
FINAL_RATINGS = os.path.join(PROCESSED_DIR, "final_ratings.csv")


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
