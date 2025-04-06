
import random
import math

def get_scenario():
    random.seed(44)  # Different seed
    size = 50
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    # Create a road network (low weights)
    # Horizontal roads
    for y in [10, 25, 40]:
        for x in range(size):
            grid[y][x] = 1
    
    # Vertical roads
    for x in [10, 25, 40]:
        for y in range(size):
            grid[y][x] = 1
    
    # Create forests (medium weights)
    num_forests = 5
    for _ in range(num_forests):
        forest_x = random.randint(5, size-6)
        forest_y = random.randint(5, size-6)
        forest_size = random.randint(3, 8)
        
        for dx in range(-forest_size, forest_size+1):
            for dy in range(-forest_size, forest_size+1):
                x, y = forest_x + dx, forest_y + dy
                if 0 <= x < size and 0 <= y < size:
                    # Forest density decreases from center
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < forest_size:
                        density = 4 - int(2 * distance / forest_size)
                        grid[y][x] = max(grid[y][x], density)
    
    # Create mountains (high weights)
    num_mountains = 3
    for _ in range(num_mountains):
        mountain_x = random.randint(10, size-11)
        mountain_y = random.randint(10, size-11)
        mountain_size = random.randint(4, 7)
        
        for dx in range(-mountain_size, mountain_size+1):
            for dy in range(-mountain_size, mountain_size+1):
                x, y = mountain_x + dx, mountain_y + dy
                if 0 <= x < size and 0 <= y < size:
                    # Mountain height decreases from center
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < mountain_size:
                        height = 9 - int(6 * distance / mountain_size)
                        grid[y][x] = max(grid[y][x], height)
    
    # Create a lake (impassable)
    lake_x = random.randint(15, size-16)
    lake_y = random.randint(15, size-16)
    lake_size = random.randint(5, 8)
    
    for dx in range(-lake_size, lake_size+1):
        for dy in range(-lake_size, lake_size+1):
            x, y = lake_x + dx, lake_y + dy
            if 0 <= x < size and 0 <= y < size:
                # Lake is circular
                distance = math.sqrt(dx**2 + dy**2)
                if distance < lake_size:
                    grid[y][x] = 9
    
    return {
        "name": "Complex Terrain (50x50)",
        "grid": grid,
        "start": (10, 10),
        "end": (35, 35)
    }
