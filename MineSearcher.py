import time
import tracemalloc
import numpy as np


class MineSeacher:
    def __init__(self, path):
        
        self.board = []
        self.load_input(path)
        self.size = -1
        self.emptyList = []
        self.mineList = []
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.zeroCount = 0;
        self.found = False
        self.load_input(path)
        self.initialize()
      

    def load_input(self,path):
       
      with open(path, 'r') as file:
          lines = file.readlines()
      self.size = int(lines[0].strip())
      self.board = np.zeros((self.size, self.size), dtype=int)
      for i in range(1, self.size + 1):
          self.board[i - 1] = np.array([int(num) for num in lines[i].strip().split()])
      
    def initialize(self):
      for i in range(self.size):
          for j in range(self.size):
              if self.board[i][j] == -1:
                  self.emptyList.append((i, j))


    def reset(self):
      self.zeroCount = 0
      self.found = False
      self.mineList = []


    def mineAt(self, i, j):
        for (dx, dy) in self.directions:
            x = dx + i
            y = dy + j
            if not self.validPos(x,y): continue
            if self.board[x][y] > 0:
              self.board[x][y] -= 1
              if self.board[x][y] == 0:
                self.zeroCount +=1
    
    def removeMineAt(self, i, j):
      for (dx, dy) in self.directions:
          x = dx + i
          y = dy + j
          if not self.validPos(x,y): continue
          if self.board[x][y] >= 0:
            if self.board[x][y] == 0:
              self.zeroCount -=1
            self.board[x][y] += 1

    def validPos(self, i, j):

      if i < 0 or i >= self.size: return False
      if j < 0 or j >= self.size: return False
      return True    
    
    def checkValidMine(self, i, j):
      for (dx, dy) in self.directions:
        x = dx + i
        y = dy + j
        if not self.validPos(x,y): continue
        if self.board[x][y] == 0:
          return False
      return True

    def DFS(self, node: int):

      currPos = self.emptyList[node]

      self.mineAt(currPos[0], currPos[1])
      self.mineList.append(currPos)

      if self.zeroCount == self.size * self.size - len(self.emptyList):
        self.found = True
        print("Found Solution!")
        print(self.mineList)
        return
      

      for nextNode in range(node + 1, len(self.emptyList)):
        if self.found: break
        x, y = self.emptyList[nextNode]
        if self.checkValidMine(x, y):         
          self.DFS(nextNode)
          
        else: # Invalid to go to next mine
          if self.validPos(x-1, y-1) and self.board[x-1][y-1] >0 :
            break
          if self.validPos(x-1, y) and self.board[x-1][y] >0:
            if not self.validPos(x, y+1) or self.board[x][y+1] != -1:
              break
          
          
      self.removeMineAt(currPos[0], currPos[1])
      self.mineList.remove(currPos)
        
      


    
    def DfsSearch(self):
      self.reset()

      for node in range(len(self.emptyList)):
        if self.found: break
        x, y = self.emptyList[node]
        if self.checkValidMine(x, y):
          self.DFS(node)

      if not self.found:
        print("Not Found!")

     





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
    
    dfs = MineSeacher("input/mine/input3.txt")
    measure_performance(dfs.DfsSearch)
    
    
    
    
   
    
    


