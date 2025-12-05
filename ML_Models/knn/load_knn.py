import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_knn():
    user_sim = np.load(os.path.join(BASE_DIR, "user_similarity.npy"))
    item_sim = np.load(os.path.join(BASE_DIR, "item_similarity.npy"))
    return user_sim, item_sim
