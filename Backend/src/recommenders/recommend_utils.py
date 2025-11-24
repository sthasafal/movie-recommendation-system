import numpy as np

def normalize_scores(scores):
    """
    Normalize scores between 0 and 1.
    Accepts dict {movie_id: score} or list/array.
    """
    if isinstance(scores, dict):
        values = np.array(list(scores.values()))
    else:
        values = np.array(scores)

    if values.max() == values.min():
        return {k: 0.0 for k in scores} if isinstance(scores, dict) else np.zeros(len(values))

    normalized = (values - values.min()) / (values.max() - values.min())

    if isinstance(scores, dict):
        return {k: float(v) for k, v in zip(scores.keys(), normalized)}

    return normalized
