import copy
from constants import *
import random
import pygame
import math
import numpy as np
from itertools import permutations
import time

def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1-y2) ** 2)

def reconstructPath(path,win, color, draw, distance):
    dist = 0
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    for i in range(len(path) - 1):
        curr = path[i]
        nextp = path[i + 1]
        dist += h(curr.getPos(), nextp.getPos())
        if draw:
            curr.drawLine(win,nextp,color)

    if distance:
        txt = font.render("Distance: " + str(round(dist,2)), False, BLACK)
        win.blit(txt, (WIDTH // 2, (WIDTH * 3) // 4))
        pygame.display.update()

    return dist


def algo(points,num, win, grid):
    if num == 1:
        greedy(points, win)

    elif num == 2:
        brute_force(points, win, grid)

    elif num == 3:
        two_opt_swap(points, win, grid)

    elif num == 4:
        hulls(points, win, grid)

def greedy(points, win):
    pts = copy.deepcopy(points)
    index = random.randint(0,len(pts) - 1)
    curr = pts.pop(index)
    path = [curr]

    while pts:
        min_dist = float('inf')
        next_p = None

        for p in pts:
            dist = h(curr.getPos(), p.getPos())
            if dist < min_dist:
                min_dist = dist
                next_p = p

        path.append(next_p)
        time.sleep(.1)
        curr.drawLine(win,next_p,RED)
        curr = next_p
        pts.remove(curr)

    
    path.append(path[0])
    time.sleep(.1)
    reconstructPath(path,win, BLUE, 1, 1)


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
    min_dist = reconstructPath(min_path,win, RED, 1, False)

    p = permutations(perm)
    for pp in p:
        path = []
        dist = 0

        draw(win,grid,ROWS,WIDTH)

        for index in pp:
            path.append(points[index])

        path.append(path[0])
        time.sleep(.1)
        dist = reconstructPath(path,win, RED, 1, False)

        if dist < min_dist:
            min_dist = dist
            min_path = path

        time.sleep(.1)
        reconstructPath(min_path,win, GREEN, 1, True)
    
    draw(win,grid,ROWS,WIDTH)
    time.sleep(.1)
    reconstructPath(min_path,win, BLUE, 1, True)

def two_opt_swap(points, win, grid):
    perm = np.random.permutation(len(points))
    best_path = []
    dist = float('inf')
    improved = True

    for index in perm:
        best_path.append(points[index])

    best_path.append(best_path[0])
    dist = reconstructPath(best_path,win, RED, 1, 1)

    while improved:
        improved = False
        for i in range(len(best_path)):
            for j in range(len(best_path)):
                #points are not already connected
                if True:
                    path = copy.deepcopy(best_path)
                    path[i] = best_path[j]
                    path[j] = best_path[i]
                    new_dist = reconstructPath(path,win, RED, 0, 0)

                    if new_dist < dist:
                        best_path = path
                        dist = new_dist
                        improved = True

                        draw(win,grid,ROWS,WIDTH)
                        best_path.append(best_path[0])
                        time.sleep(.1)
                        reconstructPath(best_path,win, RED, 1, 1)
                        best_path.pop()
    
    draw(win,grid,ROWS,WIDTH)
    best_path.append(best_path[0])
    time.sleep(.1)
    reconstructPath(best_path,win, BLUE, 1, 1)
                    

def left_index(points):
    minn = 0
    for i in range(1,len(points)): 
        if points[i].x < points[minn].x: 
            minn = i 
        elif points[i].x == points[minn].x: 
            if points[i].y > points[minn].y: 
                minn = i 
    return minn

def orientation(p, q, r): 
    ''' 
    To find orientation of ordered triplet (p, q, r).  
    The function returns following values  
    0 --> p, q and r are colinear  
    1 --> Clockwise  
    2 --> Counterclockwise  
    '''
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y) 
  
    if val == 0: 
        return 0
    elif val > 0: 
        return 1
    else: 
        return 2


def min_dist_p(outer_hull, p):
    dist = float('inf')
    pt = None
    hull = outer_hull

    for i in range(len(hull) - 1):
        curr = hull[i]
        next_pt = hull[i + 1]

        A = p.x - curr.x
        B = p.y - curr.y
        C = next_pt.x - curr.x
        D = next_pt.y - curr.y

        dot = A * C + B * D
        len_sq = C * C + D * D
        param = -1

        if (len_sq != 0):
            param = float(dot) / float(len_sq)


        if param < 0:
            xx = curr.x
            yy = curr.y
        elif param > 1:
            xx = next_pt.x
            yy = next_pt.y
        else:
            xx = curr.x + param * C
            yy = curr.y + param * D

        dx = p.x - xx
        dy = p.y - yy
        d = dx * dx + dy * dy

        if d <= dist:
            dist = d
            pt = curr
       
    return dist, pt

 
def hulls(points,win, grid):
    pts = copy.deepcopy(points)
    hulls = []
    lst = []

    while pts:
        l = []
        lst = gen_hulls(pts,win)
        hulls.append(lst)
        for p in pts:
            if p not in lst:
                l.append(p)
        pts = l

    while len(hulls) > 1:
        index = len(hulls) - 2
        outer_hull = hulls[index]
        inner_hull = hulls[index + 1]

        while inner_hull:
            min_dist = float('inf')
            pt_out = None
            in_pt = None

            for p in inner_hull:
                dist, out_pt = min_dist_p(outer_hull, p)

                if dist < min_dist:
                    pt_out = out_pt
                    min_dist = dist
                    in_pt = p

            #Add in_pt immediately after pt_out and remove in_pt
            #Then redraw hulls
            hulls[index].insert(outer_hull.index(out_pt) + 1, in_pt)
            hulls[index + 1].remove(in_pt)

            if not hulls[index + 1]:
                hulls.pop()

            draw(win,grid,ROWS,WIDTH)

            for lst in hulls:
                if len(lst) > 2:
                    for i in range(len(lst) - 1):
                        curr = lst[i]
                        nextp = lst[i + 1]
                        curr.drawLine(win,nextp,RED)
                    nextp.drawLine(win,lst[0], RED)
            time.sleep(.1)

    hulls = hulls[0]
    draw(win,grid,ROWS,WIDTH)
    hulls.append(hulls[0])
    time.sleep(.1)
    reconstructPath(hulls,win, BLUE, 1, 1)


def gen_hulls(points, win):
    n = len(points)

    if n < 3:
        return points
    
        # Find the leftmost point 
    l = left_index(points) 
  
    hull = [] 
      
    ''' 
    Start from leftmost point, keep moving counterclockwise  
    until reach the start point again. This loop runs O(h)  
    times where h is number of points in result or output.  
    '''
    p = l 
    q = 0
    while(True): 
          
        # Add current point to result  
        hull.append(p) 
  
        ''' 
        Search for a point 'q' such that orientation(p, x,  
        q) is counterclockwise for all points 'x'. The idea  
        is to keep track of last visited most counterclock-  
        wise point in q. If any point 'i' is more counterclock-  
        wise than q, then update q.  
        '''
        q = (p + 1) % n 
  
        for i in range(n): 
              
            # If i is more counterclockwise  
            # than current q, then update q  
            if(orientation(points[p],  
                           points[i], points[q]) == 2): 
                q = i 
  
        ''' 
        Now q is the most counterclockwise with respect to p  
        Set p as q for next iteration, so that q is added to  
        result 'hull'  
        '''
        p = q 
  
        # While we don't come to first point 
        if(p == l): 
            break
  
    # Print Result  
    for i in range(len(hull) - 1):
        curr = points[hull[i]]
        nextp = points[hull[i + 1]]
        curr.drawLine(win,nextp,RED)
    nextp.drawLine(win,points[hull[0]], RED)


    lst = []
    for each in hull:
        lst.append(points[each])

    return lst

   









