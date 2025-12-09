import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import FINAL_RATINGS, SVD_DIR

SVD_DIR.mkdir(parents=True, exist_ok=True)


def build_matrix(df):
    pivot = df.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
    return pivot.values, pivot.index.to_numpy(), pivot.columns.to_numpy()


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
    joblib.dump(svd, SVD_DIR / "svd_model.pkl")
    np.save(SVD_DIR / "user_embeddings.npy", user_factors)
    np.save(SVD_DIR / "item_embeddings.npy", item_factors)
    np.save(SVD_DIR / "user_ids.npy", user_ids)
    np.save(SVD_DIR / "movie_ids.npy", movie_ids)

    print("SVD training complete!")


if __name__ == "__main__":
    train_svd()
