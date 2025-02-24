from queue import PriorityQueue

class AStar:
    def __init__(self, path):
        self.board = []
        self.path = []
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        open_list = PriorityQueue()

 
    def load_input(self, path):
        with open(path) as f:
            size = int(f.readline().strip())

            for _ in range(size):  
                line = f.readline().strip().split() 
                self.board.append([int(num) for num in line])  
    
        
