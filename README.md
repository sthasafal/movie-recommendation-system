# Movie Recommendation System

Complete stack: FastAPI backend + pre-trained ML models (MovieLens 100K) + React frontend.

## Prerequisites
- Python 3.11+ (virtualenv recommended)
- Node 18+ (for Vite/React)
- TMDB images are referenced via `poster_path` (no key required for precomputed paths)

## 1) Backend setup
1. Create/activate venv  
   `python -m venv .venv`  
   `.\.venv\Scripts\Activate`
2. Install Python deps  
   `pip install -r Backend/requirements.txt`
3. (Optional) Retrain models if needed (uses MovieLens data already in `Backend/data/processed`)  
   `python -m ML_Models.train_all`
4. Run API  
   `uvicorn Backend.src.api.server:app --reload --port 8000`
5. Key endpoints (JSON):  
   - `GET /health/` – heartbeat  
   - `GET /movie/search?q=toy&limit=10` – title search  
   - `GET /movie/{movie_id}` – details  
   - `GET /recommend/similar/{movie_id}?top_n=10` – content-based  
   - `GET /recommend/model/{model}/{user_id}?top_n=10` – per-model recs (`hybrid`, `svd`, `knn`)  
   - `GET /recommend/hybrid/{user_id}` – hybrid shortcut

## 2) Frontend setup (React, Vite)
1. `cd Frontend`
2. Install deps: `npm install`
3. Set API base if not localhost:  
   Create `Frontend/.env` → `VITE_API_BASE=http://127.0.0.1:8000`
4. Run dev server: `npm run dev` (open shown URL)
5. Production build: `npm run build` (output in `Frontend/dist`)

### Frontend UX
- Login: enter any existing user_id (from MovieLens data, e.g., `1`) to set personalization context.
- Home: Netflix-style rows showing Trending, Recommended For You (hybrid), Because You Watched (content-based similar), From viewers like you (collaborative), plus search.
- Movie detail: title/overview + “More like this” (content-based).
- Theme toggle: light/dark.

## 3) Data & models
- Data: `Backend/data/processed/final_movies.csv`, `final_ratings.csv` (MovieLens 100K).
- Pretrained artifacts: `ML_Models/svd`, `ML_Models/knn`, `ML_Models/content_based`.
- Training scripts (optional rerun):
  - `python -m ML_Models.svd.train_svd`
  - `python -m ML_Models.knn.train_knn`
  - `python -m ML_Models.content_based.train_content`
  - Or all at once: `python -m ML_Models.train_all`

## 4) Architecture notes
- Backend owns model selection; frontend only calls APIs and renders results.
- Content-based uses TF-IDF + cosine similarity on genres/overview.
- Collaborative includes memory-based KNN (precomputed similarities) and SVD embeddings.
- Hybrid blends collaborative + content for user-level recommendations.

## 5) Troubleshooting
- 404/422 on `/movie/search`: ensure server restarted after adding the search route.
- “Failed to fetch” in UI: check API is running and `VITE_API_BASE` points to it.
- Missing recs for a user/movie: item/user may be absent from trained IDs; try another id.
