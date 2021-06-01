import pygame
from random import randint
from math import fabs, sqrt


def loadImage(width, high, imageName, imageAlpha=False):
    image = pygame.image.load(imageName)
    image = pygame.transform.scale(image, (width, high))
    if imageAlpha == True:
        image = image.convert_alpha()  # only on png?
    else:
        image = image.convert()
    return image



class GameStatus:
    game_over = False
    PAUSE = False
    #EXIT = False
    level = 1
    points = 0
    lives = 3
    font = None
    textWin = None
    window = (700, 700)
    infoColor = (255, 50, 0)
    frame = pygame.time.Clock()
    @staticmethod
    def printOnCenter(message):
        messageTxt = font.render(message, True, (200, 50, 0))
        screen.blit(messageTxt, (GameStatus.window[0]/2 - messageTxt.get_width()/2, GameStatus.window[1]/2 - messageTxt.get_width()/2))
    @staticmethod
    def printInfo():
        levelMessage = "Level " + str(GameStatus.level)
        pointsMessage = "Points " + str(GameStatus.points)
        livesMessage = "Lives " + str(GameStatus.lives)
        #font = pygame.font.SysFont("comicsans", 30)
        levelTxt = font.render(levelMessage, True, GameStatus.infoColor)
        screen.blit(levelTxt, (0, 0))
        pointsTxt = font.render(pointsMessage, True, GameStatus.infoColor)
        screen.blit(pointsTxt, (0, pointsTxt.get_height() + 2))
        livesTxt = font.render(livesMessage, False, GameStatus.infoColor)
        screen.blit(livesTxt,  (0, pointsTxt.get_height() + livesTxt.get_height() + 4))
    @staticmethod
    def pause():
        if GameStatus.PAUSE == False:
            GameStatus.PAUSE = True
        else:
            GameStatus.PAUSE = False
    def __init__(self):
        pass


class GameObject:   #base class
    def __init__(self, x=0, y=0, width=0, high=0):
        self.x = x # on screen
        self.y = y
        self.width = width
        self.high = high
        self.collisionState = False
        self.colx = self.width*0.85
        self.coly = self.high*0.75

    def is_colision(self, x ,y):
        if y >= self.y and y <= self.y + self.coly:
            if x >= self.x and x <= self.x + self.colx:
                self.collisionState = True
            elif x + self.colx >= self.x and x + self.colx <= self.x + self.colx:
                self.collisionState = True
        elif y + self.coly >= self.y and y + self.coly <= self.y + self.coly:
            if x >= self.x and x <= self.x + self.colx:
                self.collisionState = True
            elif x + self.colx >= self.x and x + self.colx <= self.x + self.colx:
                self.collisionState = True
        return self.collisionState

    def distance(self, x, y):
        return sqrt( fabs( (self.x - x)**2 - (self.y - y)**2 ) )



class Treasure(GameObject):
    def __init__(self, x=0, y=0, width=0, high=0):
        GameObject.__init__(self, x, y, width, high)
    def relocate_rand(self):
        x, y = [self. x, self.y]
        while True:
            self.x = randint(1,GameStatus.window[0]-self.width)
            self.y = randint(1,GameStatus.window[1]-self.high)
            if self.distance(x, y) > 0.2* sqrt(GameStatus.window[0]**2 + GameStatus.window[1]**2):
                break

    def checkForCollision(self, x, y):
        if self.is_colision(x, y) == True:
            self.collisionState = False
            GameStatus.points += 5
            self.relocate_rand()





class Player(GameObject):
    def __init__(self, x=0, y=0, width=0, high=0):
        self.step = 2
        GameObject.__init__(self, x, y, width, high)
    def initPosition(self):
        self.x = 350
        self.y = 50
    def moveRight(self):
        if self.x <= GameStatus.window[0] -0.75*self.width:
            self.x += self.step
    def moveLeft(self):
        if self.x >= 0.75*self.width:
            self.x -= self.step
    def moveUp(self):
        if self.y >= 0:
            self.y -= self.step
    def moveDown(self):
        if self.y <= GameStatus.window[1] - self.high:
            self.y += self.step
    def freeze(self):
        pass



