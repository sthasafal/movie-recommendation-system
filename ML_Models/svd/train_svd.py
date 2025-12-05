import numpy as np
import pandas as pd
import joblib
from sklearn.decomposition import TruncatedSVD

from ML_Models.utils.shared_paths import FINAL_RATINGS


def build_matrix(df):
    pivot = df.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
    return pivot.values, pivot.index, pivot.columns


def train_svd(n_components=20):
    print("Loading rating data...")
    df = pd.read_csv(FINAL_RATINGS)

    print("Building user-movie matrix...")
    matrix, user_ids, movie_ids = build_matrix(df)

    print("Training SVD model...")
    svd = TruncatedSVD(n_components=n_components)
    user_factors = svd.fit_transform(matrix)
    item_factors = svd.components_.T

    print("Saving model + embeddings...")
    joblib.dump(svd, "svd_model.pkl")
    np.save("user_embeddings.npy", user_factors)
    np.save("item_embeddings.npy", item_factors)

    print("SVD training complete!")


if __name__ == "__main__":
    train_svd()
