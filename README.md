# movie-recommendation-system

## Quick start

Backend (FastAPI):
1. `.\.venv\Scripts\Activate`
2. `uvicorn Backend.src.api.server:app --reload --port 8000`

Frontend (React + Vite):
1. `cd frontend`
2. `npm install` (first time)
3. `npm run dev` and open the shown localhost URL

Set `VITE_API_BASE` in `frontend/.env` if your API is not on `http://localhost:8000`.
