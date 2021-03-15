from constants import *
import pygame


class Point:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.color = WHITE
        self.radius = self.width // 2
        self.x = row * width + self.radius
        self.y = col * width + self.radius
        
    
    def getPos(self):
        return (self.row,self.col)

    def click(self):
        if self.color == WHITE:
            self.color = BLACK
        else:
            self.color = WHITE

    def draw(self ,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 0)

    def drawLine(self,win,p):
        pygame.draw.line(win, BLUE, self.getPos(), p.getPos())

        



       

        
