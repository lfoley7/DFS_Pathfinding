
import random
import math

def get_scenario():
    random.seed(42)  # For reproducibility
    size = 50
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    # Create several hills/mountains
    num_features = 8
    features = []
    
    for _ in range(num_features):
        # Random center point
        center_x = random.randint(5, size-6)
        center_y = random.randint(5, size-6)
        # Random radius
        radius = random.randint(3, 10)
        # Random height (1-9)
        height = random.randint(3, 9)
        features.append((center_x, center_y, radius, height))
    
    # Apply features to the grid
    for i in range(size):
        for j in range(size):
            for center_x, center_y, radius, height in features:
                # Calculate distance from feature center
                distance = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                if distance < radius:
                    # Apply height based on distance from center
                    weight = max(1, int(height * (1 - distance/radius)))
                    grid[i][j] = max(grid[i][j], weight)
    
    return {
        "name": "Hills and Valleys (50x50)",
        "grid": grid,
        "start": (3, 5),
        "end": (33, 42)
    }
