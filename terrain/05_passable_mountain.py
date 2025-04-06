def get_scenario():
    size = 20
    # Start with moderate weights everywhere
    grid = [[5 for _ in range(size)] for _ in range(size)]
    
    # Create a mountain range in the middle columns
    mountain_col_start = 8
    mountain_col_end = 10
    mountain_height = 30
    
    # Create the mountain range
    for row in range(1, size-1):  # Skip first and last row
        for col in range(mountain_col_start, mountain_col_end+1):
            grid[row][col] = mountain_height
    
    # The direct path over the mountain will be shorter than going around
    # Going over: 10 steps of weight 5 + 3 steps of weight 10 = 80
    # Going around: 18 steps of weight 5 = 90
    
    return {
        "name": "Mountain Pass (20x20)",
        "grid": grid,
        "start": (10, 0),
        "end": (10, 19)
    }
