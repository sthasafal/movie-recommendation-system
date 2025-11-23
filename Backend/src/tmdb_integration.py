from tmdbv3api import TMDb, Movie
from dotenv import load_dotenv
import pandas as pd
import os
import time

# ---- Load environment variables ----
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# ---- Setup TMDb API ----
tmdb = TMDb()
tmdb.api_key = API_KEY
tmdb.language = 'en'
movie_api = Movie()
print("Loaded key:", API_KEY[:6] + "********")  # to confirm it’s loaded


# ---- Load MovieLens movies ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "u.item")

print("Reading file from:", DATA_PATH)   # just to verify

movies = pd.read_csv(
    DATA_PATH,
    sep="|",
    encoding="latin-1",
    names=["movie_id", "title", "release_date", "IMDb_URL"],
    usecols=[0, 1, 2, 4],
    header=None
)

# ---- Fetch TMDb info ----
tmdb_info = []

for _, row in movies.iterrows():
    title = row['title'].split('(')[0].strip()
    try:
        results = movie_api.search(title)
        if results:
            first = results[0]
            tmdb_info.append({
                "movie_id": row["movie_id"],
                "title": row["title"],
                "tmdb_id": first.id,
                "poster_path": first.poster_path,
                "overview": first.overview,
                "vote_average": first.vote_average
            })
        else:
            tmdb_info.append({
                "movie_id": row["movie_id"],
                "title": row["title"],
                "tmdb_id": None,
                "poster_path": None,
                "overview": None,
                "vote_average": None
            })
    except Exception as e:
        # print(f"Error fetching {title}: {e}")
        print(f"Skipping {title} (invalid TMDb response)")

        time.sleep(0.2)

# ---- Save merged data ----
tmdb_df = pd.DataFrame(tmdb_info)
tmdb_df.to_csv('Backend/data/movies_with_tmdb.csv', index=False)
print("Enriched data saved safely without exposing API key.")
