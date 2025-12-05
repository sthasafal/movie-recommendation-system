import os
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_svd():
    model_path = os.path.join(BASE_DIR, "svd_model.pkl")
    user_emb_path = os.path.join(BASE_DIR, "user_embeddings.npy")
    item_emb_path = os.path.join(BASE_DIR, "item_embeddings.npy")

    svd_model = joblib.load(model_path)
    user_embeddings = np.load(user_emb_path)
    item_embeddings = np.load(item_emb_path)

    return svd_model, user_embeddings, item_embeddings
