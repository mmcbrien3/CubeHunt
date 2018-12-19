'''
Created on Jul 30, 2016

@author: mrmcb
'''
import random

class map():     

    def __init__(self,size):
        self.size = size
        self.graph = [['_' for _ in range(size[0])] for _ in range(size[1])]
        self.empties = self.getEmpties()
    
    def addPlayer(self,playerPos):
        try:
            self.playerPos
        except:
            self.playerPos = playerPos
            self.graph[int(self.playerPos[1]/50)][int(self.playerPos[0]/50)] = 'P'
        else:
            self.graph[int(self.playerPos[1]/50)][int(self.playerPos[0]/50)] = '_'
            self.playerPos = playerPos
            self.graph[int(self.playerPos[1]/50)][int(self.playerPos[0]/50)] = 'P'
        
    def addObjective(self,objectivePos):
        try:
            self.objectivePos
        except:
            self.objectivePos= objectivePos
            self.graph[int(self.objectivePos[1]/50)][int(self.objectivePos[0]/50)] = 'O'
        else:
            self.graph[int(self.objectivePos[1]/50)][int(self.objectivePos[0]/50)] = '_'
            self.objectivePos = objectivePos
            self.graph[int(self.objectivePos[1]/50)][int(self.objectivePos[0]/50)] = 'O'
       
    def addWalls(self,walls):
        for i in range(len(walls)):
            self.graph[int(walls[i][1]/50)][int(walls[i][0]/50)] = 'X'
       
    def addWall(self,wallPos):
        self.graph[int(wallPos[1]/50)][int(wallPos[0]/50)] = 'X'

    def addRandom(self,objectType):
        self.empties = self.getEmpties()
        spot = random.randint(0,len(self.empties)-1)
        position = self.empties[spot]
        if objectType == 'objective':
            self.addObjective(position)
            while not self.isPathway(position):
                spot = random.randint(0,len(self.empties)-1)
                position = self.empties[spot]
            self.addObjective(position)
        else:
            self.addWall(position)
        return position

    def removeWalls(self, wallPos):
        if len(wallPos) > 2:
            for i in range(len(wallPos)):
                self.graph[int(wallPos[i][1]/50)][int(wallPos[i][0]/50)] = '_'
        else:
            self.graph[int(wallPos[1]/50)][int(wallPos[0]/50)] = '_'
    
    def removeObjective(self):
        self.graph[int(self.objectivePos[1]/50)][int(self.objectivePos[0]/50)] = '_'
        
    def removePeriods(self):
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.graph[i][j] == '.':
                    self.graph[i][j] = '_'

    def inBounds(self,position):
        x = position[0]/50
        y = position[1]/50
        xVal = (x>-1 and x<self.size[0])
        yVal = (y>-1 and y<self.size[1])
        return xVal and yVal
    
    def checkMove(self,direction):
        newPos = [0,0]
        nextSquare = [0,0]
        curPos = self.playerPos
        newPos[0] = curPos[0]
        newPos[1] = curPos[1]
        nextSquare[0] = newPos[0]
        nextSquare[1] = newPos[1]
        onGrid = False
        if direction == 'LEFT':
            newPos[0] = curPos[0] - 5
            newPos[1] = curPos[1]
            nextSquare[0] = newPos[0] - (50-(newPos[0]%50))
            nextSquare[1] = newPos[1]
            if newPos[1]%50 == 0:
                onGrid = True
        elif direction == 'RIGHT':
            newPos[0] = curPos[0] + 5
            newPos[1] = curPos[1]
            nextSquare[0] = newPos[0] + (50-(newPos[0]%50))
            nextSquare[1] = newPos[1]
            if newPos[1]%50 == 0:
                onGrid = True
        elif direction == 'UP':
            newPos[0] = curPos[0]
            newPos[1] = curPos[1] - 5
            nextSquare[0] = newPos[0]
            nextSquare[1] = newPos[1] - (50-(newPos[1]%50))
            if newPos[0]%50 == 0:
                onGrid = True
        elif direction == 'DOWN':
            newPos[0] = curPos[0]
            newPos[1] = curPos[1] + 5
            nextSquare[0] = newPos[0]
            nextSquare[1] = newPos[1] + (50-(newPos[1]%50))
            if newPos[0]%50 == 0:
                onGrid = True
        print(newPos)
        print(nextSquare)
        print("")
        if onGrid and not self.getObject(nextSquare) == 'X':
            self.addPlayer(newPos)
            return newPos
        return [-1,-1]
    
    def isPathway(self,oPos):
        self.options = list()
        originalObj = self.objectivePos
        originalPlayer = self.playerPos
        self.graph[int(self.playerPos[1]/50)][int(self.playerPos[0]/50)] = '_'
        self.addObjective(oPos)
        tempOptions = self.getOptions(self.playerPos)
        self.options = list()
        for i in range(len(tempOptions)):
            if self.options == True:
                break
            if not tempOptions[i][0] == 'X' and not tempOptions[i][0] == '.' and not tempOptions[i][0] == 'O':
                self.graph[int(tempOptions[i][2]/50)][int(tempOptions[i][1]/50)] = '.'
                self.makeFakeMove(tempOptions[i][1:3])
                if type(self.options) == bool:
                    break
                self.options += [tempOptions[i]]
            elif tempOptions[i][0] == 'O':
                self.options = True
                break
        self.removePeriods()
        self.addPlayer(originalPlayer)
        self.addObjective(originalObj)
        if self.options == True:
            return True
        else:
            return False
    
    def makeFakeMove(self,newPos):
        tempOptions = self.getOptions(newPos)
        for i in range(len(tempOptions)):
            if self.options == True:
                break
            if not tempOptions[i][0] == 'X' and not tempOptions[i][0] == '.' and not tempOptions[i][0] == 'O':
                self.graph[int(tempOptions[i][2]/50)][int(tempOptions[i][1]/50)] = '.'
                self.makeFakeMove(tempOptions[i][1:3])
                if type(self.options) == bool:
                    break
                self.options += [tempOptions[i]]
            elif tempOptions[i][0] == 'O':
                self.options = True
                break

    def getOptions(self,curPos):
        self.options = list()
        self.options.append([self.getObject([curPos[0]-50,curPos[1]]),curPos[0]-50,curPos[1]])
        self.options.append([self.getObject([curPos[0]+50,curPos[1]]),curPos[0]+50,curPos[1]])
        self.options.append([self.getObject([curPos[0],curPos[1]-50]),curPos[0],curPos[1]-50])
        self.options.append([self.getObject([curPos[0],curPos[1]+50]),curPos[0],curPos[1]+50])
        return self.options
          
    def getEmpties(self):
        empties = []
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.graph[i][j] == '_':
                    empties.append([j*50,i*50])
        return empties

    def getObject(self,position):
        if self.inBounds(position):
            return self.graph[int(position[1]/50)][int(position[0]/50)]
        else:
            return 'X' 
    

    def __str__(self):
        stringThing = ''
        for i in range(self.size[1]):
            stringThing = stringThing + '\n'
            for j in range(self.size[0]):
                stringThing = stringThing + self.graph[j][i]
        return stringThing
        