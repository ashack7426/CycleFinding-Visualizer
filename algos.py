import numpy

def dist(p1,p2):
    a = numpy.array(p1)
    b = numpy.array(p2)
    return numpy.linalg.norm(a-b)

def reconstructPath(camefrom, start, win):
    curr = camefrom[start]
    while curr != start:
        prev = camefrom[curr]
        curr.drawLine(win, prev)
        curr = prev

def algo(points,num):
    check = False

    if num == 1:
        check = greedy(points)

    elif num == 2:
        check = brute_force(points)

    elif num == 3:
        check = two_opt_swap(points)

    elif num == 4:
        check = hulls(points)

    return check

def greedy(points):
    print("greed")

def brute_force(points):
    pass

def two_opt_swap(points):
    pass

def hulls(points):
    pass









