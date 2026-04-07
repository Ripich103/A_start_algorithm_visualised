import pygame
from enum import Enum

class Blocks(Enum):
    AIR = 0,
    WALL = 1,
    START = 2,
    END = 3

def drawGrid(grid : list, render_surface : pygame.Surface):
     for y in range(0, len(grid)):
         x = 0
         while x < len(grid[y]):
              tmp = grid[y][x]
              x += 1
              box_col = pygame.Color(0, 0, 0)
              if tmp == Blocks.AIR:
                   box_col.update(221, 221, 221)
              elif tmp == Blocks.WALL:
                   box_col.update(110, 110, 110)
              elif tmp == Blocks.START:
                   box_col.update(124, 252, 0)
              elif tmp == Blocks.END:
                   box_col.update(255, 0, 0)
              pygame.draw.rect(render_surface, box_col, grid[y][x])
              pygame.draw.rect(render_surface, pygame.Color(0, 0, 0), grid[y][x], 2)
              x += 1

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

grid = []
for j in range(0, 10):
        grid.append([])
        for i in range(0, 10):
            rectsize = 50
            grid[j].append(Blocks.AIR)
            grid[j].append(pygame.Rect(50 + i * rectsize, 50 + j * rectsize, rectsize, rectsize))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    drawGrid(grid, screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()