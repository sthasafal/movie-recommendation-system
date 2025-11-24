import numpy as np
from sklearn.decomposition import TruncatedSVD
import os
import joblib

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

MODELS_DIR = os.path.join(BASE_DIR, "models")

SVD_MODEL_PATH = os.path.join(MODELS_DIR, "svd_model.pkl")
USER_FACTORS_PATH = os.path.join(MODELS_DIR, "user_embeddings.npy")
ITEM_FACTORS_PATH = os.path.join(MODELS_DIR, "item_embeddings.npy")


class SVD_CF:
    def __init__(self, n_components=20):
        self.n = n_components

    def fit(self, matrix):
        print("Training SVD Model…")
        matrix_filled = matrix.fillna(0)

        svd = TruncatedSVD(n_components=self.n)
        self.user_factors = svd.fit_transform(matrix_filled)
        self.item_factors = svd.components_.T

        os.makedirs(MODELS_DIR, exist_ok=True)
        joblib.dump(svd, SVD_MODEL_PATH)
        np.save(USER_FACTORS_PATH, self.user_factors)
        np.save(ITEM_FACTORS_PATH, self.item_factors)

        print("SVD Model Saved.")

    def load(self):
        self.user_factors = np.load(USER_FACTORS_PATH)
        self.item_factors = np.load(ITEM_FACTORS_PATH)
        return self

    def predict(self, user_id, movie_id, matrix):
        if movie_id not in matrix.columns:
            return None

        user_idx = user_id - 1
        movie_idx = matrix.columns.get_loc(movie_id)

        return np.dot(self.user_factors[user_idx], self.item_factors[movie_idx])

    def recommend(self, user_id, matrix, top_n=10):
        predictions = {}

        for movie_id in matrix.columns:
            if np.isnan(matrix.loc[user_id, movie_id]):
                predictions[movie_id] = self.predict(user_id, movie_id, matrix)

        return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]
