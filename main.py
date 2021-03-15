from constants import *
import pygame
from point import *
from algos import *

win = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("CycleFinding Visualizer")

def draw(win, grid,rows , width):
    win.fill(WHITE)

    for row in grid:
        for point in row:
            point.draw(win)

    pygame.display.update()

def getClickedPos(pos, rows, width):
    x, y =pos
    gap =width//rows
    rows = x//gap
    col =  y//gap
    return rows,col

def setGrid(rows, width):
    grid= []
    gap =width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            point = Point(i,j,gap)
            grid[i].append(point)
    return grid


def get_txt(num):
    text = ""

    if num == 1:
        text = "Greedy"

    elif num == 2:
        text = "Brute Force"

    elif num == 3:
        text = "Two-opt Swap"

    elif num == 4:
        text = "Hulls"

    return text

def main(win, width,ROWS):
    grid = setGrid(ROWS, width)
    points = []
    run = True
    algo_num = 1
    num_points = 0
    txt = ""
    
    while run :
        draw(win,grid,ROWS,width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos,ROWS , width)
                point = grid[row][col]

                if point.color == WHITE:
                    if num_points < 2:
                        num_points += 1
                        point.click()
                        point.draw(win)
                        points.append(point)
                else:
                    num_points -= 1
                    point.click()
                    point.draw(win)
                    points.append(point)

            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_c:
                    grid = setGrid(ROWS, width)
                    num_points = 0
                    points = []
                    pygame.display.set_caption("CycleFinding Visualizer")

                if event.key == pygame.K_SPACE and num_points > 1:
                    txt = get_txt(algo_num)
                    pygame.display.set_caption(txt)
                    algo(points,algo_num)

                if event.key == pygame.K_1:
                    algo_num = 1
                if event.key == pygame.K_2:
                    algo_num = 2
                if event.key == pygame.K_3:
                    algo_num = 3
                if event.key == pygame.K_4:
                    algo_num = 4

main(win, WIDTH, ROWS)