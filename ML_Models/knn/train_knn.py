import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

from ML_Models.utils.shared_paths import FINAL_RATINGS, KNN_DIR

KNN_DIR.mkdir(parents=True, exist_ok=True)


def build_matrix(df):
    pivot = df.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
    return pivot.values, pivot.index.to_numpy(), pivot.columns.to_numpy()


def train_knn():
    print("Loading rating data...")
    df = pd.read_csv(FINAL_RATINGS)

    print("Building matrix...")
    matrix, user_ids, movie_ids = build_matrix(df)

    print("Computing user-user similarity...")
    user_sim = cosine_similarity(matrix)

    print("Computing item-item similarity...")
    item_sim = cosine_similarity(matrix.T)

    print("Saving similarity matrices...")
    np.save(KNN_DIR / "user_similarity.npy", user_sim)
    np.save(KNN_DIR / "item_similarity.npy", item_sim)
    np.save(KNN_DIR / "user_ids.npy", user_ids)
    np.save(KNN_DIR / "movie_ids.npy", movie_ids)

    print("KNN training complete!")


if __name__ == "__main__":
    train_knn()
