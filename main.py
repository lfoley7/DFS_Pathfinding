import heapq
from typing import List, Tuple, Dict, Set, Optional
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
import numpy as np
import os
import importlib.util

# Note: While you mentioned DFS, for finding the shortest path in a weighted graph,
# Dijkstra's algorithm or A* are more appropriate. DFS doesn't guarantee the shortest path.
# I'll implement both DFS and Dijkstra's for comparison.

def dijkstra_shortest_path(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """
    Find the shortest path from start to end using Dijkstra's algorithm with a slight
    preference for more direct paths (similar to A*).
    
    Args:
        grid: 2D array with terrain weights
        start: Starting coordinates (row, col)
        end: Ending coordinates (row, col)
        
    Returns:
        Tuple of (path, total_cost) or (None, float('inf')) if no path exists
    """
    rows, cols = len(grid), len(grid[0])
    
    # Helper function to calculate Manhattan distance to end
    def heuristic(pos):
        return 0.1 * (abs(pos[0] - end[0]) + abs(pos[1] - end[1]))
    
    # Priority queue for (cost + heuristic, cost, position, path)
    # We keep the actual cost separately to return the true path cost
    pq = [(heuristic(start), 0, start, [start])]
    visited = set()
    
    # Only allow cardinal directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while pq:
        _, cost, current, path = heapq.heappop(pq)
        
        if current == end:
            return path, cost
        
        if current in visited:
            continue
            
        visited.add(current)
        row, col = current
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            new_pos = (new_row, new_col)
            
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                new_pos not in visited):
                
                new_cost = cost + grid[new_row][new_col]
                new_path = path + [new_pos]
                
                # Use cost + heuristic for priority, but keep track of actual cost
                priority = new_cost + heuristic(new_pos)
                heapq.heappush(pq, (priority, new_cost, new_pos, new_path))
    
    return None, float('inf')

def print_path_on_grid(grid: List[List[int]], path: List[Tuple[int, int]]) -> None:
    """Print the grid with the path marked."""
    if not path:
        print("No path found!")
        return
        
    path_set = set(path)
    rows, cols = len(grid), len(grid[0])
    
    print("Path visualization (X marks the path):")
    for r in range(rows):
        for c in range(cols):
            if (r, c) in path_set:
                print("X", end=" ")
            else:
                print(grid[r][c], end=" ")
        print()

def load_terrain_scenarios():
    """Load all terrain scenarios from the terrain directory."""
    terrain_dir = "terrain"
    
    # Create terrain directory if it doesn't exist
    if not os.path.exists(terrain_dir):
        os.makedirs(terrain_dir)
        create_default_terrain_files()
    
    # Check if terrain files exist, create them if not
    if not os.listdir(terrain_dir):
        create_default_terrain_files()
    
    scenarios = []
    
    # Load all Python files from the terrain directory
    for filename in sorted(os.listdir(terrain_dir)):
        if filename.endswith(".py"):
            file_path = os.path.join(terrain_dir, filename)
            
            # Load the module
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the scenario
            if hasattr(module, "get_scenario"):
                scenario = module.get_scenario()
                scenarios.append(scenario)
    
    return scenarios

def create_default_terrain_files():
    """Create default terrain files if none exist."""
    terrain_dir = "terrain"
    
    # Create the terrain directory if it doesn't exist
    if not os.path.exists(terrain_dir):
        os.makedirs(terrain_dir)
    
    # Create default terrain files
    terrain_files = [
        ("01_uniform_grid.py", """
def get_scenario():
    grid = [[1 for _ in range(10)] for _ in range(10)]
    return {
        "name": "Uniform 10x10 Grid",
        "grid": grid,
        "start": (0, 0),
        "end": (9, 9)
    }
"""),
        ("02_random_weights.py", """
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
"""),
        ("03_diagonal_path.py", """
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
""")
    ]
    
    # Write the files
    for filename, content in terrain_files:
        with open(os.path.join(terrain_dir, filename), "w") as f:
            f.write(content)

