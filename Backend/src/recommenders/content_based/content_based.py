import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
FINAL_MOVIES = os.path.join(PROCESSED_DIR, "final_movies.csv")

# CONTENT-BASED RECOMMENDER (GENRE + METADATA SIMILARITY)
class ContentBasedRecommender:
    def __init__(self):
        print("Loading movie metadata...")
        self.movies = pd.read_csv(FINAL_MOVIES)

        # identify genre columns
        self.genre_cols = [
            "unknown","Action","Adventure","Animation","Children","Comedy",
            "Crime","Documentary","Drama","Fantasy","Film-Noir","Horror",
            "Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western"
        ]

        print("Building feature matrix (genres + vote average)...")
        # genres + TMDb vote_average
        self.feature_matrix = self.movies[self.genre_cols + ["vote_average"]].fillna(0)

        print("Computing cosine similarity matrix...")
        self.similarity = cosine_similarity(self.feature_matrix)

    # Recommend movies similar to a given movie_id
    def recommend_similar(self, movie_id, top_n=10):
        if movie_id not in self.movies["movie_id"].values:
            return None

        # find index of movie
        idx = self.movies.index[self.movies["movie_id"] == movie_id][0]

        # similarities for this movie
        sim_scores = list(enumerate(self.similarity[idx]))

        # sort by similarity (descending)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # top N recommendations (skip the movie itself at index 0)
        top_indices = [i[0] for i in sim_scores[1:top_n+1]]

        return self.movies.iloc[top_indices][["movie_id", "title", "clean_title", "poster_path", "vote_average"]]

    # GET MOVIE DETAILS
    def get_movie_details(self, movie_id):
        row = self.movies[self.movies["movie_id"] == movie_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()

# TEST RUNNER (to verify everything works)
def run_content_based_demo():
    cb = ContentBasedRecommender()

    print("\nExamples:")
    print("Similar to movie_id = 1:")
    print(cb.recommend_similar(1, top_n=5))

    print("\nMovie details (1):")
    print(cb.get_movie_details(1))

    print("\nContent-Based Filtering working successfully!")


if __name__ == "__main__":
    run_content_based_demo()
