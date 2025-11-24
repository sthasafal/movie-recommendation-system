from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.recommend_routes import router as recommend_router
from api.routes.movie_routes import router as movie_router
from api.routes.health_check import router as health_router

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
