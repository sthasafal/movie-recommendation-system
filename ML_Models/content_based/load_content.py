import os
import joblib
import numpy as np
from scipy.sparse import load_npz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_content_model():
    vectorizer = joblib.load(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"))
    tfidf_matrix = load_npz(os.path.join(BASE_DIR, "tfidf_matrix.npz"))
    cosine_sim = np.load(os.path.join(BASE_DIR, "cosine_sim.npy"))
    return vectorizer, tfidf_matrix, cosine_sim
