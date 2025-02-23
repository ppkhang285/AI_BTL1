import sys

# Directions: Up, Right, Down, Left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def load_input(filename):
    """Loads the board from the input file."""
    try:
        with open(filename, "r") as f:
            size = int(f.readline().strip())
            board = [list(map(int, f.readline().strip().split())) for _ in range(size)]
        return size, board
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)


def is_straight(x1, y1, x2, y2):
    """Checks if two points are aligned either horizontally or vertically."""
    return x1 == x2 or y1 == y2


def valid_pos(x, y, size, visited):
    """Checks if a position is within bounds and not visited."""
    return 0 <= x < size and 0 <= y < size and not visited[x][y]


def find_start_number(board, size):
    """Finds the smallest absolute value number to start."""
    start = None
    number_list = []
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                number_list.append((board[i][j], (i, j)))
                if start is None or abs(board[i][j]) < abs(start[0]):
                    start = (board[i][j], (i, j))
    return start, number_list


def dfs(board, size, x, y, curr_len, max_len, number_left, visited, path, res_path, start, start_length, done):
    """Depth-first search to find the loop."""
    if done[0]:  # Stop if solution is found
        return
    
    print(x,y)

    if max_len is not None and curr_len > max_len:
        return
    
    # Loop condition: Back to start with correct length
    if (x, y) == start[1] and curr_len + start_length == abs(board[x][y]):
        if number_left == 0:
            res_path[:] = path[:]
            done[0] = True
        return

    visited[x][y] = True

    # Explore neighbors
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if not valid_pos(nx, ny, size, visited):
            continue
        
        path.append((nx, ny))
        
        if len(path) < 2:
            # First move, no restriction
            dfs(board, size, nx, ny, curr_len + 1, max_len, number_left, visited, path, res_path, start, start_length, done)
        
        elif board[x][y] != 0:
            # Numbered node: apply white/black rules
            if board[x][y] > 0:  # White circle (straight line)
                if is_straight(path[-2][0], path[-2][1], nx, ny):
                    dfs(board, size, nx, ny, curr_len + 1, board[x][y] - curr_len, number_left - 1, visited, path, res_path, start, start_length, done)
            else:  # Black circle (must turn)
                if not is_straight(path[-2][0], path[-2][1], nx, ny):
                    dfs(board, size, nx, ny, 1, abs(board[x][y]) - curr_len, number_left - 1, visited, path, res_path, start, start_length, done)

        else:
            # Empty slot movement
            if curr_len == max_len:  # Must turn
                if not is_straight(path[-2][0], path[-2][1], nx, ny):
                    dfs(board, size, nx, ny, 1, None, number_left, visited, path, res_path, start, start_length, done)
            else:
                dfs(board, size, nx, ny, curr_len + 1, max_len, number_left, visited, path, res_path, start, start_length, done)
        
        path.pop()
    
    visited[x][y] = False


def solve_shingoki(filename):
    """Solves the Shingoki puzzle."""
    size, board = load_input(filename)
    start, number_list = find_start_number(board, size)
    
    if not start:
        print("No numbers found on the board.")
        return
    
    visited = [[False] * size for _ in range(size)]
    path = [start[1]]
    res_path = []
    done = [False]  # Mutable flag

    for start_length in range(1, abs(start[0])):
        if done[0]:
            break
        dfs(board, size, start[1][0], start[1][1], 0, start_length, len(number_list) - 1, visited, path, res_path, start, start_length, done)

    print("Solution Path:", res_path)


if __name__ == "__main__":
    solve_shingoki("input/input0.txt")
