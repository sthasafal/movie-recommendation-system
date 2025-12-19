import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML_Models.utils.shared_paths import CONTENT_DIR, FINAL_MOVIES

CONTENT_DIR.mkdir(parents=True, exist_ok=True)


def build_genre_strings(df: pd.DataFrame) -> pd.Series:
    """
    Build a genre text string per movie.
    - If a 'genres' column exists (pipe-delimited), use that.
    - Otherwise, fallback to one-hot encoded genre columns.
    """
    if "genres" in df.columns:
        return df["genres"].fillna("").str.replace("|", " ", regex=False)

    one_hot_cols = [
        c for c in df.columns
        if df[c].dropna().isin([0, 1]).all()
        and c not in ("movie_id", "user_id")
    ]

    def row_to_genres(row):
        return " ".join(col for col in one_hot_cols if row.get(col) == 1)

    return df.apply(row_to_genres, axis=1)


def train_content():
    print("Loading movie metadata...")
    movies = pd.read_csv(FINAL_MOVIES)

    print("Constructing combined text features (genres + overview)...")
    movies["genre_text"] = build_genre_strings(movies)
    movies["combined"] = (
        movies["genre_text"].astype(str) + " " +
        movies["overview"].fillna("").astype(str)
    )

    print("Building TF-IDF matrix...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20000,   # IMPORTANT: limits memory
        min_df=5
    )

    tfidf_matrix = vectorizer.fit_transform(movies["combined"])

    print("Saving content-based artifacts...")
    joblib.dump(vectorizer, CONTENT_DIR / "tfidf_vectorizer.pkl")
    save_npz(CONTENT_DIR / "tfidf_matrix.npz", tfidf_matrix)
    np.save(CONTENT_DIR / "movie_ids.npy", movies["movie_id"].to_numpy())

    print("Content model training complete!")


if __name__ == "__main__":
    train_content()
