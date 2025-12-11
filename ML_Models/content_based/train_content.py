import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import CONTENT_DIR, FINAL_MOVIES

CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# Genre indicator columns in the processed dataset
GENRE_COLS = [
    "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
]


def build_genre_strings(df: pd.DataFrame) -> pd.Series:
    """Turn one-hot genre columns into a space-separated genre string per movie."""
    def row_to_genres(row):
        genres = [col for col in GENRE_COLS if col in row.index and row[col] == 1]
        return " ".join(genres)
    return df.apply(row_to_genres, axis=1)
    


def train_content():
    print("Loading movie metadata...")
    movies = pd.read_csv(FINAL_MOVIES)

    # Build combined text from genres + overview
    print("Constructing combined text features (genres + overview)...")
    movies["genre_text"] = build_genre_strings(movies)
    movies["combined"] = movies["genre_text"].astype(str) + " " + movies["overview"].astype(str)

    print("Building TF-IDF matrix...")
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(movies["combined"])

    print("Computing cosine similarity...")
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    print("Saving model + matrices...")
    joblib.dump(vectorizer, CONTENT_DIR / "tfidf_vectorizer.pkl")
    save_npz(CONTENT_DIR / "tfidf_matrix.npz", tfidf_matrix)
    np.save(CONTENT_DIR / "cosine_sim.npy", cosine_sim)
    np.save(CONTENT_DIR / "movie_ids.npy", movies["movie_id"].to_numpy())

    
    movie_ids = movies["movie_id"].to_numpy()
    print("\n=== MOVIE IDS PREVIEW ===")
    print(movie_ids[:20])
    print("Min:", movie_ids.min())
    print("Max:", movie_ids.max())
    print("Unique:", len(np.unique(movie_ids)))
    print("Total count:", movie_ids.size)

    print("\n=== COSINE SIM SHAPE ===")
    print(cosine_sim.shape)
    print("First 5×5:")
    print(cosine_sim[:5, :5])

    print("\n=== TF-IDF MATRIX SHAPE ===")
    print(tfidf_matrix.shape)
    print(tfidf_matrix)

    print("Content model training complete!")


if __name__ == "__main__":
    train_content()
