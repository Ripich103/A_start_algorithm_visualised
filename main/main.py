import pygame
from enum import Enum

class Blocks(Enum):
    AIR = 0,
    WALL = 1,
    START = 2,
    END = 3

def setColor(color : pygame.Color, type : Blocks):
     if type == Blocks.AIR:
          color.update(221, 221, 221)
     elif type == Blocks.WALL:
          color.update(110, 110, 110)
     elif type == Blocks.START:
          color.update(124, 252, 0)
     elif type == Blocks.END:
          color.update(255, 0, 0)
     return color

def drawGrid(grid : list, render_surface : pygame.Surface) -> None :
     for y in range(0, len(grid)):
         for x in range(0, len(grid[y])):
              type = type_array[y][x]
              box_col = pygame.Color(0, 0, 0)
              setColor(box_col, type)
              pygame.draw.rect(render_surface, box_col, grid[y][x])
              pygame.draw.rect(render_surface, pygame.Color(0, 0, 0), grid[y][x], 2)

def toIndexes(mx : int, my : int) -> tuple[int, int] :
     x = int(mx / 50) - 1
     y = int(my / 50) - 1

     if(x < GRID_SIZE_X and x >= 0 and y < GRID_SIZE_Y and y >= 0):
          return x, y
     else:
          return -1, -1

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
mouse = pygame.mouse
running = True
clicked = False
selected_type = Blocks.WALL

GRID_SIZE_Y = 10
GRID_SIZE_X = 10

grid = []
type_array = []
for j in range(0, GRID_SIZE_Y):
        grid.append([])
        type_array.append([])
        for i in range(0, GRID_SIZE_X):
            rectsize = 50
            type_array[j].append(Blocks.AIR)
            grid[j].append(pygame.Rect(50 + i * rectsize, 50 + j * rectsize, rectsize, rectsize))


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
    screen.fill("blue")     
    
    if clicked:
         x, y = mouse.get_pos()
         x, y = toIndexes(x, y)
         if x != -1 and y != -1:
              type_array[y][x] = selected_type

    drawGrid(grid, screen)

    pygame.draw.rect(screen, setColor(pygame.Color(0, 0, 0), selected_type), pygame.rect.Rect(700, 500, 50, 50))

    pygame.display.flip()

    clicked = False
    clock.tick(60)

pygame.quit()