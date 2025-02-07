"""Loads the Sokoban grid and returns positions."""
def load_sokoban(filename):
    grid = []
    robot_pos, box_pos, target_pos = None, None, None
    walls = set()
    
    with open(filename, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            char = grid[row][col]
            if char == 'T':
                robot_pos = (row, col)
            elif char == 'B':
                box_pos = (row, col)
            elif char == '@':
                target_pos = (row, col)
            elif char == '#':
                walls.add((row, col))
    
    return grid, robot_pos, box_pos, target_pos, walls

"""Checks if a move is valid (not a wall)."""
def is_valid_move(pos, walls):
    return pos not in walls


"""Calculate Manhattan distance between two positions."""
def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]