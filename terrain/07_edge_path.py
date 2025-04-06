
def get_scenario():
    size = 20
    # Start with high weights everywhere
    grid = [[8 for _ in range(size)] for _ in range(size)]
    
    # Create low-weight path along the edges
    for i in range(size):
        grid[0][i] = 1  # Top edge
        grid[size-1][i] = 1  # Bottom edge
        grid[i][0] = 1  # Left edge
        grid[i][size-1] = 1  # Right edge
    
    # Make the center extremely high weight
    for i in range(2, size-2):
        for j in range(2, size-2):
            grid[i][j] = 15
    
    return {
        "name": "Edge Path (20x20)",
        "grid": grid,
        "start": (10, 0),
        "end": (10, 19)
    }
