import pandas as pd
import numpy as np
import os

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

MOVIELENS_ITEM = os.path.join(DATA_DIR, "u.item")
MOVIELENS_RATINGS = os.path.join(DATA_DIR, "u.data")
TMDB_FILE = os.path.join(DATA_DIR, "movies_with_tmdb.csv")

FINAL_MOVIES = os.path.join(DATA_DIR, "final_movies.csv")
FINAL_RATINGS = os.path.join(DATA_DIR, "final_ratings.csv")


# LOAD MOVIELENS MOVIE METADATA
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


# LOAD MOVIELENS RATINGS
def load_ratings():
    ratings = pd.read_csv(
        MOVIELENS_RATINGS,
        sep="\t",
        names=["user_id", "movie_id", "rating", "timestamp"]
    )
    return ratings


# MERGE TMDB METADATA
def merge_tmdb(movies):
    tmdb = pd.read_csv(TMDB_FILE)
    merged = pd.merge(movies, tmdb, on="movie_id", how="left")
    return merged


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
    print(" - final_movies.csv")
    print(" - final_ratings.csv")
    print("======================================\n")


# MAIN PIPELINE
def run_preprocessing():
    print("Loading datasets...")

    movies = load_movielens_movies()
    ratings = load_ratings()

    print("Merging TMDb metadata...")
    movies = merge_tmdb(movies)

    # Fix duplicate title columns created by merge
    if "title_y" in movies.columns:
        movies.drop(columns=["title_y"], inplace=True)
    if "title_x" in movies.columns and "title" not in movies.columns:
        movies.rename(columns={"title_x": "title"}, inplace=True)

    print("Cleaning movie titles...")
    movies = clean_titles(movies)

    # Handle missing TMDb data
    print("Handling missing TMDb metadata...")
    movies["poster_path"].fillna("", inplace=True)
    movies["overview"].fillna("", inplace=True)
    movies["vote_average"].fillna(movies["vote_average"].mean(), inplace=True)

    print("Saving final datasets...")
    save_final(movies, ratings)


if __name__ == "__main__":
    run_preprocessing()