class Enemy(Player):
    def __init__(self, x=0, y=0, width=0, high=0):
        Player.__init__(self, x, y, width, high)
        self.step = 1
    def move(self, x, y):
        if fabs(self.x - x) <=1 and fabs(self.y - y) <=1:
            return
        if x > self.x:
            if y == self.y:
                self.moveRight()
            elif y > self.y:
                if fabs(x - self.x) >= fabs(y - self.y):
                    self.moveRight()
                else:
                    self.moveDown()
            else:
                if fabs(x - self.x) >= fabs(y - self.y):
                    self.moveRight()
                else:
                    self.moveUp()
        elif x < self.x:
            if y == self.y:
                self.moveLeft()
            elif y > self.y:
                if fabs(x - self.x) >= fabs(y - self.y):
                    self.moveLeft()
                else:
                    self.moveDown()
            else:
                if fabs(x - self.x) >= fabs(y - self.y):
                    self.moveLeft()
                else:
                    self.moveUp()
        else:
            if y > self.y:
                self.moveDown()
            else:
                self.moveUp()

    def checkEnemyCollision(self, x, y):
        if self.is_colision(x, y) == True:
            GameStatus.lives -= 1
            self.collisionState = False
            if GameStatus.lives == 0:
                GameStatus.game_over = True
            return True
        return False






width, high = [40, 40]
px0 , py0 = [int(GameStatus.window[0]/2 - width/2), int(GameStatus.window[1]*0.05)]
tx0, ty0 = [px0, int(GameStatus.window[1]*0.85)]
ex0, ey0 = [int(GameStatus.window[0]*0.85), int(GameStatus.window[1]*0.85)]

pygame.init()
screen = pygame.display.set_mode(GameStatus.window)

backround = GameObject(0,0,GameStatus.window[0],GameStatus.window[1])
backroundImage = loadImage(backround.width, backround.high, "background.png")

player = Player(px0, py0, width, high)
playerImage = loadImage(player.width, player.high, "player.png", True)

treasure = Treasure(tx0, ty0, int(3*width/4), int(3*high/4))
treasureImage = loadImage(treasure.width, treasure.high, "treasure.png")

enemy = Enemy(ex0, ey0, width, high)
#enemy2 = Enemy(5, 5, width, high)
enemyImage = loadImage(enemy.width, enemy.high, "enemy.png", True)



font = pygame.font.SysFont("comicsans", 30)




while GameStatus.game_over == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameStatus.game_over = True

    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_ESCAPE] == 1:
        GameStatus.game_over = True

    if pressedKeys[pygame.K_SPACE] == 1:
        GameStatus.pause()

    if GameStatus.PAUSE == False:
        if pressedKeys[pygame.K_UP] == 1:
            player.moveUp()
        elif pressedKeys[pygame.K_DOWN] == 1:
            player.moveDown()
        elif pressedKeys[pygame.K_LEFT] == 1:
            player.moveLeft()
        elif pressedKeys[pygame.K_RIGHT] == 1:
            player.moveRight()

        enemy.move(player.x, player.y)
        #enemy2.move(player.x, player.y)


    screen.blit(backroundImage,(backround.x,backround.y))
    GameStatus.printInfo()
    screen.blit(treasureImage,(treasure.x,treasure.y))
    screen.blit(playerImage,(player.x,player.y))
    screen.blit(enemyImage,(enemy.x, enemy.y))
    #screen.blit(enemyImage,(enemy2.x, enemy2.y))
    pygame.display.flip()

    if GameStatus.PAUSE == True:
        pass

    treasure.checkForCollision(player.x, player.y)

    if enemy.checkEnemyCollision(player.x, player.y): #or enemy2.checkEnemyCollision(player.x, player.y):
        GameStatus.printOnCenter("Busted !!")
        pygame.display.flip()
        GameStatus.frame.tick(1)
        player.initPosition()

    GameStatus.frame.tick(100)
