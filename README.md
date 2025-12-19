# Movie Recommendation System

FastAPI backend + pre-trained ML models + React frontend. Supports legacy MovieLens 100K and newer MovieLens datasets (20M/25M/32M style).

## Prerequisites
- Python 3.11+ (virtualenv recommended)
- Node 18+

## Backend setup
1. Create/activate venv  
   `python -m venv .venv`  
   `.\.venv\Scripts\Activate`
2. Install deps  
   `pip install -r Backend/requirements.txt`
3. Run API  
   `uvicorn Backend.src.api.server:app --reload --port 8000`
4. Key endpoints  
   - `GET /health/` — heartbeat  
   - `GET /movie/search?q=toy&limit=10` — title search  
   - `GET /movie/{movie_id}` — details  
   - `GET /recommend/similar/{movie_id}?top_n=10` — content-based  
   - `GET /recommend/model/{model}/{user_id}?top_n=10` — per-model recs (`hybrid`, `svd`, `knn`)  
   - `GET /recommend/hybrid/{user_id}` — hybrid shortcut

## Frontend setup (React, Vite)
1. `cd Frontend`
2. `npm install`
3. If API not on localhost: create `Frontend/.env` with `VITE_API_BASE=http://127.0.0.1:8000`
4. Dev: `npm run dev` (open shown URL)  
   Build: `npm run build`

### Frontend UX
- Login with any valid `user_id` from the dataset.
- Home rows: Trending (popularity), Recommended For You (hybrid), Because You Watched (content-based similar), From viewers like you (collaborative), plus search.
- Movie detail: info + “More like this” (content-based).
- Theme toggle: light/dark.

## Data & models
- Processed data: `Backend/data/processed/final_movies.csv`, `final_ratings.csv`.
- Models: `ML_Models/svd` (SVD factors), `ML_Models/knn` (KNN similarities), `ML_Models/content_based` (TF-IDF + cosine).
- Training scripts:  
  - `python -m ML_Models.svd.train_svd`  
  - `python -m ML_Models.knn.train_knn`  
  - `python -m ML_Models.content_based.train_content`  
  - All at once: `python -m ML_Models.train_all`

## Architecture notes
- Backend chooses models; frontend only calls APIs.
- Content-based uses TF-IDF over genres/overview.
- Collaborative: memory-based KNN + SVD factors.
- Hybrid blends collaborative + content for user-level recs.

## Using a newer MovieLens dataset (20M/25M/32M)
1. Download `movies.csv`, `ratings.csv`, `links.csv`.
2. Place them in `Backend/data/ml-32m/` (keep filenames).
3. Regenerate processed data:  
   `python Backend/src/preprocess_final.py`
4. Retrain models on the new data:  
   `python -m ML_Models.train_all`
5. Restart the API.

The preprocessing script auto-detects `Backend/data/ml-32m/` and rebuilds the processed files. Content training reads the `genres` column directly, so no extra changes are needed.

## Troubleshooting
- 404/422 on `/movie/search`: restart the server to load routes.
- “Failed to fetch” in UI: ensure API is running and `VITE_API_BASE` matches.
- Missing recs: user/movie may not exist in trained IDs; try another id.
