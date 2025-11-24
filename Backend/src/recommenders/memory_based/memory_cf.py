import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MemoryCF:
    def __init__(self, matrix):
        self.matrix = matrix.fillna(0)

        print("Computing User–User Similarity…")
        self.user_similarity = cosine_similarity(self.matrix)

        print("Computing Item–Item Similarity…")
        self.item_similarity = cosine_similarity(self.matrix.T)

    # USER–USER
    def predict_user_user(self, user_id, movie_id):
        if movie_id not in self.matrix.columns:
            return None

        user_index = user_id - 1
        similarities = self.user_similarity[user_index]
        movie_ratings = self.matrix[movie_id].values

        num = np.dot(similarities, movie_ratings)
        den = np.sum(np.abs(similarities))
        return num / den if den != 0 else None

    # ITEM–ITEM
    def predict_item_item(self, user_id, movie_id):
        if user_id not in self.matrix.index:
            return None

        if movie_id not in self.matrix.columns:
            return None

        user_ratings = self.matrix.loc[user_id]
        movie_idx = self.matrix.columns.get_loc(movie_id)

        similarities = self.item_similarity[movie_idx]

        num = np.dot(similarities, user_ratings)
        den = np.sum(np.abs(similarities))
        return num / den if den != 0 else None

    # TOP-N
    def recommend_user_user(self, user_id, top_n=10):
        predictions = {}

        for movie_id in self.matrix.columns:
            if np.isnan(self.matrix.loc[user_id, movie_id]):
                predictions[movie_id] = self.predict_user_user(user_id, movie_id)

        return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]
