"""
Project bootstrap for Python imports.

We keep the Backend/src directory and the repository root on sys.path so that
absolute imports like `recommenders...` and `ML_Models...` resolve no matter
where the app is run from (uvicorn, notebooks, or ad-hoc scripts).
"""

from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent.parent  # repository root

for path in (SRC_DIR, ROOT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
