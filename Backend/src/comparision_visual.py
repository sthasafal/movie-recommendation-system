import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Backend.src.recommenders.model_based.svd_cf import SVD_CF
from Backend.src.recommenders.memory_based.memory_cf import MemoryCF
from Backend.src.recommenders.content_based.content_based import ContentBasedRecommender
from Backend.src.recommenders.hybrid_recommender import HybridRecommender
from Backend.src.recommenders.utils.matrix_builder import load_data

# Load processed data
movies = pd.read_csv("Backend/data/processed/final_movies.csv")
ratings = pd.read_csv("Backend/data/processed/final_ratings.csv")



# Load trained models
svd = SVD_CF()
svd.load()

knn = MemoryCF()
knn.load()

content = ContentBasedRecommender()
content.load()

hybrid = HybridRecommender()
hybrid.load()



USER_ID = 1        # choose any valid MovieLens user
TOP_N = 10

recs = {}

recs["SVD"] = svd.recommend(user_id=USER_ID, top_n=TOP_N)
recs["KNN"] = knn.recommend(user_id=USER_ID, top_n=TOP_N)
recs["Hybrid"] = hybrid.recommend(user_id=USER_ID, top_n=TOP_N)

# Content-based requires a movie reference
MOVIE_ID = ratings[ratings["user_id"] == USER_ID]["movie_id"].iloc[0]
recs["Content-Based"] = content.recommend_similar(movie_id=MOVIE_ID, top_n=TOP_N)



avg_scores = {
    model: recs[model]["score"].mean()
    for model in recs
}

plt.figure(figsize=(7,4))
plt.bar(avg_scores.keys(), avg_scores.values())
plt.ylabel("Average Recommendation Score")
plt.xlabel("Model")
plt.title("Hybrid vs Other Models (Real Predictions)")
plt.tight_layout()
plt.savefig("real_hybrid_vs_models_scores.png")
plt.show()


diversity = {
    model: recs[model]["movie_id"].nunique()
    for model in recs
}

plt.figure(figsize=(7,4))
plt.bar(diversity.keys(), diversity.values())
plt.ylabel("Unique Movies in Top-10")
plt.xlabel("Model")
plt.title("Recommendation Diversity Comparison (Real Data)")
plt.tight_layout()
plt.savefig("real_hybrid_vs_models_diversity.png")
plt.show()
hybrid_set = set(recs["Hybrid"]["movie_id"])

overlap = {
    model: len(hybrid_set.intersection(set(recs[model]["movie_id"])))
    for model in recs if model != "Hybrid"
}

plt.figure(figsize=(7,4))
plt.bar(overlap.keys(), overlap.values())
plt.ylabel("Overlapping Movies with Hybrid")
plt.xlabel("Model")
plt.title("Overlap Between Hybrid and Other Models")
plt.tight_layout()
plt.savefig("real_hybrid_overlap.png")
plt.show()


comparison_df = pd.DataFrame({
    "Model": avg_scores.keys(),
    "Avg Score": avg_scores.values(),
    "Diversity (Unique Movies)": diversity.values()
})

comparison_df
