import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import FINAL_RATINGS, SVD_DIR

SVD_DIR.mkdir(parents=True, exist_ok=True)


def train_svd(n_components=50):
    print("Loading rating data...")
    ratings = pd.read_csv(FINAL_RATINGS)

    print("Encoding user and movie IDs...")
    user_cat = ratings["user_id"].astype("category")
    movie_cat = ratings["movie_id"].astype("category")

    user_idx = user_cat.cat.codes.to_numpy()
    movie_idx = movie_cat.cat.codes.to_numpy()
    values = ratings["rating"].to_numpy()

    print("Building sparse user–movie matrix...")
    matrix = csr_matrix(
        (values, (user_idx, movie_idx)),
        shape=(user_cat.cat.categories.size, movie_cat.cat.categories.size)
    )

    print("Training Truncated SVD...")
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    user_embeddings = svd.fit_transform(matrix)
    movie_embeddings = svd.components_.T

    print("Saving model + embeddings...")
    joblib.dump(svd, SVD_DIR / "svd_model.pkl")
    np.save(SVD_DIR / "user_embeddings.npy", user_embeddings)
    np.save(SVD_DIR / "movie_embeddings.npy", movie_embeddings)
    np.save(SVD_DIR / "user_ids.npy", user_cat.cat.categories.to_numpy())
    np.save(SVD_DIR / "movie_ids.npy", movie_cat.cat.categories.to_numpy())

    print("SVD training complete!")


if __name__ == "__main__":
    train_svd()
