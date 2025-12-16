import math
from fastapi import APIRouter
from recommenders.hybrid_recommender import HybridRecommender
from recommenders.content_based.content_based import ContentBasedRecommender
from recommenders.memory_based.memory_cf import MemoryCF
from recommenders.model_based.svd_cf import SVD_CF
from recommenders.utils.matrix_builder import load_data, create_user_movie_matrix

router = APIRouter(prefix="/recommend", tags=["Recommend"])

movies_df, ratings_df = load_data()
matrix = create_user_movie_matrix(ratings_df)

hybrid = HybridRecommender()
cb = ContentBasedRecommender()
mem_cf = MemoryCF(matrix)
svd_cf = SVD_CF()

def _clean_value(value):
    """Normalize NaN/numpy types for JSON responses."""
    try:
        if value is None:
            return None
        if isinstance(value, float) and math.isnan(value):
            return None
        if hasattr(value, "item"):
            return value.item()
    except Exception:
        return None
    return value

def _movie_payload(movie_id, score):
    row = movies_df[movies_df["movie_id"] == movie_id]
    if row.empty:
        return None
    movie_row = row.iloc[0]
    return {
        "movie_id": int(_clean_value(movie_id)),
        "title": movie_row["title"],
        "clean_title": _clean_value(movie_row.get("clean_title")),
        "score": _clean_value(score),
        "poster_path": _clean_value(movie_row.get("poster_path")),
        "vote_average": _clean_value(movie_row.get("vote_average")),
    }

@router.get("/user/{user_id}")
def recommend_for_user(user_id: int, top_n: int = 10):
    return hybrid.recommend(user_id, top_n)

@router.get("/similar/{movie_id}")
def similar_movies(movie_id: int, top_n: int = 10):
    result = cb.recommend_similar(movie_id, top_n)
    if result is None:
        return []

    cleaned = []
    for _, row in result.iterrows():
        payload = {k: _clean_value(v) for k, v in row.to_dict().items()}
        cleaned.append(payload)
    return cleaned

@router.get("/hybrid/{user_id}")
def hybrid_recommend(user_id: int, top_n: int = 10):
    return hybrid.recommend(user_id, top_n)


@router.get("/model/{model}/{user_id}")
def recommend_by_model(model: str, user_id: int, top_n: int = 10):
    """
    Serve recommendations from specific models (hybrid, svd, knn).
    """
    model = model.lower()
    if model == "hybrid":
        return hybrid.recommend(user_id, top_n)
    if model == "svd":
        ranked = svd_cf.recommend(user_id, top_n=top_n)
    elif model in {"knn", "memory"}:
        ranked = mem_cf.recommend_user_user(user_id, top_n=top_n)
    else:
        return {"error": f"Unknown model '{model}'. Use hybrid, svd, knn."}

    results = []
    for movie_id, score in ranked:
        payload = _movie_payload(movie_id, score)
        if payload:
            results.append(payload)
    return results
