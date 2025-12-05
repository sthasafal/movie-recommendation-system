import joblib
import numpy as np
from scipy.sparse import load_npz
from ML_Models.utils.shared_paths import CONTENT_DIR


def load_content_model():
    vectorizer = joblib.load(CONTENT_DIR / "tfidf_vectorizer.pkl")
    tfidf_matrix = load_npz(CONTENT_DIR / "tfidf_matrix.npz")
    cosine_sim = np.load(CONTENT_DIR / "cosine_sim.npy")
    movie_ids = np.load(CONTENT_DIR / "movie_ids.npy")
    return vectorizer, tfidf_matrix, cosine_sim, movie_ids
