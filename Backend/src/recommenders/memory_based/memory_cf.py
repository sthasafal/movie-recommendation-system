import numpy as np
from ML_Models.knn.load_knn import load_knn


class MemoryCF:
    def __init__(self, matrix):
        # Load precomputed similarities + id order
        (
            self.user_similarity,
            self.item_similarity,
            self.user_ids,
            self.movie_ids,
        ) = load_knn()

        # Align rating matrix to saved id order for consistent lookups
        self.matrix = (
            matrix.reindex(index=self.user_ids, columns=self.movie_ids)
            .fillna(0)
        )

        self.user_index = {uid: idx for idx, uid in enumerate(self.user_ids)}
        self.movie_index = {mid: idx for idx, mid in enumerate(self.movie_ids)}

    # USER-USER
    def predict_user_user(self, user_id, movie_id):
        if user_id not in self.user_index or movie_id not in self.movie_index:
            return None

        user_idx = self.user_index[user_id]
        movie_idx = self.movie_index[movie_id]

        similarities = self.user_similarity[user_idx]
        movie_ratings = self.matrix.iloc[:, movie_idx].values

        num = np.dot(similarities, movie_ratings)
        den = np.sum(np.abs(similarities))
        return num / den if den != 0 else None

    # ITEM-ITEM
    def predict_item_item(self, user_id, movie_id):
        if user_id not in self.user_index or movie_id not in self.movie_index:
            return None

        user_ratings = self.matrix.loc[user_id].values
        movie_idx = self.movie_index[movie_id]

        similarities = self.item_similarity[movie_idx]

        num = np.dot(similarities, user_ratings)
        den = np.sum(np.abs(similarities))
        return num / den if den != 0 else None

    # TOP-N
    def recommend_user_user(self, user_id, top_n=10):
        if user_id not in self.user_index:
            return []
        predictions = {}

        for movie_id in self.movie_ids:
            if np.isnan(self.matrix.loc[user_id, movie_id]):
                predictions[movie_id] = self.predict_user_user(user_id, movie_id)

        filtered = [(mid, score) for mid, score in predictions.items() if score is not None]
        return sorted(filtered, key=lambda x: x[1], reverse=True)[:top_n]
