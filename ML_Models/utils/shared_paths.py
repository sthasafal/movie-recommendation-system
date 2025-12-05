from pathlib import Path

# Base directory = ML_Models folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data files from backend (ratings + movies)
DATA_DIR = BASE_DIR.parent / "Backend" / "data" / "processed"
FINAL_MOVIES = DATA_DIR / "final_movies.csv"
FINAL_RATINGS = DATA_DIR / "final_ratings.csv"

# Model subfolders
SVD_DIR = BASE_DIR / "svd"
KNN_DIR = BASE_DIR / "knn"
CONTENT_DIR = BASE_DIR / "content_based"
