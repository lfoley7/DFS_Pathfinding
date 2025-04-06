
def get_scenario():
    size = 20
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    # Create two mountain ranges
    # Mountain 1 (vertical barrier)
    for i in range(5, 15):
        for j in range(7, 9):
            grid[i][j] = 9
    
    # Mountain 2 (horizontal barrier)
    for i in range(12, 14):
        for j in range(10, 18):
            grid[i][j] = 9
    
    return {
        "name": "Two Mountains (20x20)",
        "grid": grid,
        "start": (4, 6),
        "end": (14, 16)
    }
