import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz

from ML_Models.utils.shared_paths import FINAL_MOVIES


def train_content():
    print("Loading movie metadata...")
    movies = pd.read_csv(FINAL_MOVIES)

    movies["combined"] = (
        movies["genres"].astype(str) + " " + movies["overview"].astype(str)
    )

    print("Building TF-IDF matrix...")
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(movies["combined"])

    print("Computing cosine similarity...")
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    print("Saving model + matrices...")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
    save_npz("tfidf_matrix.npz", tfidf_matrix)
    np.save("cosine_sim.npy", cosine_sim)

    print("Content model training complete!")


if __name__ == "__main__":
    train_content()
