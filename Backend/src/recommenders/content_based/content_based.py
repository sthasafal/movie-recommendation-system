import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ML_Models.content_based.load_content import load_content_model
from recommenders.utils.paths import FINAL_MOVIES


# CONTENT-BASED RECOMMENDER (pre-trained TF-IDF + cosine similarity)
class ContentBasedRecommender:
    def __init__(self):
        print("Loading movie metadata...")
        self.movies = pd.read_csv(
            FINAL_MOVIES,
            low_memory=False,
            dtype={"poster_path": "string", "overview": "string"},
        )

        print("Loading pre-trained content model artifacts...")
        (
            self.vectorizer,
            self.tfidf_matrix,
            self.similarity,
            self.model_movie_ids,
        ) = load_content_model()

        if self.similarity is not None and self.similarity.shape[0] != len(self.model_movie_ids):
            # Mismatched legacy similarity matrix; ignore it
            print("Content similarity matrix shape mismatch; falling back to on-the-fly similarity.")
            self.similarity = None

        # Keep only rows present in the trained model order
        self.movies = (
            self.movies[self.movies["movie_id"].isin(self.model_movie_ids)]
            .copy()
            .reset_index(drop=True)
        )
        self.id_to_idx = {
            int(mid): idx for idx, mid in enumerate(self.model_movie_ids)
        }

    # Recommend movies similar to a given movie_id
    def recommend_similar(self, movie_id, top_n=10):
        if movie_id not in self.id_to_idx:
            return None

        idx = self.id_to_idx[movie_id]

        if self.similarity is not None:
            sim_scores = list(enumerate(self.similarity[idx]))
        else:
            # Compute similarity on the fly to avoid stale or missing precomputed matrices
            row_vec = self.tfidf_matrix[idx]
            sims = cosine_similarity(row_vec, self.tfidf_matrix, dense_output=False).toarray().ravel()
            sim_scores = list(enumerate(sims))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in sim_scores[1:top_n + 1]]

        return self.movies.iloc[top_indices][[
            "movie_id", "title", "clean_title", "poster_path", "vote_average"
        ]]

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
