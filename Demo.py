import pygame

import Manager
from Masyu_A import AStarSeacher
from Masyu_DFS import MasyuDFS

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        WHITE = (255,255,255)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class MasyuGame:
    def __init__(self, board):
       
        self.CELL_SIZE = 80  
        self.GRID_SIZE = len(board)  
        self.BOARD_SIZE = self.CELL_SIZE * self.GRID_SIZE

 
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 600

        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.BLUE = (70, 130, 180)
        self.RED = (178, 34, 34)
        self.GREEN = (34, 139, 34)
        self.ORANGE = (255, 140, 0)
        self.PURPLE = (128, 0, 128)
        self.GRAY_DARK = (100, 100, 100)

       
        self.OFFSET_X = (self.WINDOW_WIDTH - self.BOARD_SIZE) // 2
        self.OFFSET_Y = (self.WINDOW_HEIGHT - self.BOARD_SIZE) // 2

  
        self.board = board
        self.path = []
        self.pathIndex = 0
        self.currentScene = 1

        self.startVisual = False
        self.mode = 1 # 1: DFS, 2: A*
        self.testcase = 1
  
        self.create_btn()

        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Masyu")

    def create_btn(self):
        #   Scene 1 btn
        self.dfs_btn = Button(300, 200, 200, 80, "DFS", self.BLUE, (100, 149, 237))
        self.a_star_button = Button(300, 350, 200, 80, "A*", self.RED, (220, 20, 60))
        # Scene 2 btn
        self.testcase1_btn = Button(300, 150, 200, 80, "Testcase 1", self.GREEN, (50, 205, 50))
        self.testcase2_btn = Button(300, 250, 200, 80, "Testcase 2", self.ORANGE, (255, 165, 0))
        self.testcase3_btn = Button(300, 350, 200, 80, "Testcase 3", self.PURPLE, (186, 85, 211))
        self.back_btn = Button(20, 20, 100, 50, "Back", self.GRAY, self.GRAY_DARK)

    def draw_board(self):
        self.screen.fill(self.WHITE)
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                cx = self.OFFSET_X + x * self.CELL_SIZE + self.CELL_SIZE // 2
                cy = self.OFFSET_Y + y * self.CELL_SIZE + self.CELL_SIZE // 2
                pygame.draw.circle(self.screen, self.GRAY, (cx, cy), 5)  
                
              
                if self.board[y][x] == 1:
                    pygame.draw.circle(self.screen, self.BLACK, (cx, cy), 25, 3)  
                elif self.board[y][x] == -1:
                    pygame.draw.circle(self.screen, self.BLACK, (cx, cy), 25) 

    def draw_connection(self, p1, p2):
      
        x1 = self.OFFSET_X + p1[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        y1 = self.OFFSET_Y + p1[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        x2 = self.OFFSET_X + p2[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        y2 = self.OFFSET_Y + p2[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        pygame.draw.line(self.screen, self.BLACK, (x1, y1), (x2, y2), 7)



    def draw_scene1(self):
        self.dfs_btn.draw(self.screen)
        self.a_star_button.draw(self.screen)

    def draw_scene2(self):
        self.testcase1_btn.draw(self.screen)
        self.testcase2_btn.draw(self.screen)
        self.testcase3_btn.draw(self.screen)
        self.back_btn.draw(self.screen)

    def draw_scene3(self):
        self.draw_board()
        self.back_btn.draw(self.screen)

    def handleBtnClick(self, event):

        if self.currentScene == 1:
            if self.a_star_button.is_clicked(event):
                self.currentScene += 1
                self.mode = 2

            if self.dfs_btn.is_clicked(event):
                self.currentScene += 1
                self.mode = 1

        elif self.currentScene == 2:
            if self.back_btn.is_clicked(event):
                self.currentScene -= 1
            
            if self.testcase1_btn.is_clicked(event):
                self.currentScene += 1
                self.testcase = 1
                self.board = Manager.load_input(self.testcase)

            if self.testcase2_btn.is_clicked(event):
                self.currentScene += 1
                self.testcase = 2
                self.board = Manager.load_input(self.testcase)
            
            if self.testcase3_btn.is_clicked(event):
                self.currentScene += 1
                self.testcase = 3
                self.board = Manager.load_input(self.testcase)

        elif self.currentScene == 3:
            if self.back_btn.is_clicked(event):
                self.currentScene -= 1

    def draw_scene(self):
        if self.currentScene == 1:
            self.draw_scene1()
        elif self.currentScene == 2:
            self.draw_scene2()
        elif self.currentScene == 3:
            self.draw_scene3()

    def run(self):
     
        
        

        pygame.display.flip()

        running = True
        while running:
            self.screen.fill(self.WHITE)  # Xóa nội dung cũ
            self.draw_scene()  # Vẽ scene hiện tại
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.currentScene == 3 and event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                self.handleBtnClick(event)

        pygame.quit()


if __name__ == "__main__":
    
    game = MasyuGame([])
    game.run()
  