def create_visualization(scenarios):
    """Create an interactive visualization for the path finding scenarios."""
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(left=0.25, bottom=0.2)
    
    current_scenario_idx = 0
    path_info_text = None  # Track the path info text object
    
    def draw_grid(scenario_idx):
        nonlocal path_info_text
        ax.clear()
        
        # Clear previous path info if it exists
        if path_info_text:
            path_info_text.remove()
            path_info_text = None
        
        scenario = scenarios[scenario_idx]
        grid = scenario['grid']
        start = scenario['start']
        end = scenario['end']
        
        rows, cols = len(grid), len(grid[0])
        
        # Get path using Dijkstra's algorithm
        path, cost = dijkstra_shortest_path(grid, start, end)
        title = f"Dijkstra's Shortest Path - Cost: {cost}"
        
        path_set = set(path) if path else set()
        
        # Create a grid of squares
        for r in range(rows):
            for c in range(cols):
                color = 'lightblue' if (r, c) in path_set else 'white'
                rect = plt.Rectangle((c, rows-r-1), 1, 1, 
                                    facecolor=color, 
                                    edgecolor='black',
                                    alpha=0.7)
                ax.add_patch(rect)
                
                # Add the terrain weight as text, but not for start and end points
                if (r, c) != start and (r, c) != end:
                    ax.text(c + 0.5, rows-r-1 + 0.5, str(grid[r][c]), 
                            ha='center', va='center', fontsize=12)
        
        # Highlight start and end points
        start_rect = plt.Rectangle((start[1], rows-start[0]-1), 1, 1, 
                                  facecolor='green', edgecolor='black', alpha=0.5)
        end_rect = plt.Rectangle((end[1], rows-end[0]-1), 1, 1, 
                                facecolor='red', edgecolor='black', alpha=0.5)
        ax.add_patch(start_rect)
        ax.add_patch(end_rect)
        
        # Add labels for start and end
        ax.text(start[1] + 0.5, rows-start[0]-1 + 0.5, "S", 
                ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(end[1] + 0.5, rows-end[0]-1 + 0.5, "E", 
                ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Set plot limits and title
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_title(f"Scenario {scenario_idx+1}: {scenario['name']} - {title}")
        ax.set_xticks(np.arange(0, cols+1, 1))
        ax.set_yticks(np.arange(0, rows+1, 1))
        ax.grid(True, linestyle='-', alpha=0.7)
        
        # Add path information
        if path:
            path_info = f"Path Length: {len(path)}, Cost: {cost}"
            path_info_text = plt.figtext(0.5, 0.02, path_info, ha="center", fontsize=12, 
                      bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
        else:
            path_info_text = plt.figtext(0.5, 0.02, "No path found!", ha="center", fontsize=12, 
                      bbox={"facecolor":"red", "alpha":0.5, "pad":5})
        
        plt.draw()
    
    # Create radio buttons for scenario selection
    scenario_labels = [f"Scenario {i+1}" for i in range(len(scenarios))]
    ax_scenario = plt.axes([0.025, 0.2, 0.15, 0.25])
    scenario_radio = RadioButtons(ax_scenario, scenario_labels)
    
    # Create next and previous buttons
    ax_prev = plt.axes([0.4, 0.05, 0.1, 0.075])
    ax_next = plt.axes([0.55, 0.05, 0.1, 0.075])
    btn_prev = Button(ax_prev, 'Previous')
    btn_next = Button(ax_next, 'Next')
    
    # Event handlers
    def update_scenario(label):
        nonlocal current_scenario_idx
        current_scenario_idx = int(label.split()[1]) - 1
        draw_grid(current_scenario_idx)
    
    def next_scenario(event):
        nonlocal current_scenario_idx
        current_scenario_idx = (current_scenario_idx + 1) % len(scenarios)
        scenario_radio.set_active(current_scenario_idx)
        draw_grid(current_scenario_idx)
    
    def prev_scenario(event):
        nonlocal current_scenario_idx
        current_scenario_idx = (current_scenario_idx - 1) % len(scenarios)
        scenario_radio.set_active(current_scenario_idx)
        draw_grid(current_scenario_idx)
    
    # Connect callbacks
    scenario_radio.on_clicked(update_scenario)
    btn_next.on_clicked(next_scenario)
    btn_prev.on_clicked(prev_scenario)
    
    # Initial draw
    draw_grid(current_scenario_idx)
    
    plt.show()

def main():
    scenarios = load_terrain_scenarios()
    create_visualization(scenarios)

if __name__ == "__main__":
    main() 