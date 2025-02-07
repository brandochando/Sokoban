import sys
from heapq import heappush, heappop
from sokoban_utils import load_sokoban, is_valid_move, directions, distance

"""Calculate minimum possible robot moves needed to reach a pushing position (for admissability)."""
def min_robot_moves(player, box, walls):
    # Check all four pushing positions around the box
    min_dist = float('inf')
    for d in directions:
        push_pos = (box[0] - d[0], box[1] - d[1])  # Position needed to push box
        if is_valid_move(push_pos, walls):
            dist = distance(player, push_pos)
            min_dist = min(min_dist, dist)
    return min_dist if min_dist != float('inf') else 0

'''Implements A* Search'''
def astar_solve(player_pos, box_pos, target_pos, walls):
    # Using manhattan distance to box and target as heuristic
    initial_box_dist = distance(box_pos, target_pos)
    initial_robot_dist = min_robot_moves(player_pos, box_pos, walls)
    initial_state = (player_pos, box_pos)
    
    # g_scores now stores tuple (box_moves, robot_moves)
    g_scores = {initial_state: (0, 0)}
    # f_scores stores tuple (box_score, robot_score)
    f_scores = {initial_state: (initial_box_dist, initial_robot_dist)}
    
    pq = [((initial_box_dist, initial_robot_dist), (player_pos, box_pos, 0, 0))]
    visited = set()
    
    max_fringe_size = 1
    states_visited = 0
    
    while pq:
        max_fringe_size = max(max_fringe_size, len(pq))
        _, (player, box, box_moves, robot_moves) = heappop(pq)
        current_state = (player, box)
        
        # Continue if in visited
        if current_state in visited:
            continue
        
        # Add to states
        visited.add(current_state)
        states_visited += 1

        # Return res if found
        if box == target_pos:
            return {
                "algorithm": "A*",
                "states_visited": states_visited,
                "max_fringe_size": max_fringe_size,
                "solution_found": True,
                "box_moves": box_moves,
                "robot_moves": robot_moves
            }
        
        # Try each direction
        for d in directions:
            new_player = (player[0] + d[0], player[1] + d[1])
            new_box = box
            
            # Skip invalid moves
            if not is_valid_move(new_player, walls):
                continue
            
            # Calculate new costs
            new_robot_moves = robot_moves + 1
            new_box_moves = box_moves
            
            # Push box
            if new_player == box:
                new_box = (box[0] + d[0], box[1] + d[1])
                if not is_valid_move(new_box, walls):
                    continue
                new_box_moves += 1
            
            new_state = (new_player, new_box)
            new_g_score = (new_box_moves, new_robot_moves)
            
            # Skip if we've found a better path to this state
            if new_state in g_scores:
                old_g = g_scores[new_state]
                if new_g_score[0] > old_g[0] or (new_g_score[0] == old_g[0] and new_g_score[1] >= old_g[1]):
                    continue
            
            # This path is better - record it
            g_scores[new_state] = new_g_score
            h_box = distance(new_box, target_pos)
            h_robot = min_robot_moves(new_player, new_box, walls)
            f_scores[new_state] = (new_box_moves + h_box, new_robot_moves + h_robot)
            
            heappush(pq, (f_scores[new_state], 
                         (new_player, new_box, new_box_moves, new_robot_moves)))
    
    return {
        "algorithm": "A*",
        "states_visited": states_visited,
        "max_fringe_size": max_fringe_size,
        "solution_found": False,
        "box_moves": -1,
        "robot_moves": -1
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sokoban_astar.py <puzzle_file>")
        sys.exit(1)
    
    puzzle_file = sys.argv[1]
    grid, player_pos, box_pos, target_pos, walls = load_sokoban(puzzle_file)
    result = astar_solve(player_pos, box_pos, target_pos, walls)
    
    print("Search Summary:")
    print(f"Algorithm Used: {result['algorithm']}")
    print(f"States Visited: {result['states_visited']}")
    print(f"Max Fringe Size: {result['max_fringe_size']}")
    print(f"Solution Found: {'Yes' if result['solution_found'] else 'No'}")
    print(f"Box Moves: {result['box_moves']}")
    print(f"Robot Moves: {result['robot_moves']}")