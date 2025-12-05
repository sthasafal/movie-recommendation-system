import numpy as np
from ML_Models.svd.load_svd import load_svd


class SVD_CF:
    def __init__(self):
        (
            self.svd_model,
            self.user_factors,
            self.item_factors,
            self.user_ids,
            self.movie_ids,
        ) = load_svd()
        self.user_index = {uid: idx for idx, uid in enumerate(self.user_ids)}
        self.movie_index = {mid: idx for idx, mid in enumerate(self.movie_ids)}

    def predict(self, user_id, movie_id):
        if user_id not in self.user_index or movie_id not in self.movie_index:
            return None
        u_idx = self.user_index[user_id]
        m_idx = self.movie_index[movie_id]
        return float(np.dot(self.user_factors[u_idx], self.item_factors[m_idx]))

    def recommend(self, user_id, top_n=10):
        if user_id not in self.user_index:
            return []
        scores = {
            mid: self.predict(user_id, mid)
            for mid in self.movie_ids
            if self.predict(user_id, mid) is not None
        }
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_n]
