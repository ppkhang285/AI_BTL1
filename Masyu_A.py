import copy
import itertools
import sys
from queue import PriorityQueue
from Manager import getTestcase, load_input, measure_performance, write_result
class MasyuPuzzle:

    def __init__(self, board):
        self.board = board
        self.size =  len(board)
        self.directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    # Check if current state is goal
    def check_goal(self, path, count):
      
      if count > 0: return False
      if (path[-1] != path[0]): return False

      startPos = path[0]
      
      # If Black -> Goal
      if self.board[startPos[0]][startPos[1]] == -1: return True
      else:
          # White 
          # Check  straight in current
          
          if self.isTurn(path[-2], path[1]): return False

          # Check turn pre and next
          if not self.isTurn(startPos, path[-3]) and not self.isTurn(startPos,  path[2]): return False
          
          return True

    def pos_valid(self, pos):
        #Check if pos(x,y) in [0; size)
        return 0 <= pos[0] < self.size and  0 <= pos[1] < self.size 

    def isTurn(self, prePos, nextPos):
        # Retur True if turn else False (Go Straight)
        if prePos[0] == nextPos[0] or prePos[1] == nextPos[1]: return False
        return True

    def filter_direcions(self, steps, prePos, currPos, needToTurn, needToStraight):
        
        if needToStraight and needToTurn: return []
        temp = []
        for(dx, dy) in steps:
            nextPos = (dx + currPos[0], dy + currPos[1])
            if not self.pos_valid(nextPos): continue
       
            if needToTurn and self.isTurn(prePos, nextPos):temp.append((dx, dy))
            elif needToStraight and not self.isTurn(prePos, nextPos): temp.append((dx, dy))
            elif not needToTurn and not needToStraight: temp.append((dx,dy))
        return temp

    

    # Return all new valid state
    def movements(self, path, count):

        currPos = path[-1]
        # Path has only 1 point
        if len(path)  <= 1:
            for(dx, dy) in self.directions:
                x, y = dx + currPos[0], dy + currPos[1]
                if self.pos_valid((x, y)): 
                    new_path = copy.deepcopy(path)
                    new_path.append((x, y))
                    new_count = count - (self.board[x][y] != 0)
                    yield new_path, new_count
            return
        
        prePos = path[-2]
        # Flag if need to turn/go straight
        needToTurn = False
        needToStraight = False
        

        # Go Straight if Current is White or Previous is Black
        if self.board[currPos[0]][ currPos[1]] == 1 or self.board[prePos[0]][ prePos[1]] == -1:
            needToStraight = True

        # Turn if 
        #   - Current is Black  
        #   - Previous is White and Straight previous:
        #   --  (turn at path[-3]-> Check -4 and -2 -> len(path) >=4)
        if self.board[currPos[0]][currPos[1]] == -1:
            needToTurn = True
        if self.board[prePos[0]][prePos[1]] == 1 and len(path) >=4 and not self.isTurn(path[-4], path[-2]):
            needToTurn = True
        
        nextSteps = self.filter_direcions(self.directions, prePos, currPos, needToTurn, needToStraight)
        


        for(dx, dy) in nextSteps:
            x, y = dx + currPos[0], dy + currPos[1]
            nextPos = (x,y)
            if  nextPos in path and not (nextPos==path[0] and count == 0): continue
            if self.board[x][y] == -1 and self.isTurn(prePos, nextPos): continue
            new_path = copy.deepcopy(path)
            new_path.append(nextPos)
            new_count = count - (self.board[nextPos[0]][nextPos[1]] != 0)
            yield new_path, new_count

   

class State:

    def __init__(self, path,  circleNum: int = 0):
        self.path = path
        self.circleCount = circleNum

    def expanse(self, puzzle):
        # Return list of valid states
        return [State(path, count) for path, count in puzzle.movements(self.path, self.circleCount)]

class AStarSeacher:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.puzzle = MasyuPuzzle(board)
        self.start = None


        self.initialize()

    def initialize(self):
        startPoint = (-1, -1)
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    count +=1
                    if startPoint == (-1,-1): startPoint = (i,j)
    
        self.start = State([startPoint], count-1)


                  
    def heuristic(self, state: State):
        currenPos = state.path[-1]
        startPos = self.start.path[0]

        mahathanDistance = abs(currenPos[0] - startPos[0]) + abs(currenPos[1] - startPos[1])
        
        return mahathanDistance + state.circleCount * 3

    def a_star_search(self):
        
        open_set = PriorityQueue()
        closed_set = set()
        came_from = {}
        counter = itertools.count()

        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}
        
        
        open_set.put((f_score[self.start], next(counter), self.start))
        

        while not open_set.empty():
            _, _,current = open_set.get()
            

            
            if self.puzzle.check_goal(current.path, current.circleCount):
                print("Found")
                print(current.path)
                write_result(2, testcase, current.path)
                return
            
            for neighbor in current.expanse(self.puzzle):
                if current in closed_set: continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                    open_set.put((f_score[neighbor], next(counter), neighbor))
            
            closed_set.add(current)
        
        print("Not found")
        

            




if __name__=="__main__":
    
    testcase = getTestcase()
    board = load_input(testcase)

    searcher = AStarSeacher(board)
    measure_performance(searcher.a_star_search)
    
        