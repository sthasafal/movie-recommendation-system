import sys
from pathlib import Path

import joblib
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import SVD_DIR


def load_svd():
    model_path = SVD_DIR / "svd_model.pkl"
    user_emb_path = SVD_DIR / "user_embeddings.npy"
    item_emb_path = SVD_DIR / "item_embeddings.npy"
    user_ids_path = SVD_DIR / "user_ids.npy"
    movie_ids_path = SVD_DIR / "movie_ids.npy"

    svd_model = joblib.load(model_path)
    user_embeddings = np.load(user_emb_path)
    item_embeddings = np.load(item_emb_path)
    user_ids = np.load(user_ids_path)
    movie_ids = np.load(movie_ids_path)

    return svd_model, user_embeddings, item_embeddings, user_ids, movie_ids
