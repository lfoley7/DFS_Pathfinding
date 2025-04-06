
def get_scenario():
    grid = [[1 for _ in range(10)] for _ in range(10)]
    return {
        "name": "Uniform 10x10 Grid",
        "grid": grid,
        "start": (0, 0),
        "end": (9, 9)
    }
