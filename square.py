'''
Created on Jul 30, 2016

@author: mrmcb
'''
import pygame

class square():
    '''
    classdocs
    '''
    def __init__(self,color):
        pygame.init()
        self.color = color
    
    def place(self,position):
        self.position = position
        self.squareRect = pygame.Rect(self.position[0],self.position[1],50,50)
    
    def returnPos(self):
        return self.position
    
    def returnColor(self):
        return self.color
    
    def returnRect(self):
        return self.squareRect


class playerSquare(square):

    def __init__(self,color,position):
        pygame.init()
        self.color = color
        self.position = position
        self.squareRect = pygame.Rect(self.position[0],self.position[1],50,50)    
    
    def move(self,position):
        newPosX = position[0] - self.position[0] 
        newPosY = position[1] - self.position[1]
        self.position = position
        self.squareRect.move_ip((newPosX,newPosY))
        
