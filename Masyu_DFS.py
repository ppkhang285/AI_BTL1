import time
import tracemalloc



class MasyuDFS:
    def __init__(self, path):
        
        self.board = []
        self.visited = []
        self.trace = []
        self.resTrace = tuple()
        self.startPoint = (0, 0)
        self.directions = [(1, 0), (-1, 0), (0, 1),  (0, -1),]
        self.circleCount = 0
        self.done = False
        self.size = 0

        self.load_input(path)
        self.init()

    def load_input(self,path):
        with open(path) as f:
            self.size = int(f.readline().strip())

            for _ in range(self.size):  
                line = f.readline().strip().split() 
                self.board.append([int(num) for num in line])  

    
    def init(self):

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    if self.startPoint is None: self.startPoint = (i, j)
                    self.circleCount += 1
                

    def isStraight(self, i,j, x, y): # pre and next node
        if i == x or j == y: return True
        return False

    def validMove(self, pre_i, pre_j, i, j, mode):
        #Mode:
        # 0: every where
        # 1: go straingt
        # 2: turn off
        nextPoints = []
        for (dx, dy) in self.directions:
            x = i + dx
            y = j + dy
            # print(f"Pre I J {i} - {j}")
            # print(f"X - Y: {x} - {y}")
            preStraight = self.isStraight(pre_i, pre_j, x, y)
            if not self.validPos(x,y): continue
            if mode == 0:
                nextPoints.append((x,y))
            elif mode == 1:
                
                if preStraight:
                    nextPoints.append((x, y))
            elif mode == 2:
                if not preStraight:
                    nextPoints.append((x, y))
        
        return nextPoints
        



    def validPos(self, i, j):
        if (i < 0 or i >= self.size): return False
        if (j < 0 or j >= self.size): return False
        if (i,j) != self.startPoint and   self.visited[i][j]: return False
        return True

    def DFS(self, i, j, count, needStrainght, needTurn):

        
       
        self.visited[i][j] = 1
        self.trace.append((i,j))

        if count == 0 and i == self.startPoint[0] and j == self.startPoint[1]:
            preIsStraight = self.isStraight(self.trace[-3][0], self.trace[-3][1], i, j)
            firstIsStraight = self.isStraight(self.trace[0][0], self.trace[0][1], self.trace[2][0], self.trace[2][1])
            starEndStraight = self.isStraight(self.trace[-2][0], self.trace[-2][1], self.trace[1][0], self.trace[1][1])
            stop = False
            if self.board[i][j] < 0:
                if not starEndStraight and preIsStraight and firstIsStraight:
                    stop = True
            
            else:
                if starEndStraight and not (preIsStraight and firstIsStraight):
                    stop = True
            if stop:
                self.done = True
                self.resTrace = tuple(self.trace)
                return
        
        mode = needStrainght * 1 + needTurn * 2

        if mode >=3:
            self.visited[i][j] = 0
            self.trace.pop()
            return

        willTurn = False
        willStraight = False
        goBack = False
        nextCount = count - (self.board[i][j] != 0)
        

        if self.board[i][j] < 0: #Must Turn - Will Straight - Must PreTurn
            if len(self.trace) > 2:
                if  self.isStraight(self.trace[-3][0], self.trace[-3][1], i, j) :
                    
                    goBack = needStrainght
                    
                else:
                    goBack = True
            willStraight = True
            mode = 2 
            

        elif self.board[i][j] > 0: #Must Straight - Maybe will Turn
            if len(self.trace)> 2:
                if  self.isStraight(self.trace[-3][0], self.trace[-3][1], i, j):
                    willTurn = True
                goBack = needTurn
            mode = 1

        
        
        if not goBack:
            preI = 0
            preJ = 0

            if len(self.trace) > 1:
                preI =  self.trace[-2][0]
                preJ = self.trace[-2][1]
            else:
                mode = 0

            validMoveArr = self.validMove(preI , preJ, i, j, mode)
            for (x,y) in validMoveArr:
                if self.done: return
                self.DFS(x, y, nextCount, willStraight, willTurn)
                
        
        self.visited[i][j] = 0
        self.trace.pop()

    
    def reset(self):


        self.trace = []    
        self.done = False
        self.visited  = [[0 for i in range(self.size)] for j in range(self.size)]


    def findSolution(self):
        self.reset()
    
        self.DFS(self.startPoint[0], self.startPoint[1], self.circleCount, 0 , 0)
        if self.done:
            print("FOUND SOLUTION! ")
            print(self.resTrace)
        else:
            print("SOLUTION NOT FOUND")


def measure_performance(func, *args, **kwargs):
    tracemalloc.start()
    start_time = time.perf_counter()

    result = func(*args, **kwargs)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Thời gian chạy: {end_time - start_time:.6f} giây")
    print(f"Dung lượng bộ nhớ hiện tại: {current / 1024:.2f} KB")
    print(f"Dung lượng bộ nhớ tối đa: {peak / 1024:.2f} KB")

    return result

if __name__=="__main__":
    
    dfs = MasyuDFS("input/input1.txt")

    measure_performance(dfs.findSolution)
    
    
    
   
    
    


