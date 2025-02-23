import time
import tracemalloc

board = []
trace = []
resTrace = tuple()
startPoint = None
directions = [(1, 0), (-1, 0), (0, 1),  (0, -1),]
circleCount = 0
done = False

def load_input(path):
    global board, size
    with open(path) as f:
        size = int(f.readline().strip())

        for _ in range(size):  
            line = f.readline().strip().split() 
            board.append([int(num) for num in line])  

    
def init():
    global startPoint
    global circleCount

    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                if startPoint is None: startPoint = (i, j)
                circleCount += 1
                

def isStraight(i,j, x, y): # pre and next node
    if i == x or j == y: return True
    return False

def validMove(pre_i, pre_j, i, j, mode):
    #Mode:
    # 0: every where
    # 1: go straingt
    # 2: turn off
    nextPoints = []
    for (dx, dy) in directions:
        x = i + dx
        y = j + dy
        # print(f"Pre I J {i} - {j}")
        # print(f"X - Y: {x} - {y}")
        preStraight = isStraight(pre_i, pre_j, x, y)
        if not validPos(x,y): continue
        if mode == 0:
            nextPoints.append((x,y))
        elif mode == 1:
            
            if preStraight:
                nextPoints.append((x, y))
        elif mode == 2:
            if not preStraight:
                nextPoints.append((x, y))
    
    return nextPoints
        



def validPos(i, j):
    if (i < 0 or i >= size): return False
    if (j < 0 or j >= size): return False
    if (i,j) != startPoint and   visited[i][j]: return False
    return True

def DFS(i, j, count, needStrainght, needTurn):
    global done
    global trace
    global resTrace
    global visited

   # print(f"---- AT {i}  -   {j} ---------")
    #print(f"Count = {count}")
    visited[i][j] = 1
    trace.append((i,j))

    if count == 0 and i == startPoint[0] and j == startPoint[1]:
        preIsStraight = isStraight(trace[-3][0], trace[-3][1], i, j)
        firstIsStraight = isStraight(trace[0][0], trace[0][1], trace[2][0], trace[2][1])
        starEndStraight = isStraight(trace[-2][0], trace[-2][1], trace[1][0], trace[1][1])
        stop = False
        if board[i][j] < 0:
            if not starEndStraight and preIsStraight and firstIsStraight:
                stop = True
           
        else:
            if starEndStraight and not (preIsStraight and firstIsStraight):
                stop = True
        if stop:
            done = True
            resTrace = tuple(trace)
            return
    
    mode = needStrainght * 1 + needTurn * 2

    if mode >=3:
        visited[i][j] = 0
        trace.pop()
        return

    willTurn = False
    willStraight = False
    goBack = False
    nextCount = count - (board[i][j] != 0)
    

    if board[i][j] < 0: #Must Turn - Will Straight - Must PreTurn
        if len(trace) > 2:
            if  isStraight(trace[-3][0], trace[-3][1], i, j) :
                
                goBack = needStrainght
                   
            else:
                goBack = True
        willStraight = True
        mode = 2 
        

    elif board[i][j] > 0: #Must Straight - Maybe will Turn
        if len(trace)> 2:
            if  isStraight(trace[-3][0], trace[-3][1], i, j):
                willTurn = True
            goBack = needTurn
        mode = 1

    
    
    if not goBack:
        preI = 0
        preJ = 0

        if len(trace) > 1:
            preI =  trace[-2][0]
            preJ = trace[-2][1]
        else:
            mode = 0

        validMoveArr = validMove(preI , preJ, i, j, mode)
        for (x,y) in validMoveArr:
            if done: return
            DFS(x, y, nextCount, willStraight, willTurn)
            
    
    visited[i][j] = 0
    trace.pop()

    
def reset():
    global trace
    global done
    global visited

    trace = []    
    done = False
    visited  = [[0 for i in range(size)] for j in range(size)]


def findSolution():
    reset()
 
    DFS(startPoint[0], startPoint[1], circleCount, 0 , 0)
    if done:
        print("FOUND SOLUTION! ")
        print(resTrace)
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
    
    load_input("input/input1.txt")
    init()
    measure_performance(findSolution)
    
    
    
   
    
    


