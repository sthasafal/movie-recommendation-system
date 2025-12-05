import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from ML_Models.utils.shared_paths import FINAL_RATINGS


def build_matrix(df):
    pivot = df.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
    return pivot.values


def train_knn():
    print("Loading rating data...")
    df = pd.read_csv(FINAL_RATINGS)

    print("Building matrix...")
    matrix = build_matrix(df)

    print("Computing user-user similarity...")
    user_sim = cosine_similarity(matrix)

    print("Computing item-item similarity...")
    item_sim = cosine_similarity(matrix.T)

    print("Saving similarity matrices...")
    np.save("user_similarity.npy", user_sim)
    np.save("item_similarity.npy", item_sim)

    print("KNN training complete!")


if __name__ == "__main__":
    train_knn()
