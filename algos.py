import copy
from constants import *
import random
import pygame
import math
from itertools import permutations  

def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1-y2) ** 2)

def reconstructPath(path,win, color, min):
    dist = 0
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    for i in range(len(path) - 1):
        curr = path[i]
        next = path[i + 1]
        dist += h(curr.getPos(), next.getPos())
        curr.drawLine(win,next,color)

    txt = font.render("Distance: " + str(round(dist,2)), False, BLACK)
    win.blit(txt, (WIDTH // 2, (WIDTH * 3) // 4))
    min = dist


def algo(points,num, win, grid):
    if num == 1:
        greedy(points, win)

    elif num == 2:
        brute_force(points, win, grid)

    elif num == 3:
        two_opt_swap(points, win)

    elif num == 4:
        hulls(points, win)

def greedy(points, win):
    pts = copy.deepcopy(points)
    index = random.randint(0,len(pts) - 1)
    curr = pts.pop(index)
    path = [curr]

    while pts:
        min = float('inf')
        next = None

        for p in pts:
            dist = h(curr.getPos(), p.getPos())
            if dist < min:
                min = dist
                next = p

        path.append(next)
        curr.drawLine(win,next,RED)
        curr = next
        pts.remove(curr)
    
    path.append(path[0])
    reconstructPath(path,win, BLUE, min)


def draw(win, grid,rows , width):
    win.fill(WHITE)

    for row in grid:
        for point in row:
            point.draw(win)

    pygame.display.update()


def brute_force(points, win, grid):
    min_dist = float('inf')
    min_path = copy.deepcopy(points)

    perm = []
    for i in range(len(points)):
        perm.append(i)

    min_path.append(points[0])
    reconstructPath(min_path,win, RED, min_dist)

    p = permutations(perm)
    for pp in p:
        path = []
        dist = 0

        draw(win,grid,ROWS,WIDTH)

        for index in pp:
            path.append(points[index])

        path.append(path[0])
        reconstructPath(path,win, RED, dist)

        if dist < min_dist:
            min_dist = dist
            min_path = path
    
    draw(win,grid,ROWS,WIDTH)
    reconstructPath(min_path,win, BLUE, min_dist)

def two_opt_swap(points, win):
    pass

def hulls(points, win):
    pass









