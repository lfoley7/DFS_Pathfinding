
import random

def get_scenario():
    # For reproducibility
    random.seed(42)
    grid = [[random.randint(1, 5) for _ in range(10)] for _ in range(10)]
    return {
        "name": "Random Weights 10x10",
        "grid": grid,
        "start": (0, 0),
        "end": (9, 9)
    }
