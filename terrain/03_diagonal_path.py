
def get_scenario():
    size = 10
    grid = [[5 for _ in range(size)] for _ in range(size)]
    
    # Create a diagonal path with lower weights
    for i in range(size):
        grid[i][i] = 1
    
    return {
        "name": "Diagonal Path",
        "grid": grid,
        "start": (0, 0),
        "end": (9, 9)
    }
