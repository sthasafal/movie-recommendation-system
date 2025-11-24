import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---- PATH SETUP ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

FINAL_MOVIES = os.path.join(DATA_DIR, "final_movies.csv")
FINAL_RATINGS = os.path.join(DATA_DIR, "final_ratings.csv")

OUTPUT_MOVIE_POP = os.path.join(DATA_DIR, "baseline_movie_popularity.csv")
OUTPUT_USER_AVG = os.path.join(DATA_DIR, "baseline_user_avg.csv")
OUTPUT_GLOBAL = os.path.join(DATA_DIR, "baseline_global.json")


def load_data():
    """Load final cleaned datasets."""
    movies = pd.read_csv(FINAL_MOVIES)
    ratings = pd.read_csv(FINAL_RATINGS)
    return movies, ratings


# BASELINE MODELS

def global_average(ratings):
    """Compute global average rating."""
    global_avg = ratings["rating"].mean()
    print(f"Global Average Rating = {global_avg:.4f}")

    # save
    pd.Series({"global_average": global_avg}).to_json(OUTPUT_GLOBAL)
    return global_avg


def user_average(ratings):
    """Compute average rating per user."""
    user_avg = (
        ratings.groupby("user_id")["rating"]
        .mean()
        .reset_index()
        .rename(columns={"rating": "user_avg_rating"})
    )

    user_avg.to_csv(OUTPUT_USER_AVG, index=False)
    print(f"Saved user averages → {OUTPUT_USER_AVG}")

    return user_avg


def movie_popularity(ratings, movies):
    """
    Movie popularity: 
    - number of ratings (count)
    - average rating
    """
    movie_stats = (
        ratings.groupby("movie_id")
        .agg(
            rating_count=("rating", "count"),
            mean_rating=("rating", "mean")
        )
        .reset_index()
    )

    # merge with movie metadata
    movie_stats = movie_stats.merge(movies[["movie_id", "title"]], on="movie_id", how="left")

    movie_stats.sort_values(
        by=["rating_count", "mean_rating"],
        ascending=[False, False],
        inplace=True
    )

    movie_stats.to_csv(OUTPUT_MOVIE_POP, index=False)
    print(f"Saved movie popularity dataset → {OUTPUT_MOVIE_POP}")

    return movie_stats



# VISUALIZATION (EDA)
def plot_rating_distribution(ratings):
    plt.figure(figsize=(6, 4))
    plt.hist(ratings["rating"], bins=5, edgecolor="black")
    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


def plot_most_rated_movies(movie_pop):
    top = movie_pop.head(10)
    plt.figure(figsize=(10, 4))
    plt.barh(top["title"], top["rating_count"], color="skyblue")
    plt.title("Top 10 Most Rated Movies")
    plt.xlabel("Number of Ratings")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_most_active_users(ratings):
    user_activity = (
        ratings.groupby("user_id")["rating"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 4))
    plt.bar(user_activity.index.astype(str), user_activity.values, color="orange")
    plt.title("Top 10 Most Active Users")
    plt.xlabel("User ID")
    plt.ylabel("Ratings Count")
    plt.tight_layout()
    plt.show()


# MAIN RUNNER
def run_baselines():
    print("Loading final datasets...")
    movies, ratings = load_data()

    print("\ Computing Global Average Model...")
    global_avg = global_average(ratings)

    print("\ Computing User Average Model...")
    user_avg = user_average(ratings)

    print("\n Computing Movie Popularity Model...")
    movie_pop = movie_popularity(ratings, movies)

    print("\nGenerating Visualizations...")
    plot_rating_distribution(ratings)
    plot_most_rated_movies(movie_pop)
    plot_most_active_users(ratings)

    print("\n Baseline Models Completed Successfully!")


if __name__ == "__main__":
    run_baselines()
