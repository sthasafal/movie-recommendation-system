import sys
from pathlib import Path

# Ensure project + backend src are on sys.path before importing routers
SRC_DIR = Path(__file__).resolve().parents[1]  # Backend/src
ROOT_DIR = SRC_DIR.parent.parent
for path in (SRC_DIR, ROOT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.recommend_routes import router as recommend_router
from .routes.movie_routes import router as movie_router
from .routes.health_check import router as health_router

app = FastAPI(title="Movie Recommendation API")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(recommend_router)
app.include_router(movie_router)
app.include_router(health_router)
