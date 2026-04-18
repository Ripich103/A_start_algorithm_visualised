import pygame
import math
from enum import Enum

class Blocks(Enum):
    AIR = 0
    WALL = 1
    START = 2
    END = 3
    PATH = 4

def setColor(color : pygame.Color, type : Blocks) -> pygame.Color:
     if type == Blocks.AIR:
          color.update(221, 221, 221)
     elif type == Blocks.WALL:
          color.update(110, 110, 110)
     elif type == Blocks.START:
          color.update(124, 252, 0)
     elif type == Blocks.END:
          color.update(255, 0, 0)
     elif type == Blocks.PATH:
          color.update(100, 100, 0)
     return color

def getBlockPos(typelist : list, type : Blocks) -> tuple[int, int]:
     for y in range(0, len(typelist)):
          for x in range(0, len(typelist[y])):
              if typelist[y][x][1] == type:
                   return (x, y)
     return -1, -1
              
def drawGrid(grid : list, render_surface : pygame.Surface) -> None :
     for y in range(0, len(grid)):
         for x in range(0, len(grid[y])):
              cell, type = grid[y][x]
              box_col = pygame.Color(0, 0, 0)
              setColor(box_col, type)
              pygame.draw.rect(render_surface, box_col, cell)
              pygame.draw.rect(render_surface, pygame.Color(0, 0, 0), cell, 2)

def toIndexes(mx : int, my : int) -> tuple[int, int] :
     x = int(mx / 50) - 1
     y = int(my / 50) - 1

     if(x < GRID_SIZE_X and x >= 0 and y < GRID_SIZE_Y and y >= 0):
          return x, y
     else:
          return -1, -1     

def get_g(a : tuple[int, int], b : tuple[int, int]) -> int:
     x, y = a
     xx, yy = b
     g = 0
     if y - 1 == yy:
          if x == xx:
               return 10
     elif y  == yy:
          return 10
     elif y == yy + 1:
          if x == xx:
               return 10
     return 14

def heruistics(start : tuple[int, int], end : tuple[int, int]) -> int:
     x, y = start
     ex, ey = end
     return int(math.sqrt((x - ex)**2 + (y - ey)**2)) * 10

def neighbours(node : tuple[int, int], grid : list) -> list:
     x, y = node
     return [(x - 1, y - 1), (x - 0, y - 1), (x + 1, y - 1),
             (x - 1, y - 0),                 (x + 1, y - 0),
             (x - 1, y + 1), (x - 0, y + 1), (x + 1, y + 1)]

def search_path(sx : int, sy : int, ex : int, ey : int, grid : list) -> list:
     open = []
     closed = []
     open.append((sx, sy))

     g_dict = {(sx, sy) : 0}

     came_from = {}

     while True:
          current = None

          best_f = 2147483647
          for node in open:
               x, y = node

               g = g_dict.get(node, 2147483647)
               h = heruistics(node, (ex, ey))
               f = g + h
               if f < best_f :
                   best_f = f
                   current = node
          if current not in open:
               return [(-1, -1)]
          open.remove(current)
          closed.append(current)

          if current == (ex, ey):
               path = []
               while current in came_from:
                    path.append(current)
                    current = came_from[current]
               path.append((sx, sy))
               path.reverse()
               return path
          
          for node in neighbours(current, grid):
               x, y = node
               if(y >= 0 and y < len(grid)):
                    if (x >= 0 and x < len(grid[y])):
                         if grid[y][x][1] == Blocks.WALL or (x, y) in closed:
                              continue
                         else:
                              tentative_g = g_dict[current] + get_g(node, current)
                              if not node in open or tentative_g < g_dict.get(node, 2147483647):
                                   g_dict[node] = tentative_g
                                   came_from[node] = current
                                   if node not in open:
                                        open.append(node)
     return [(-1, -1)]  

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
mouse = pygame.mouse
running = True
clicked = False
startExists = False
endExists = False
selected_type = Blocks.WALL

GRID_SIZE_Y = 10
GRID_SIZE_X = 10

lines = 0

grid = []
for j in range(0, GRID_SIZE_Y):
     grid.append([])
     for i in range(0, GRID_SIZE_X):
          rectsize = 50
          grid[j].append([pygame.Rect(50 + i * rectsize, 50 + j * rectsize, rectsize, rectsize), Blocks.AIR])


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
             clicked = True
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_1:
                  selected_type = Blocks.AIR
             elif event.key == pygame.K_2: 
                  selected_type = Blocks.WALL
             elif event.key == pygame.K_3: 
                  selected_type = Blocks.START
             elif event.key == pygame.K_4: 
                  selected_type = Blocks.END
             elif event.key == pygame.K_r:
                  if startExists and endExists:    
                    print("run")
                    for i in range(0, len(grid)):
                         for j in range(0, len(grid[i])):
                              if grid[i][j][1] == Blocks.PATH:
                                   grid[i][j][1] = Blocks.AIR

                    startx, starty = getBlockPos(grid, Blocks.START)
                    endx, endy = getBlockPos(grid, Blocks.END)
                    lines = search_path(startx, starty, endx, endy, grid)
                    print(lines)
                    if lines[0] != (-1, -1):
                         for x, y in lines:
                              if grid[y][x][1] != Blocks.START and grid[y][x][1] != Blocks.END:
                                   grid[y][x][1] = Blocks.PATH

    screen.fill("blue")     
    
    if clicked:
         x, y = mouse.get_pos()
         x, y = toIndexes(x, y)
         if x != -1 and y != -1:
              flag = False
              if(startExists and selected_type == Blocks.START or (endExists and selected_type == Blocks.END)):
                   flag = True

              pos, type = grid[y][x]

              if (type == Blocks.START):
                   if (selected_type != Blocks.START):
                        if not (selected_type == Blocks.END and endExists):
                              startExists = False
              if (type == Blocks.END):
                   if (selected_type != Blocks.END):
                        if not (selected_type == Blocks.START and startExists):
                              endExists = False

              if (not startExists and selected_type == Blocks.START):
                   startExists = True
              elif (not endExists and selected_type == Blocks.END):
                   endExists = True 

              if (not flag):
                   grid[y][x][1] = selected_type

    drawGrid(grid, screen)

    pygame.draw.rect(screen, setColor(pygame.Color(0, 0, 0), selected_type), pygame.rect.Rect(700, 500, 50, 50))

    pygame.display.flip()

    clicked = False
    clock.tick(60)

pygame.quit()