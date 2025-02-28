

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
        if len(path) <= 1:
          for (dx, dy) in self.directions:
              x, y = dx + currPos[0], dy + currPos[1]
              if self.pos_valid((x, y)):
                  path.append((x, y))  # Modify path in place
                  new_count = count - (self.board[x][y] != 0)
                  yield path, new_count
                  path.pop()  # Backtrack
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
             #new_path = copy.deepcopy(path)
            # new_path.append(nextPos)
           # path.append(nextPos)
            # new_count = count - (self.board[nextPos[0]][nextPos[1]] != 0)
            # yield path, new_count
            path.append(nextPos)  # Modify in place
            new_count = count - (self.board[x][y] != 0)
            yield path, new_count
            path.pop()  # Backtrack



class State:

    def __init__(self, path,  circleNum: int = 0):
        self.path = path
        self.circleCount = circleNum

    def expanse(self, puzzle):
        # Return list of valid states
        for move in puzzle.movements(self.path, self.circleCount):
            yield State(self.path, move[1])


class DfsSearcher:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.puzzle = MasyuPuzzle(board)
        self.path = []  # Single path for all states
        self.found = False
        self.initialize()

    def initialize(self):
        startPoint = (-1, -1)
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    count += 1
                    if startPoint == (-1, -1):
                        startPoint = (i, j)

        self.path.append(startPoint)  # Set initial path
        self.start = State(self.path, count - 1)

    def DFS(self, state):
        if self.puzzle.check_goal(state.path, state.circleCount):
            print("Found")
            print(state.path)
            write_result(1, testcase, state.path)
            self.found = True
            return

        for neighbor in state.expanse(self.puzzle):
            self.DFS(neighbor)
            if self.found:
                return

    def Dfs_search(self):
        self.DFS(self.start)






if __name__=="__main__":
    testcase = getTestcase()
    board = load_input(testcase)
    dfs = DfsSearcher(board)
    measure_performance(dfs.Dfs_search)






