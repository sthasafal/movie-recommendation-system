from pathlib import Path

# Resolve important project paths in one place
_HERE = Path(__file__).resolve()
BACKEND_DIR = _HERE.parents[3]  # .../Backend
ROOT_DIR = BACKEND_DIR.parent

DATA_DIR = BACKEND_DIR / "data" / "processed"
FINAL_MOVIES = DATA_DIR / "final_movies.csv"
FINAL_RATINGS = DATA_DIR / "final_ratings.csv"

ML_MODELS_DIR = ROOT_DIR / "ML_Models"
SVD_DIR = ML_MODELS_DIR / "svd"
KNN_DIR = ML_MODELS_DIR / "knn"
CONTENT_DIR = ML_MODELS_DIR / "content_based"

SVD_MODEL_PATH = SVD_DIR / "svd_model.pkl"
USER_FACTORS_PATH = SVD_DIR / "user_embeddings.npy"
ITEM_FACTORS_PATH = SVD_DIR / "item_embeddings.npy"

KNN_USER_SIM_PATH = KNN_DIR / "user_similarity.npy"
KNN_ITEM_SIM_PATH = KNN_DIR / "item_similarity.npy"

CONTENT_VECTORIZER_PATH = CONTENT_DIR / "tfidf_vectorizer.pkl"
CONTENT_TFIDF_PATH = CONTENT_DIR / "tfidf_matrix.npz"
CONTENT_COSINE_SIM_PATH = CONTENT_DIR / "cosine_sim.npy"
