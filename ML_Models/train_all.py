import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
PYTHON = sys.executable


def run(module: str):
    """Run a training module from repo root so ML_Models package is resolvable."""
    subprocess.run(
        [PYTHON, "-m", module],
        cwd=ROOT_DIR,
        check=True,
    )


def main():
    print("Training SVD model...")
    run("ML_Models.svd.train_svd")

    print("Training Content-Based model...")
    run("ML_Models.content_based.train_content")

    print("Training KNN similarities...")
    # run("ML_Models.knn.train_knn")

    print("All models trained successfully!")


if __name__ == "__main__":
    main()

