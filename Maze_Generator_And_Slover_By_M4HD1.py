import pygame
import random
import sys
import heapq

#By M4HD1
#Follow me on github :)

pygame.init()

WIDTH, HEIGHT = 1000, 1000 # width and height screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator and Solver")

build_time = 1 # Build time (by step) (ms)
path_finding_time = 1 # Slove time (by step) (ms)

BLACK = (0, 0, 0)  # Wall color
GREEN = (0, 255, 0)  # Path color
RED = (255, 0, 0)  # Path found color
BLUE = (0, 0, 255)  # Open nodes (currently being explored)
WHITE = (255, 255, 255)  # Processing nodes
PURPLE = (128, 0, 128)  # Starting and ending points

GRID_SIZE = 5
cols = WIDTH // GRID_SIZE
rows = HEIGHT // GRID_SIZE

# Maze grid: 0 = wall, 1 = path
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Stack for DFS (for maze generation)
stack = []

# Directions for DFS (right, down, left, up)
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Maze Generator with DFS
def generate_maze(x, y):
    grid[y][x] = 1
    stack.append((x, y))

    while stack:
        current_x, current_y = stack[-1]
        neighbors = []

        for dx, dy in directions:
            nx, ny = current_x + dx * 2, current_y + dy * 2
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            grid[ny][nx] = 1
            grid[current_y + (ny - current_y) // 2][current_x + (nx - current_x) // 2] = 1
            stack.append((nx, ny))
        else:
            stack.pop()

        draw_maze()
        pygame.display.flip()
        pygame.time.delay(build_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# A* Algorithm to find the shortest path with incremental steps
def a_star(start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    closed_list = set()
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Reverse the path to go from start to end
            return path

        closed_list.add(current)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows) or grid[neighbor[1]][neighbor[0]] == 0:
                continue

            if neighbor in closed_list:
                continue

            tentative_g_score = g_score.get(current, float('inf')) + 1

            if neighbor not in [i[1] for i in open_list]:
                heapq.heappush(open_list, (f_score.get(neighbor, float('inf')), neighbor))

            if tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)

        draw_maze(open_list, closed_list)  # Draw the current search state
        pygame.display.flip()
        pygame.time.delay(path_finding_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return []  # No path found

# Draw the maze and the search progress (open nodes, closed nodes, and path)
def draw_maze(open_list=None, closed_list=None):
    if open_list is None:
        open_list = []
    if closed_list is None:
        closed_list = []

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0:  # Wall
                color = BLACK
            elif grid[y][x] == 1:  # Path
                color = GREEN
            else:
                color = GREEN  # Default to green for paths
            pygame.draw.rect(SCREEN, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Highlight the open nodes being processed (in blue)
    for _, node in open_list:
        pygame.draw.rect(SCREEN, BLUE, (node[0] * GRID_SIZE, node[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Highlight the closed nodes (in white)
    for node in closed_list:
        pygame.draw.rect(SCREEN, WHITE, (node[0] * GRID_SIZE, node[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Draw the red path (once found)
def draw_path(path):
    for (x, y) in path:
        pygame.draw.rect(SCREEN, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(SCREEN, RED, (0, 0, GRID_SIZE, GRID_SIZE))

# Main game loop
def main():
    generate_maze(0, 0)  # Start generating from the top-left corner

    # Set start and end points
    start = (0, 0)
    end = (cols - 2, rows - 2)

    # Make sure the end point is a path
    if grid[end[1]][end[0]] == 0:
        grid[end[1]][end[0]] = 1

    # A* to solve the maze
    path = a_star(start, end)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill(BLACK)  # Fill the screen with black (background)
        draw_maze()  # Draw the maze and open nodes

        if path:
            draw_path(path)  # Draw the path in red once it's found
        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    main()
