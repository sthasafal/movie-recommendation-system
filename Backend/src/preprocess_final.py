import os
import numpy as np
import pandas as pd
from re import escape as re_escape

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Legacy MovieLens 100K paths
MOVIELENS_ITEM = os.path.join(DATA_DIR, "u.item")
MOVIELENS_RATINGS = os.path.join(DATA_DIR, "u.data")
TMDB_FILE = os.path.join(DATA_DIR, "movies_with_tmdb.csv")
TMDB_EXTERNAL_FILE = os.path.join(DATA_DIR, "external", "movies_with_tmdb.csv")

# Newer MovieLens (e.g., 25M/32M style) paths under data/ml-32m/
NEW_DATA_DIR = os.path.join(DATA_DIR, "ml-32m")
NEW_MOVIES = os.path.join(NEW_DATA_DIR, "movies.csv")
NEW_RATINGS = os.path.join(NEW_DATA_DIR, "ratings.csv")
NEW_LINKS = os.path.join(NEW_DATA_DIR, "links.csv")

PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FINAL_MOVIES = os.path.join(PROCESSED_DIR, "final_movies.csv")
FINAL_RATINGS = os.path.join(PROCESSED_DIR, "final_ratings.csv")

os.makedirs(PROCESSED_DIR, exist_ok=True)


def using_new_dataset():
    return os.path.exists(NEW_MOVIES) and os.path.exists(NEW_RATINGS)


# LOAD MOVIES/RATINGS (NEW DATASET)
def load_new_movies():
    movies = pd.read_csv(NEW_MOVIES)
    movies = movies.rename(columns={"movieId": "movie_id"})
    # normalize genres text
    movies["genres"] = movies["genres"].replace("(no genres listed)", "").fillna("")
    return movies


def load_new_ratings():
    ratings = pd.read_csv(NEW_RATINGS)
    return ratings.rename(columns={"movieId": "movie_id", "userId": "user_id"})


def merge_links(movies):
    if not os.path.exists(NEW_LINKS):
        return movies
    links = pd.read_csv(NEW_LINKS).rename(columns={"movieId": "movie_id", "imdbId": "imdb_id", "tmdbId": "tmdb_id"})
    return movies.merge(links, on="movie_id", how="left")


def expand_genres(movies):
    """Create one-hot genre columns for compatibility with downstream content model."""
    genre_lists = movies["genres"].fillna("").str.split("|")
    all_genres = sorted({g for lst in genre_lists for g in lst if g})
    for g in all_genres:
        movies[g] = movies["genres"].str.contains(rf"(?:^|\|){re_escape(g)}(?:\||$)", regex=True)
        movies[g] = movies[g].astype(int)
    return movies


# LOAD MOVIELENS MOVIE METADATA (LEGACY)
def load_movielens_movies():
    columns = [
        "movie_id", "title", "release_date", "video_release", "IMDb_URL",
        "unknown", "Action", "Adventure", "Animation", "Children",
        "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
        "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
        "Sci-Fi", "Thriller", "War", "Western"
    ]

    movies = pd.read_csv(
        MOVIELENS_ITEM,
        sep="|",
        encoding="latin-1",
        names=columns,
        usecols=range(24),
        header=None
    )
    return movies


# LOAD MOVIELENS RATINGS (LEGACY)
def load_ratings():
    ratings = pd.read_csv(
        MOVIELENS_RATINGS,
        sep="\t",
        names=["user_id", "movie_id", "rating", "timestamp"]
    )
    return ratings


# MERGE TMDB METADATA (LEGACY)
def merge_tmdb(movies):
    # Prefer local merged file; fall back to external export if present
    tmdb_path = TMDB_FILE if os.path.exists(TMDB_FILE) else TMDB_EXTERNAL_FILE
    if not os.path.exists(tmdb_path):
        return movies
    tmdb = pd.read_csv(tmdb_path)
    merged = pd.merge(movies, tmdb, on="movie_id", how="left")
    return merged


def _dedupe_titles_and_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize title/tmdb columns after merges to keep expected names."""
    if "title_y" in df.columns:
        df = df.drop(columns=["title_y"])
    if "title_x" in df.columns and "title" not in df.columns:
        df = df.rename(columns={"title_x": "title"})

    if "tmdb_id_y" in df.columns:
        df = df.drop(columns=["tmdb_id_y"])
    if "tmdb_id_x" in df.columns and "tmdb_id" not in df.columns:
        df = df.rename(columns={"tmdb_id_x": "tmdb_id"})
    return df


# CLEAN MOVIE TITLES
def clean_titles(df):
    # Determine which title column exists
    if "title" in df.columns:
        title_col = "title"
    elif "title_x" in df.columns:
        title_col = "title_x"
    elif "title_y" in df.columns:
        title_col = "title_y"
    else:
        raise KeyError("No title column found in movie dataset.")

    # Extract clean title (remove year)
    df["clean_title"] = df[title_col].str.extract(
        r"^(.*?)(\s\(|$)", expand=False
    )[0]
    df["clean_title"] = df["clean_title"].str.strip()

    return df


# SAVE FINAL OUTPUT FILES
def save_final(movies, ratings):
    movies.to_csv(FINAL_MOVIES, index=False)
    ratings.to_csv(FINAL_RATINGS, index=False)

    print("======================================")
    print("FINAL DATASETS SAVED SUCCESSFULLY!")
    print(f" - {FINAL_MOVIES}")
    print(f" - {FINAL_RATINGS}")
    print("======================================\n")


# MAIN PIPELINE
def run_preprocessing():
    if using_new_dataset():
        print("Detected new MovieLens dataset in data/ml-32m/.")
        movies = load_new_movies()
        ratings = load_new_ratings()
        movies = merge_links(movies)
        movies = expand_genres(movies)
        movies = merge_tmdb(movies)
        movies = _dedupe_titles_and_ids(movies)
    else:
        print("Loading legacy MovieLens 100K dataset...")
        movies = load_movielens_movies()
        ratings = load_ratings()
        print("Merging TMDb metadata...")
        movies = merge_tmdb(movies)
        movies = _dedupe_titles_and_ids(movies)

    print("Cleaning movie titles...")
    movies = clean_titles(movies)

    # Handle missing TMDb data / placeholders
    print("Normalizing metadata...")
    movies["poster_path"] = movies.get("poster_path", "")
    movies["overview"] = movies.get("overview", "")
    movies["poster_path"] = movies["poster_path"].fillna("")
    movies["overview"] = movies["overview"].fillna("")
    movies["vote_average"] = movies.get("vote_average", np.nan)
    movies["vote_average"].fillna(movies["vote_average"].mean(), inplace=True)

    print("Saving final datasets...")
    save_final(movies, ratings)


if __name__ == "__main__":
    run_preprocessing()
