import sys
from sokoban_utils import load_sokoban, is_valid_move, directions

"""Implements Iterative Deepening Depth-First Seach."""
def iddfs_solve(grid, player_pos, box_pos, target_pos, walls):
    # Depth-limited search
    def dls(player, box, depth, path):
        # Base cases:
        if depth < 0: # Exceeded depth threshold
            return None
        if box == target_pos:
            return path
            
        # Try each direction
        for d in directions:
            new_player = (player[0] + d[0], player[1] + d[1])
            new_box = box
            
            # Skip invalid moves
            if not is_valid_move(new_player, walls):
                continue
                
            # Push box
            if new_player == box:
                new_box = (box[0] + d[0], box[1] + d[1])
                if not is_valid_move(new_box, walls):
                    continue
            
            # Skip if state reached
            new_state = (new_player, new_box)
            if new_state in reached:
                continue
                
            # Add to reached set
            reached.add(new_state)
            fringe.append(new_state)
            
            # Recursive DLS call
            result = dls(new_player, new_box, depth - 1, path + [(new_player, new_box)])
            if result is not None:
                return result
            
            fringe.pop()
            
        return None

    max_depth = 0
    states_visited = 0
    max_fringe_size = 0
    
    max_depth_limit = len(grid) * len(grid[0]) * 4  # approximation of |V| where |V| would be the total number of possible states
    
    while max_depth <= max_depth_limit:
        # Initialize fringe with initial state
        fringe = [(player_pos, box_pos)]
        # Initialize reached set with initial state
        reached = {(player_pos, box_pos)}
        
        # Call depth-limited search
        path = dls(player_pos, box_pos, max_depth, [])
        
        # Update stats
        states_visited += len(reached)
        max_fringe_size = max(max_fringe_size, len(fringe))
        
        # If goal found, calculate moves and return
        if path is not None:
            robot_moves = len(path)
            box_moves = sum(1 for i in range(len(path)) 
                          if i > 0 and path[i][1] != path[i-1][1])
            return {
                "algorithm": "IDDFS",
                "states_visited": states_visited,
                "max_fringe_size": max_fringe_size,
                "solution_found": True,
                "robot_moves": robot_moves,
                "box_moves": box_moves
            }
        
        max_depth += 1
    
    return {
        "algorithm": "IDDFS",
        "states_visited": states_visited,
        "max_fringe_size": max_fringe_size,
        "solution_found": False,
        "robot_moves": -1,
        "box_moves": -1
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sokoban_iddfs.py <puzzle_file>")
        sys.exit(1)
    
    puzzle_file = sys.argv[1]
    grid, player_pos, box_pos, target_pos, walls = load_sokoban(puzzle_file)
    result = iddfs_solve(grid, player_pos, box_pos, target_pos, walls)
    
    print("Search Summary:")
    print(f"Algorithm Used: {result['algorithm']}")
    print(f"States Visited: {result['states_visited']}")
    print(f"Max Fringe Size: {result['max_fringe_size']}")
    print(f"Solution Found: {'Yes' if result['solution_found'] else 'No'}")
    print(f"Robot Moves: {result['robot_moves']}")
    print(f"Box Moves: {result['box_moves']}")
