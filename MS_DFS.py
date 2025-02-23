import time
import tracemalloc




board = []
numberList = [] # List<( value , (i,j)  ) >
startNumber = None
startLength = 0
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
trace = []
resTrace = []
done = False

def load_input():
    global board, size
    with open("input/input0.txt") as f:
        size = int(f.readline().strip())

        for _ in range(size):  
            line = f.readline().strip().split() 
            board.append([int(num) for num in line])  

    
def init():
    global numberList
    global board
    global startNumber
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                numberList.append((board[i][j],(i,j)))
                if startNumber is None or startNumber[0] > abs(board[i][j]):
                    startNumber = (board[i][j],(i,j))



def isStraight(i,j, x, y): # pre and next node
    if i == x or j == y: return True
    return False

def validPos(i, j ):
    global size
    global visited
    if (i < 0 or i >= size): return False
    if (j < 0 or j >= size): return False
    if visited[i][j]: return False
    return True

def DFS(i, j, currLen, maxLen, numberLeft):
    global board
    global visited
    global trace
    global startNumber
    global directions
    global startLength
    global done
    global resTrace

    print(f"{i}  {j}\n")
    if done: return

    
    if maxLen is not None and currLen > maxLen: return

    if i == startNumber[1][0] and j == startNumber[1][1]:
        #Check if startNumber valid
        if numberLeft > 0 and len(trace) > 1: return
        if currLen + startLength == abs(board[i][j]):
            resTrace = trace.copy()
            done = True
            return

    visited[i][j] = 1
    
    
    # 2nd Node -> Chillig
    if (len(trace)< 2):
        for (dx, dy) in directions:
            x = i + dx
            y = i + dy
            if not validPos(x,y): continue
            trace.append((x,y))
            DFS(x,y, currLen+1, maxLen, numberLeft)
            trace.pop()
    
    # Travel at Number Slot
    elif board[i][j] != 0:
        if currLen >= abs(board[i][j]): 
            visited[i][j] = 0
            return
        # White number
        if board[i][j] > 0:
            if maxLen is not None and (board[i][j] != maxLen): 
                visited[i][j] = 0
                return

            for (dx, dy) in directions:
                x = i + dx
                y = j + dy
                if not validPos(x,y): continue
                if isStraight(trace[-2][0], trace[-2][1], x, y):
                    trace.append((x,y))
                    DFS(x, y, currLen+1, board[i][j] - currLen, numberLeft-1)
                    trace.pop()

        else: # Black number
            # If not reach need len (maxLen) when go here -> Return
            if currLen is not None and currLen != maxLen: 
                visited[i][j] = 0
                return
            for (dx, dy) in directions:
                x = i + dx
                y = j + dy
                if not validPos(x,y): continue
                if not isStraight(trace[-2][0], trace[-2][1], x, y):
                    trace.append((x,y))
                    DFS(x, y, 1, abs(board[i][j]) - currLen, numberLeft-1)
                    trace.pop() 


    # Travel at empty Slot:
    else:
        # Reach maxLen -> Turn
        if currLen == maxLen:
            for (dx, dy) in directions:
                x = i + dx
                y = j + dy
                if not validPos(x,y): continue
                if not isStraight(trace[-2][0], trace[-2][1], x, y):
                    trace.append((x,y))
                    DFS(x, y, 1, None, numberLeft)
                    trace.pop() 
        else:
            for (dx, dy) in directions:
                x = i + dx
                y = j + dy
                if not validPos(x,y): continue
                trace.append((x,y))
                if isStraight(trace[-2][0], trace[-2][1], x, y):
                    DFS(x, y, currLen+1, maxLen, numberLeft)  
                else:
                    DFS(x, y, 1, None, numberLeft)  
                trace.pop() 

    visited[i][j] = 0
    

if __name__=="__main__":
    
    load_input()
    init()
    visited  = [[0 for i in range(size)] for j in range(size)]
    trace.append(startNumber[1])

    for lenght in range(1, startNumber[0]):
        startLength = lenght
        print(startLength)
        if done: break
        DFS(startNumber[1][0], startNumber[1][1], 0, lenght, len(numberList)-1)

    print(resTrace)
    
    


