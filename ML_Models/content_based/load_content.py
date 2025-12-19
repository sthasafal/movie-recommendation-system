import sys
from pathlib import Path

import joblib
import numpy as np
from scipy.sparse import load_npz

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import CONTENT_DIR


def load_content_model():
    vectorizer = joblib.load(CONTENT_DIR / "tfidf_vectorizer.pkl")
    tfidf_matrix = load_npz(CONTENT_DIR / "tfidf_matrix.npz")
    movie_ids = np.load(CONTENT_DIR / "movie_ids.npy")

    # cosine_sim is optional; fall back to on-the-fly similarity if missing or mismatched
    cosine_sim_path = CONTENT_DIR / "cosine_sim.npy"
    cosine_sim = None
    if cosine_sim_path.exists():
        cosine_sim = np.load(cosine_sim_path)
    return vectorizer, tfidf_matrix, cosine_sim, movie_ids
