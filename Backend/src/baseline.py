import pandas as pd
import matplotlib.pyplot as plt

ratings = pd.read_csv('Backend/data/u.data', sep='\t', names=["user_id", "movie_id", "rating", "timestamp"])
columns = ["movie_id", "title", "release_date", "IMDb_URL"]
movies = pd.read_csv('Backend/data/u.item', sep='|', encoding='latin-1', names=columns, usecols=[0, 1, 2, 4], header=None)

# Merge datasets
data = pd.merge(ratings, movies, on="movie_id")

# --- Global average ---
global_avg = data['rating'].mean()
print(f"Global average rating: {global_avg:.2f}")

# --- Top 10 movies by average rating ---
top_movies = (
    data.groupby('title')['rating']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 movies by average rating:")
print(top_movies)
top_movies.to_csv('Backend/data/top_movies.csv')


plt.hist(data['rating'], bins=5, edgecolor='black')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()
