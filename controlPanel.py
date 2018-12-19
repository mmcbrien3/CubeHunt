'''
Created on Jul 30, 2016

@author: mrmcb
'''
from map import map
from square import square, playerSquare
import random, pygame, sys, re


class controlPanel(object):
    '''
    classdocs
    '''
    def __init__(self):
        pygame.init()
        self.playingGame = False
        self.viewingScores = False
        self.playSmooth = False
        self.viewHS = 'Not smooth'
        
        self.wallColor = [198, 147, 84]
        self.bgColor = [0, 37, 76]
        self.playerColor = [255,255,255]
        self.objectiveColor = [255,0,0]
        self.menuColor = self.wallColor
        self.rainbowColors = [[244,154,194],[174,198,207],[119,190,119],[207,207,196],[253,253,150],[130,105,83]]
        
        self.myfont = pygame.font.SysFont('Consolas', 32)
        self.menuFont = pygame.font.SysFont('Consolas', 18)        
        self.myfont2 = pygame.font.SysFont('Consolas', 16)
        
        self.sixButton = pygame.Rect(50,225,100,50)
        self.tenButton = pygame.Rect(200,225,100,50)
        self.fourteenButton = pygame.Rect(350,225,100,50)
        self.scoresButton = pygame.Rect(200,325,100,50)
        self.smoothButton = pygame.Rect(200,425,100,50)
        
        self.downButton = pygame.Rect(240,480,20,15)
        self.upButton = pygame.Rect(240,5,20,15)

        self.playerSymbol = pygame.Rect(50,75,100,100)
        self.objectiveSymbol = pygame.Rect(350,75,100,100)
        
        self.sixLabel = self.menuFont.render('Miniature', 1, [255,255,255])
        self.tenLabel = self.menuFont.render('Standard', 1, [255,255,255])
        self.fourteenLabel = self.menuFont.render('Massive', 1, [255,255,255])
        self.scoresLabel = self.menuFont.render('Scores',1,[0,255,0])
        self.smoothLabel = self.menuFont.render('Smooth',1,[0,0,0])
        
        self.scoresLabels = list()
        self.plaques = list()
        pygame.display.set_icon(pygame.image.load('.\\data\\cube hunt icon.png'))
        
        while True:
            if self.playingGame:
                if self.seconds > 0:
                    self.lost = True
                    self.playGame(self.playSmooth)
                else:
                    self.loseGame()
            else:
                if self.viewingScores:
                    self.viewScoresScreen()
                else:
                    self.menuScreen()
                    
    def menuScreen(self):
        self.screen = pygame.display.set_mode((500,500),0,32)
        pygame.display.set_caption('Cube Hunt')
        self.drawMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.sixButton.collidepoint(pos):
                    self.size = 6
                    self.playingGame = True
                    self.screen = pygame.display.set_mode((300,300),0,32)
                    self.setGame()
                elif self.tenButton.collidepoint(pos):
                    self.size = 10
                    self.playingGame = True
                    self.setGame()
                elif self.fourteenButton.collidepoint(pos):
                    self.size = 14
                    self.playingGame = True
                    self.screen = pygame.display.set_mode((700,700),0,32)
                    self.setGame()
                elif self.scoresButton.collidepoint(pos):
                    self.viewingScores = True
                    self.viewHS = 'Not smooth'
                    self.getHSTable()
                elif self.smoothButton.collidepoint(pos):
                    self.playSmooth = not self.playSmooth
                    
    def viewScoresScreen(self):
        self.drawScores()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.viewingScores = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.downButton.collidepoint(pos): 
                    self.viewHS = 'Smooth'  
                    self.getHSTable() 
                if self.upButton.collidepoint(pos): 
                    self.viewHS = 'Not smooth'
                    self.getHSTable()
    
    def getHSTable(self):   
        information6 = self.getHS(6)
        information10 = self.getHS(10)
        information14 = self.getHS(14)
        self.info = [information6, information10, information14]
        self.scoresLabels = [[],[],[]]
        for i in range(3):
            for j in range(10):
                name = self.info[i][1][j]
                if len(name) > 10:
                    name = name[:7]+'...'
                self.scoresLabels[i].append(self.menuFont.render(name + ': ' + self.info[i][0][j],1,[255,255,255]))
        for i in range(3):
            for j in range(10):
                self.plaques.append(pygame.Rect(10+i*163.33,23.81+47.62*j,153.33,23.81)) 
    
    def playGame(self,smooth):
        if smooth:
            self.seconds = self.allowed - self.milliseconds/1000
            if self.objective.returnPos() == [-50,-50] or self.player.returnRect().colliderect(self.objective.returnRect()):
                tempPos = self.pathway.addRandom('objective')
                if self.player.returnRect().colliderect(self.objective.returnRect()):
                    self.pathway.removeObjective()
                    self.objective.place([-50,-50])
                else:
                    self.objective.place(tempPos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.key.append('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.key.append('RIGHT')
                    elif event.key == pygame.K_UP:
                        self.key.append('UP')
                    elif event.key == pygame.K_DOWN:
                        self.key.append('DOWN')
                    elif event.key == pygame.K_a:
                        self.key = 'LEFT'
                    elif event.key == pygame.K_d:
                        self.key = 'RIGHT'
                    elif event.key == pygame.K_w:
                        self.key = 'UP'
                    elif event.key == pygame.K_s:
                        self.key = 'DOWN'
                    elif event.key == pygame.K_ESCAPE:
                        self.playingGame = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.key.remove('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.key.remove('RIGHT')
                    elif event.key == pygame.K_UP:
                        self.key.remove('UP')
                    elif event.key == pygame.K_DOWN:
                        self.key.remove('DOWN')
                    elif event.key == pygame.K_a:
                        self.key = 'LEFT'
                    elif event.key == pygame.K_d:
                        self.key = 'RIGHT'
                    elif event.key == pygame.K_w:
                        self.key = 'UP'
                    elif event.key == pygame.K_s:
                        self.key = 'DOWN'
            for i in range(len(self.key)):
                self.checkMove(self.key[i])
            self.pathway.addPlayer(self.player.returnPos())
            if self.player.returnRect().colliderect(self.objective.returnRect()):
                if len(self.walls) == (self.size*self.size-2):
                    pygame.mixer.music.load('.\\data\\level up.wav')
                    pygame.mixer.music.play()
                    self.level += 1
                    self.pathway.removeWalls(self.wallPos)
                    self.walls = self.addWalls()
                    self.score+=50
                    if self.lowestTime > self.size/2-2:
                        self.lowestTime -= 1
                    tempPos = self.pathway.addRandom('objective')
                    self.objective.place(tempPos)
                    self.allowed = self.size
                    self.seconds = self.allowed
                    self.milliseconds = 0
                    self.resetClock()
                else:
                    self.score+=1
                    pygame.mixer.music.load('.\\data\\ding.wav')
                    pygame.mixer.music.play()
                    if self.level > 3:
                        newWall = square(self.rainbowColors[random.randint(0,len(self.rainbowColors)-1)])
                    else:
                        newWall = square(self.wallColor)
                    tempPos = self.pathway.addRandom('wall')
                    newWall.place(tempPos)
                    options = self.pathway.getOptions(self.player.returnPos())
                    neighbors = list()
                    for i in range(len(options)):
                        neighbors.append(options[i][0])
                    while not '_' in neighbors and not 'O' in neighbors:
                        self.pathway.removeWalls(tempPos)
                        tempPos = self.pathway.addRandom('wall')
                        newWall.place(tempPos)
                        options = self.pathway.getOptions(self.player.returnPos())
                        neighbors = list()
                        for i in range(len(options)):
                            neighbors.append(options[i][0])
                    if self.player.returnRect().colliderect(newWall.returnRect()):
                        self.pathway.removeWalls(tempPos)
                        newWall.place([-50,-50])
                    self.walls.append(newWall)
                    self.wallPos.append(newWall.returnPos())
                    self.objective.place([-50,-50])
                    self.pathway.removeObjective()
                    self.resetClock()
        else:
            self.seconds = self.allowed - self.milliseconds/1000
            self.key = ''
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.key = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.key = 'RIGHT'
                    elif event.key == pygame.K_UP:
                        self.key = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.key = 'DOWN'
                    elif event.key == pygame.K_a:
                        self.key = 'LEFT'
                    elif event.key == pygame.K_d:
                        self.key = 'RIGHT'
                    elif event.key == pygame.K_w:
                        self.key = 'UP'
                    elif event.key == pygame.K_s:
                        self.key = 'DOWN'
                    elif event.key == pygame.K_ESCAPE:
                        self.playingGame = False
            self.checkMove(self.key)
            if self.player.returnPos() == self.objective.returnPos():
                if len(self.walls) == (self.size*self.size-2):
                    pygame.mixer.music.load('.\\data\\level up.wav')
                    pygame.mixer.music.play()
                    self.level += 1
                    self.pathway.removeWalls(self.wallPos)
                    self.walls = self.addWalls()
                    self.pathway.addWalls(self.wallPos)
                    self.score+=50
                    if self.lowestTime > self.size/2-2:
                        self.lowestTime -= 1
                    tempPos = self.pathway.addRandom('objective')
                    while not self.pathway.isPathway(tempPos):
                        tempPos = self.pathway.addRandom('objective')
                    self.objective.place(tempPos)
                    self.allowed = self.size
                    self.seconds = self.allowed
                    self.milliseconds = 0
                    self.resetClock()
                else:
                    self.score+=1
                    pygame.mixer.music.load('.\\data\\ding.wav')
                    pygame.mixer.music.play()
                    if self.level > 3:
                        newWall = square(self.rainbowColors[random.randint(0,len(self.rainbowColors)-1)])
                    else:
                        newWall = square(self.wallColor)
                    tempPos = self.pathway.addRandom('wall')
                    newWall.place(tempPos)
                    options = self.pathway.getOptions(self.player.returnPos())
                    neighbors = list()
                    for i in range(len(options)):
                        neighbors.append(options[i][0])
                    while not '_' in neighbors and not 'O' in neighbors:
                        self.pathway.removeWalls(tempPos)
                        tempPos = self.pathway.addRandom('wall')
                        newWall.place(tempPos)
                        options = self.pathway.getOptions(self.player.returnPos())
                        neighbors = list()
                        for i in range(len(options)):
                            neighbors.append(options[i][0])
                    self.walls.append(newWall)
                    self.wallPos.append(newWall.returnPos())
                    tempPos = self.pathway.addRandom('objective')
                    while not self.pathway.isPathway(tempPos):
                        tempPos = self.pathway.addRandom('objective')
                    self.objective.place(tempPos)
                    self.resetClock()
        self.milliseconds += self.t.tick_busy_loop(60)
        self.label = self.myfont.render('%.1f' %self.seconds, 1, (0, 0,0))
        self.scoreLabel = self.myfont2.render(str(self.score),1,(25,75,0))
        self.drawAll()
    
    def loseGame(self):
        if self.lost:
            pygame.mixer.music.load('.\\data\\game over.wav')
            pygame.mixer.music.play()
            self.lost = False
        temp = self.viewHS
        if self.playSmooth:
            self.viewHS = 'Smooth'
        else:
            self.viewHS = 'Not smooth'
        bestScores = self.getHS(self.size)
        self.viewHS = temp
        hsPos = -1
        nameEntered = True
        for i in range(10):
            if self.score > int(bestScores[0][i]):
                hsPos = i+1
                nameEntered = False
                self.hsBG = pygame.Rect(0,0,200,50)
                break
        for event in pygame.event.get():
            if nameEntered:
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.setGame()
                    elif event.key == pygame.K_ESCAPE:
                        self.playingGame = False
            else:
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.username =='':
                            self.setHS(self.size,self.score,self.username,hsPos)
                            nameEntered = True
                            self.setGame()
                    elif event.key == pygame.K_ESCAPE:
                        self.playingGame = False
                    elif (event.key >= 65 and event.key <= 90) or (event.key >= 97 and event.key <=122):
                        self.username += chr(event.key)
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:len(self.username)-1]
        if not nameEntered:
            self.hsLabelAnnounc = self.myfont2.render('New High Score (' + str(hsPos)+ ')!',1,[0,255,0])
            self.hsLabel = self.myfont2.render('Username: '+self.username,1,[0,255,0])
        self.label = self.myfont.render('0.0', 1, (255,0,0))
        self.drawAll()
    
    def setGame(self):
        pygame.mixer.music.load('.\\data\\game start.wav')
        pygame.mixer.music.play()
        self.hsLabel = self.myfont2.render('',1,[255,255,255])
        self.hsLabelAnnounc = self.myfont2.render('',1,[25,75,0])
        self.hsBG = pygame.Rect(0,0,0,0)
        self.username = ''
        self.level = 1
        self.score = 0
        self.lowestTime = self.size/2
        self.milliseconds = 0
        self.allowed = self.size
        self.seconds = self.allowed
        self.pathway = map([self.size,self.size])
        self.player = playerSquare(self.playerColor,[0,0])
        self.pathway.addPlayer(self.player.returnPos())
        self.wallPos = []
        self.walls = self.addWalls()
        self.pathway.addWalls(self.wallPos)
        self.label = self.myfont.render('%.1f' %self.seconds, 1, (255,255,255))
        self.scoreLabel = self.myfont2.render(str(self.score),1,(255,255,255))
        self.objective = square(self.objectiveColor)
        tempPos = self.pathway.addRandom('objective')
        self.objective.place(tempPos)
        self.key = []
        self.drawAll()
        self.t = pygame.time.Clock()
        
    def addWalls(self):
        walls = []
        self.wallPos = []
        walls.append(square(self.wallColor))
        walls.append(square(self.wallColor))
        walls.append(square(self.wallColor))
        walls.append(square(self.wallColor))
        walls[0].place([int(self.size*50/2-50),int(self.size*50/2-50)])
        walls[1].place([int(self.size*50/2),int(self.size*50/2-50)])
        walls[2].place([int(self.size*50/2-50),int(self.size*50/2)])
        walls[3].place([int(self.size*50/2),int(self.size*50/2)])
        self.wallPos.append([int(self.size*50/2-50),int(self.size*50/2-50)])
        self.wallPos.append([int(self.size*50/2),int(self.size*50/2-50)])
        self.wallPos.append([int(self.size*50/2-50),int(self.size*50/2)])
        self.wallPos.append([int(self.size*50/2),int(self.size*50/2)])
        self.pathway.addWalls(self.wallPos)
        return walls

    def drawAll(self):
        self.screen.fill(self.bgColor)
        pygame.draw.rect(self.screen, self.player.returnColor(), self.player.returnRect(),0)
        pygame.draw.rect(self.screen, self.objective.returnColor(), self.objective.returnRect(),0)
        for i in range(len(self.walls)):
            pygame.draw.rect(self.screen,self.walls[i].returnColor(),self.walls[i].returnRect(),0)
        pygame.draw.rect(self.screen, [255,0,255], self.hsBG ,0)
        self.screen.blit(self.label, [int(self.size*50/2-50)+25,int(self.size*50/2-50)+30])
        self.screen.blit(self.scoreLabel,[int(self.size*50/2-50)+70,int(self.size*50/2-50)+80])
        self.screen.blit(self.hsLabelAnnounc,[0,0])
        self.screen.blit(self.hsLabel,[0,18])
        pygame.display.update()
    
    def drawMenu(self):
        self.screen.fill(self.menuColor)
        pygame.draw.rect(self.screen, self.bgColor, self.sixButton,0)
        pygame.draw.rect(self.screen, self.bgColor, self.tenButton,0)
        pygame.draw.rect(self.screen, self.bgColor, self.fourteenButton,0)
        pygame.draw.rect(self.screen, [100,100,100], self.scoresButton,0)
        if self.playSmooth:
            pygame.draw.rect(self.screen,[0,255,0],self.smoothButton,0)
        else:
            pygame.draw.rect(self.screen,[255,0,0],self.smoothButton,0)
        
        pygame.draw.rect(self.screen, self.playerColor, self.playerSymbol,0)
        pygame.draw.rect(self.screen, self.objectiveColor, self.objectiveSymbol,0)

        self.screen.blit(self.sixLabel, [55,241])
        self.screen.blit(self.tenLabel, [209,241])
        self.screen.blit(self.fourteenLabel, [365,241]) 
        self.screen.blit(self.scoresLabel, [220,341])    
        self.screen.blit(self.smoothLabel, [220,441]) 
               
        pygame.display.update()
    
    def drawScores(self):
        self.screen.fill(self.bgColor)
        if self.viewHS == 'Not smooth':
            pygame.draw.polygon(self.screen,[255,255,255],((240,480),(260,480),(250,495)))
        else:
            pygame.draw.polygon(self.screen,[255,255,255],((240,20),(260,20),(250,5)))
        for i in range(len(self.plaques)):
            pygame.draw.rect(self.screen,self.wallColor,self.plaques[i],0)
            
        for i in range(3):
            for j in range(10):
                self.screen.blit(self.scoresLabels[i][j],[10+i*163.33,23.81+47.62*j])
        pygame.display.update()
            
    def resetClock(self):
        if self.allowed > self.lowestTime:
            self.allowed -= .5
        self.seconds = self.allowed
        self.milliseconds = 0
    
    def getHS(self,mode):
        scoreID = re.compile('score:')
        usernameID = re.compile('username:')
        if self.viewHS == 'Smooth':
            recordBook = open('.\\data\\CH HS Smooth.txt', 'r')
        else:
            recordBook = open('.\\data\\CH HS Not Smooth.txt', 'r')
        text = recordBook.read()
        if mode == 6:
            start = text.index('Miniature')
            end = text.index('Standard')
        elif mode == 10:
            start = text.index('Standard')
            end = text.index('Massive')
        elif mode == 14:
            start = text.index('Massive')
            end = len(text)
        text = text[start:end]
        scores = scoreID.finditer(text)
        users = usernameID.finditer(text)
        scores = [match.start() for match in scores]
        users = [match.start() for match in users]
        for i in range(10):
            sub = text[scores[i]+7:]
            sub = sub.index("'")
            scores[i] = text[scores[i]+7:scores[i]+7+sub]
            sub = text[users[i]+10:]
            sub = sub.index("'")
            users[i] = text[users[i]+10:users[i]+10+sub]
        recordBook.close()
        return [scores, users]
    
    def setHS(self,mode,score,user,pos):
        scoreID = re.compile('score:')
        usernameID = re.compile('username:')
        if self.playSmooth:
            recordBook = open('.\\data\\CH HS Smooth.txt', 'r')
        else:
            recordBook = open('.\\data\\CH HS Not Smooth.txt', 'r')
        originalText = recordBook.read()
        recordBook.close()
        if mode == 6:
            start = originalText.index('Miniature')
            end = originalText.index('Standard')
        elif mode == 10:
            start = originalText.index('Standard')
            end = originalText.index('Massive')
        elif mode == 14:
            start = originalText.index('Massive')
            end = len(originalText)
        text = originalText[start:end]
        if not pos == 10:
            line = text[text.index(str(pos)+'.'):text.index(str(pos+1)+'.')]
            ogScore = scoreID.search(line)
            sub = line[ogScore.start()+7:]
            sub = sub.index("'")
            ogScore = line[ogScore.start()+7:ogScore.start()+7+sub]
            ogUser = usernameID.search(line)
            sub = line[ogUser.start()+10:]
            sub = sub.index("'")
            ogUser = line[ogUser.start()+10:ogUser.start()+10+sub]
            originalText = originalText[:originalText.index(line)] + str(pos)+".score:'"+str(score)+"'username:'"+user+"'\n"+originalText[originalText.index(line)+len(line):]
            if self.playSmooth:
                recordBook = open('.\\data\\CH HS Smooth.txt', 'w')
            else:
                recordBook = open('.\\data\\CH HS Not Smooth.txt', 'w')
            recordBook.write(originalText)
            recordBook.close()
            self.setHS(mode,ogScore,ogUser,pos+1)       
        else:
            line = text[text.index(str(pos)+'.'):end]
            originalText = originalText[:originalText.index(line)] + str(pos)+".score:'"+str(score)+"'username:'"+user+"'\n\n"+originalText[originalText.index(line)+len(line):]
            if self.playSmooth:
                recordBook = open('.\\data\\CH HS Smooth.txt', 'w')
            else:
                recordBook = open('.\\data\\CH HS Not Smooth.txt', 'w')
            recordBook.write(originalText)
            recordBook.close()
    
    def checkMove(self,direction):
        newPos = [0,0]
        curPos = self.player.returnPos()
        newPos[0] = curPos[0]
        newPos[1] = curPos[1]
        change = 50
        if self.playSmooth:
            change = 5
        if direction == 'LEFT':
            newPos[0] = curPos[0] - change
            newPos[1] = curPos[1]
            
        elif direction == 'RIGHT':
            newPos[0] = curPos[0] + change
            newPos[1] = curPos[1]
            
        elif direction == 'UP':
            newPos[0] = curPos[0]
            newPos[1] = curPos[1] - change
            
        elif direction == 'DOWN':
            newPos[0] = curPos[0]
            newPos[1] = curPos[1] + change
        if self.playSmooth:
            if newPos[0] >= 0 and newPos[0] <=self.size*50-50 and newPos[1] >= 0 and newPos[1] <=self.size*50-50:
                collided = False
                self.player.move(newPos)
                for i in range(len(self.walls)):
                    if self.player.returnRect().colliderect(self.walls[i].returnRect()):
                        collided = True
                if collided:
                    self.player.move(curPos)
        else:
            if not self.pathway.getObject(newPos) == 'X':
                self.player.move(newPos)
                self.pathway.addPlayer(newPos)
            
controlPanel()  