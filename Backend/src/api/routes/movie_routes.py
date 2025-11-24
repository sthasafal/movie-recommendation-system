from fastapi import APIRouter
from recommenders.content_based.content_based import ContentBasedRecommender
import math

router = APIRouter(prefix="/movie", tags=["Movie"])

cb = ContentBasedRecommender()

def convert_nan(value):
    """Convert NaN to None for JSON compatibility."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

@router.get("/{movie_id}")
def get_movie(movie_id: int):
    details = cb.get_movie_details(movie_id)
    if details is None:
        return {"error": "Movie not found"}

    # Convert all problematic values (NaN, numpy types, etc.)
    cleaned = {}
    for key, value in details.items():
        try:
            # remove NaN
            value = convert_nan(value)

            # convert numpy numbers to Python numbers
            if hasattr(value, "item"):
                value = value.item()

        except Exception:
            value = None

        cleaned[key] = value

    return cleaned
