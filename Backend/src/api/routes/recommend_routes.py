from fastapi import APIRouter
from recommenders.hybrid_recommender import HybridRecommender
from recommenders.content_based.content_based import ContentBasedRecommender

router = APIRouter(prefix="/recommend", tags=["Recommend"])

hybrid = HybridRecommender()
cb = ContentBasedRecommender()

@router.get("/user/{user_id}")
def recommend_for_user(user_id: int, top_n: int = 10):
    return hybrid.recommend(user_id, top_n)

@router.get("/similar/{movie_id}")
def similar_movies(movie_id: int, top_n: int = 10):
    result = cb.recommend_similar(movie_id, top_n)
    return result.to_dict(orient="records") if result is not None else []

@router.get("/hybrid/{user_id}")
def hybrid_recommend(user_id: int, top_n: int = 10):
    return hybrid.recommend(user_id, top_n)
