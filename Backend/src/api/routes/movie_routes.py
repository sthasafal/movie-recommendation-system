import math
import pandas as pd
from fastapi import APIRouter, Query
from recommenders.content_based.content_based import ContentBasedRecommender
from recommenders.utils.paths import FINAL_MOVIES

router = APIRouter(prefix="/movie", tags=["Movie"])

cb = ContentBasedRecommender()
MOVIES_DF = pd.read_csv(FINAL_MOVIES)

def convert_nan(value):
    """Convert NaN to None for JSON compatibility."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


@router.get("/search")
def search_movies(q: str = Query(..., description="Movie title substring"), limit: int = 10):
    """
    Lightweight title search over the processed movie catalog.
    """
    query = q.strip()
    if not query:
        return []

    mask = (
        MOVIES_DF["title"].str.contains(query, case=False, na=False)
        | MOVIES_DF.get("clean_title", pd.Series(dtype=str)).str.contains(query, case=False, na=False)
    )
    results = MOVIES_DF[mask].head(limit)

    cleaned_rows = []
    for _, row in results.iterrows():
        cleaned = {}
        for key, value in row.to_dict().items():
            try:
                value = convert_nan(value)
                if hasattr(value, "item"):
                    value = value.item()
            except Exception:
                value = None
            cleaned[key] = value
        cleaned_rows.append(cleaned)

    return cleaned_rows


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