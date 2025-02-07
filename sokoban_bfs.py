import sys
from collections import deque
from sokoban_utils import load_sokoban, is_valid_move, directions

"""Implements Breadth-First Search."""
def bfs_solve(player_pos, box_pos, target_pos, walls):
    queue = deque([(player_pos, box_pos, 0, 0)])  # (player_pos, box_pos, box_moves, robot_moves)
    visited = set()
    visited.add((player_pos, box_pos))
    
    max_fringe_size = 1
    states_visited = 0
    
    while queue:
        max_fringe_size = max(max_fringe_size, len(queue))
        player, box, box_moves, robot_moves = queue.popleft()
        states_visited += 1

        # Return res if found
        if box == target_pos:
            return {
                "algorithm": "BFS",
                "states_visited": states_visited,
                "max_fringe_size": max_fringe_size,
                "solution_found": True,
                "box_moves": box_moves,
                "robot_moves": robot_moves
            }
        
        # Try each direction
        for d in directions:
            new_player = (player[0] + d[0], player[1] + d[1])
            
            # Skip invalid moves
            if not is_valid_move(new_player, walls):
                continue
            
            # Push box
            if new_player == box:
                new_box = (box[0] + d[0], box[1] + d[1])
                if not is_valid_move(new_box, walls):
                    continue
                new_state = (new_player, new_box)
                new_box_moves = box_moves + 1
            else:
                new_state = (new_player, box)
                new_box_moves = box_moves
            
            # Add state if not reached
            if new_state not in visited:
                visited.add(new_state)
                queue.append((*new_state, new_box_moves, robot_moves + 1))
    
    return {
        "algorithm": "BFS",
        "states_visited": states_visited,
        "max_fringe_size": max_fringe_size,
        "solution_found": False,
        "box_moves": -1,
        "robot_moves": -1
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sokoban_bfs.py <puzzle_file>")
        sys.exit(1)
    
    puzzle_file = sys.argv[1]
    grid, player_pos, box_pos, target_pos, walls = load_sokoban(puzzle_file)
    result = bfs_solve(player_pos, box_pos, target_pos, walls)
    
    print("Search Summary:")
    print(f"Algorithm Used: {result['algorithm']}")
    print(f"States Visited: {result['states_visited']}")
    print(f"Max Fringe Size: {result['max_fringe_size']}")
    print(f"Solution Found: {'Yes' if result['solution_found'] else 'No'}")
    print(f"Box Moves: {result['box_moves']}")
    print(f"Robot Moves: {result['robot_moves']}")
