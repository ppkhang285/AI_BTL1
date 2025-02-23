import pygame

class MasyuGame:
    def __init__(self, board):
       
        self.CELL_SIZE = 80  
        self.GRID_SIZE = 6  
        self.BOARD_SIZE = self.CELL_SIZE * self.GRID_SIZE

 
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 600
        self.WHITE, self.BLACK, self.GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)

       
        self.OFFSET_X = (self.WINDOW_WIDTH - self.BOARD_SIZE) // 2
        self.OFFSET_Y = (self.WINDOW_HEIGHT - self.BOARD_SIZE) // 2

  
        self.board = [
            [None,  0, None, None,  1],
            [0, None,  0,    0, None],
            [0,  0, None, None, None],
            [None, 0, None,  0,    0],
            [None, None,  1,  0, None]
        ]

  
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Masyu")

    def draw_board(self):
        self.screen.fill(self.WHITE)
       
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                cx = self.OFFSET_X + x * self.CELL_SIZE + self.CELL_SIZE // 2
                cy = self.OFFSET_Y + y * self.CELL_SIZE + self.CELL_SIZE // 2
                pygame.draw.circle(self.screen, self.GRAY, (cx, cy), 5)  
                
              
                if self.board[y][x] == 0:
                    pygame.draw.circle(self.screen, self.BLACK, (cx, cy), 25, 3)  
                elif self.board[y][x] == 1:
                    pygame.draw.circle(self.screen, self.BLACK, (cx, cy), 25) 

    def draw_connection(self, p1, p2):
      
        x1 = self.OFFSET_X + p1[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        y1 = self.OFFSET_Y + p1[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        x2 = self.OFFSET_X + p2[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        y2 = self.OFFSET_Y + p2[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        pygame.draw.line(self.screen, self.BLACK, (x1, y1), (x2, y2), 7)

    def run(self):
     
        self.draw_board()
        self.draw_connection((1, 0), (2, 1))  
        self.draw_connection((2, 1), (3, 1))

        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()


if __name__ == "__main__":
    game = MasyuGame()
    game.run()
