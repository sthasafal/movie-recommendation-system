import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import FINAL_RATINGS, KNN_DIR

KNN_DIR.mkdir(parents=True, exist_ok=True)


def train_knn(top_k=50):
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

    print("Computing item–item cosine similarity (Top-K only)...")
    item_matrix = matrix.T  # items × users
    sim = cosine_similarity(item_matrix, dense_output=False)

    knn_indices = np.argsort(sim.toarray(), axis=1)[:, -top_k-1:-1]
    knn_scores = np.take_along_axis(sim.toarray(), knn_indices, axis=1)

    print("Saving KNN artifacts...")
    np.save(KNN_DIR / "item_knn_indices.npy", knn_indices)
    np.save(KNN_DIR / "item_knn_scores.npy", knn_scores)
    np.save(KNN_DIR / "movie_ids.npy", movie_cat.cat.categories.to_numpy())

    print("KNN training complete!")


if __name__ == "__main__":
    train_knn()
