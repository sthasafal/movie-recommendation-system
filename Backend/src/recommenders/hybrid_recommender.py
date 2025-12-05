from recommenders.recommend_utils import normalize_scores
from recommenders.memory_based.memory_cf import MemoryCF
from recommenders.model_based.svd_cf import SVD_CF
from recommenders.content_based.content_based import ContentBasedRecommender
from recommenders.utils.matrix_builder import load_data, create_user_movie_matrix
import numpy as np


class HybridRecommender:
    def __init__(self, w_cf=0.5, w_content=0.5):
        """Initialize Hybrid Recommender"""
        self.w_cf = w_cf
        self.w_content = w_content

        # Load data
        self.movies, self.ratings = load_data()
        base_matrix = create_user_movie_matrix(self.ratings)

        # Load all models (pre-trained artifacts)
        print("Loading Collaborative Filtering Models (KNN similarities)...")
        self.mem_cf = MemoryCF(base_matrix)

        print("Loading SVD Model (pre-trained)...")
        self.svd_cf = SVD_CF()

        print("Loading Content-Based Model (pre-trained)...")
        self.cb = ContentBasedRecommender()

        # Align matrix columns to SVD/movie ids for scoring
        self.matrix = base_matrix.reindex(
            index=self.svd_cf.user_ids, columns=self.svd_cf.movie_ids
        )

    # Hybrid Score for a single (user, movie)
    def hybrid_score(self, user_id, movie_id):
        # Collaborative Filtering score (SVD)
        cf_score = self.svd_cf.predict(user_id, movie_id)
        if cf_score is None:
            cf_score = 0

        # Content score
        cb_score = 0
        if movie_id in self.cb.id_to_idx:
            similar_movies = self.cb.recommend_similar(movie_id, top_n=10)
            if similar_movies is not None:
                cb_score = 1  # simple signal meaning "this movie has similar content"

        # Weighted hybrid score
        final_score = (self.w_cf * cf_score) + (self.w_content * cb_score)
        return final_score

    # Top-N Hybrid Recommendations
    def recommend(self, user_id, top_n=10):
        if user_id not in self.svd_cf.user_index:
            return []

        predictions = {}

        for movie_id in self.svd_cf.movie_ids:
            # respect existing ratings
            if np.isnan(self.matrix.loc[user_id, movie_id]):
                predictions[movie_id] = self.hybrid_score(user_id, movie_id)

        # Sort by score (descending)
        ranked = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

        results = []
        for movie_id, score in ranked[:top_n]:
            movie_row = self.movies[self.movies["movie_id"] == movie_id].iloc[0]
            results.append({
                "movie_id": int(movie_id),
                "title": movie_row["title"],
                "clean_title": movie_row["clean_title"],
                "score": float(score),
                "poster_path": movie_row["poster_path"],
                "vote_average": float(movie_row["vote_average"])
            })

        return results


# RUNNER
def run_hybrid_demo():
    hybrid = HybridRecommender(w_cf=0.7, w_content=0.3)
    print("\nHybrid Recommendations for User 1:")
    print(hybrid.recommend(1, top_n=5))

    print("\nHybrid Recommender Working Successfully!")


if __name__ == "__main__":
    run_hybrid_demo()
