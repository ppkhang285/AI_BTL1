
from Masyu_A import MasyuPuzzle, State
from Manager import getTestcase, load_input, measure_performance, write_result



class DfsSearcher:
  def __init__(self, board):
          self.board = board
          self.size = len(board)
          self.puzzle = MasyuPuzzle(board)
          self.start = None
          self.came_from ={}
          self.found = False

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

    
  def DFS(self, state):

      if self.puzzle.check_goal(state.path, state.circleCount):
        print("Found")
        print(state.path)
        write_result(1, testcase, state.path)
        self.found = True
        return

      for neighbor in state.expanse(self.puzzle):
        self.came_from[neighbor] = state
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
    
    
    
   
    
    


