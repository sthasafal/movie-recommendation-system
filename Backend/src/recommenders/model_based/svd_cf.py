from recommenders.utils.matrix_builder import load_data, create_user_movie_matrix
from recommenders.memory_based.memory_cf import MemoryCF
from recommenders.model_based.svd_cf import SVD_CF

def run_collaborative():
    movies, ratings = load_data()
    matrix = create_user_movie_matrix(ratings)

    print("\n=== Memory-Based CF ===")
    mem = MemoryCF(matrix)
    print(mem.recommend_user_user(1, top_n=5))

    print("\n=== SVD CF ===")
    svd = SVD_CF(n_components=20)
    svd.fit(matrix)
    print(svd.recommend(1, matrix, top_n=5))

    print("\nCollaborative Filtering Completed!")

if __name__ == "__main__":
    run_collaborative()
