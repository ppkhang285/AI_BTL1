def load_input(path):
    board = []
    with open(path) as f:
        size = int(f.readline().strip())
        for _ in range(size):  
            line = f.readline().strip().split() 
            board.append([int(num) for num in line])
    return board