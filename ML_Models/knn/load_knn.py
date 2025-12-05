import numpy as np
from ML_Models.utils.shared_paths import KNN_DIR


def load_knn():
    user_sim = np.load(KNN_DIR / "user_similarity.npy")
    item_sim = np.load(KNN_DIR / "item_similarity.npy")
    user_ids = np.load(KNN_DIR / "user_ids.npy")
    movie_ids = np.load(KNN_DIR / "movie_ids.npy")
    return user_sim, item_sim, user_ids, movie_ids
