
import random

def get_scenario():
    random.seed(43)  # Different seed
    size = 50
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    # Create a winding river
    river_x = 25
    for y in range(size):
        # Make the river meander
        river_x += random.randint(-1, 1)
        river_x = max(5, min(size-6, river_x))
        
        # Create the river (width of 3)
        for dx in range(-1, 2):
            if 0 <= river_x + dx < size:
                grid[y][river_x + dx] = 7
    
    # Create a mountain range
    mountain_y = 25
    for x in range(size):
        # Make the mountain range vary in position
        mountain_y += random.randint(-1, 1)
        mountain_y = max(5, min(size-6, mountain_y))
        
        # Create the mountain range (width of 5)
        for dy in range(-2, 3):
            if 0 <= mountain_y + dy < size:
                # Higher in the center
                height = 9 - abs(dy)
                grid[mountain_y + dy][x] = height
    
    return {
        "name": "River and Mountain (50x50)",
        "grid": grid,
        "start": (5, 5),
        "end": (45, 45)
    }
