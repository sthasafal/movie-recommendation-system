import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from recommenders.utils.paths import FINAL_MOVIES, FINAL_RATINGS


def load_data():
    """Load the processed movies and ratings datasets."""
    movies = pd.read_csv(
        FINAL_MOVIES,
        low_memory=False,
        dtype={
            "poster_path": "string",
            "overview": "string",
        },
    )
    ratings = pd.read_csv(FINAL_RATINGS)
    return movies, ratings


def create_user_movie_matrix(ratings: pd.DataFrame) -> pd.DataFrame:
    """
    Build a sparse user-movie ratings matrix without materializing a huge
    dense pivot. Missing ratings are represented as NaN via SparseDtype.
    """
    user_cat = ratings["user_id"].astype("category")
    movie_cat = ratings["movie_id"].astype("category")

    user_idx = user_cat.cat.codes.to_numpy()
    movie_idx = movie_cat.cat.codes.to_numpy()
    values = ratings["rating"].to_numpy()

    sparse_matrix = csr_matrix(
        (values, (user_idx, movie_idx)),
        shape=(user_cat.cat.categories.size, movie_cat.cat.categories.size),
        dtype=np.float32,
    )

    matrix_df = pd.DataFrame.sparse.from_spmatrix(
        sparse_matrix,
        index=user_cat.cat.categories.to_numpy(),
        columns=movie_cat.cat.categories.to_numpy(),
    ).astype(pd.SparseDtype("float", np.nan))

    return matrix_df
