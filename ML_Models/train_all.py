import os

print("Training SVD model...")
os.system("python ./svd/train_svd.py")

print("Training Content-Based Model...")
os.system("python ./content_based/train_content.py")

print("Training KNN Similarity...")
os.system("python ./knn/train_knn.py")

print("All models trained successfully!")

