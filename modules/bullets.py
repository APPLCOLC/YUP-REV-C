import pygame,random
# from modules.sounds import *
#from main import *

#IMAGE LOADING
class bullet_images():
    default = pygame.image.load("./assets/images/bullets/bullet.png").convert_alpha()
    track = pygame.image.load("./assets/images/bullets/trackbullet.png").convert_alpha()
    quadLeft = pygame.image.load("./assets/images/bullets/quadLeft.png").convert_alpha()
    quadRight = pygame.image.load("./assets/images/bullets/quadRight.png").convert_alpha()
    quadUp = pygame.image.load("./assets/images/bullets/quadUp.png").convert_alpha()
    quadDown = pygame.image.load("./assets/images/bullets/quadDown.png").convert_alpha()
    quad = [quadLeft, quadRight, quadUp, quadDown];del quadLeft, quadRight, quadUp, quadDown
    quadFull = pygame.image.load("./assets/images/bullets/quadFull.png").convert_alpha()
    laser = pygame.image.load("./assets/images/bullets/laser.png").convert_alpha()
b=bullet_images()

#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(pygame.sprite.Sprite):
    def __init__(self,arg1,arg2,sounds,b=b):
        # shoot_bap[random.randint(0,3)].play()
        sounds.shoot_realistic.play()
        pygame.sprite.Sprite.__init__(self)
        self.health = 1
        self.image = pygame.Surface((20,20))
        self.image = b.default
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = (arg1,arg2)

    def update(self):
    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 25
        if self.rect.top <= 0:
            self.kill()
        if self.health <= 0:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self,arg1,arg2,sounds,enemyClass = None,b=b):
        self.sounds=sounds #EXPERIMENTAL RAM TEST
        sounds.shoot_missile.play()

        self.enemyClass = enemyClass

        #LOCK-ON DETECTION
        # if enemyClass != None and len(enemyClass) > 0:
        #     enemyClass = list(enemyClass)
        #     lockChar = enemyClass[random.randint(0,(len(enemyClass)-1))]
        #     self.lockX = lockChar.rect.x
        # else: self.lockX = None

        self.lockX = None
        self.lockY = None
        if self.enemyClass != None and len(self.enemyClass) > 0:
            tempList = list(self.enemyClass)
            self.lockIndex = random.randint(0,(len(self.enemyClass)-1))
            self.lockChar = tempList[self.lockIndex]
            self.lockX = self.lockChar.rect.x
            self.lockY = self.lockChar.rect.y
        else: self.lockX = None
        self.direction = "up"
        self.hasFlipped = True

        pygame.sprite.Sprite.__init__(self)
        self.health = 1
        self.image = pygame.Surface((30,50))
        self.image = b.track
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = (arg1,arg2)

    def update(self):

    #RE-UPDATING THE LOCK
        if self.lockX != None:self.lockX = self.lockChar.rect.x
        if self.lockY != None:self.lockY = self.lockChar.rect.y

    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        if self.lockX != None:
            if self.rect.x - self.lockX >= 5:
                self.rect.x-=5
                self.rect.x -= (self.rect.x - self.lockX) / 5
            elif self.rect.x - self.lockX <= -5:
                self.rect.x+=5
                self.rect.x += abs(self.rect.x - self.lockX) / 5
            else: self.lockX = None
        elif self.lockX == None:pass
        if self.lockY != None:
            if self.rect.y - self.lockY >= 5:
                self.rect.y -= 15
                if self.direction == "down" and self.hasFlipped: self.direction="up";self.hasFlipped=False
                # self.rect.y -= (self.rect.y - self.lockY) / 5
            elif self.rect.y - self.lockY <= -5:
                self.rect.y += 10
                if self.direction == "up" and self.hasFlipped: self.direction = "down";self.hasFlipped = False
                # self.rect.y += abs(self.rect.y - self.lockY) / 5
            else: self.lockY = None
        elif self.lockY == None:
            if self.direction == "down" and self.hasFlipped: self.direction = "up";self.hasFlipped = False
            self.rect.y -= 20

    #Kill Code
        if self.rect.top <= 0:
            self.kill()
        if self.health <= 0:
            self.kill()

    #Directional Code
        if not self.hasFlipped:self.image = pygame.transform.flip(self.image,False,True);self.hasFlipped = True

class Quad(pygame.sprite.Sprite):
    def __init__(self, direction, spawnx, spawny, b=b):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.health = 1
        self.image = pygame.Surface((20, 20))
        self.image = b.quad[direction]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.spawncoord=(spawnx,spawny)
        self.rect.center = self.spawncoord

    def update(self):
        if self.direction == 0: self.rect.x -= 25
        if self.direction == 1: self.rect.x += 25
        if self.direction == 2: self.rect.y -= 25
        if self.direction == 3: self.rect.y += 25

        if self.direction == 0 and self.rect.right <= 0: self.kill()
        if self.direction == 1 and self.rect.left >= 600: self.kill()
        if self.direction == 2 and self.rect.top <= 0: self.kill()
        if self.direction == 3 and self.rect.bottom >= 800: self.kill()

        if self.health <= 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self,arg1,arg2,b=b):
        # shoot_laser.play()
        pygame.sprite.Sprite.__init__(self)
        self.health = 15
        self.image = pygame.Surface((30,100))
        self.image = b.laser
        self.image = pygame.transform.scale(self.image, (30, 100))
        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = (arg1,arg2)

    def update(self):
    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 50
        if self.rect.bottom <= 0:
            self.kill()
        if self.health <= 0:
            self.kill()

class Large(pygame.sprite.Sprite):
    def __init__(self,arg1,arg2,b=b):
        # shoot_bap[random.randint(0,3)].play()
        # shoot_realistic.play()
        pygame.sprite.Sprite.__init__(self)
        self.health = 5
        self.image = pygame.Surface((100,100))
        self.image = b.default
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = (arg1,arg2)

    def update(self):
    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 25
        if self.rect.top <= 0:
            self.kill()
        if self.health <= 0:
            self.kill()



def shoot(playerx,playery,allsprites,bulletsprites, HurtSprites, sounds, bullettype = "default"):
    if len(bulletsprites)<2:
        if bullettype == "default" and len(bulletsprites)<2:
            
            bullet = Bullet(playerx,playery,sounds)
            allsprites.add(bullet)
            bulletsprites.add(bullet)
        elif bullettype == "large":
            bullet = Large(playerx,playery)
            allsprites.add(bullet)
            bulletsprites.add(bullet)
        elif bullettype == "missile":
            bullet = Missile(playerx,playery,sounds,enemyClass=HurtSprites)
            allsprites.add(bullet)
            bulletsprites.add(bullet)
        elif bullettype == "quad":
            bullet = Quad(0, playerx,playery)
            allsprites.add(bullet)
            bulletsprites.add(bullet)
            bullet2 = Quad(1, playerx, playery)
            allsprites.add(bullet2)
            bulletsprites.add(bullet2)
            bullet3 = Quad(2, playerx, playery)
            allsprites.add(bullet3)
            bulletsprites.add(bullet3)
            bullet4 = Quad(3, playerx, playery)
            allsprites.add(bullet4)
            bulletsprites.add(bullet4)
        elif bullettype == "laser":
            bullet = Laser(playerx, playery)
            allsprites.add(bullet)
            bulletsprites.add(bullet)
        else:
            bullet = Bullet(playerx,playery,sounds)
            allsprites.add(bullet)
            bulletsprites.add(bullet)
    # elif bullettype == "missile":
    #         bullet = Missile(playerx,playery,sounds,enemyClass=HurtSprites)
    #         allsprites.add(bullet)
    #         bulletsprites.add(bullet)
        

def display_bullet(WIN,positionTuple,bullettype,b=b):
    if bullettype == "default":
        image = pygame.transform.scale(b.default, (18, 18))
    elif bullettype == "large":
        image = pygame.transform.scale(b.default, (25, 25))
        positionTuple = (positionTuple[0]-4,positionTuple[1]-4)
    elif bullettype == "missile":
        image = pygame.transform.scale(b.track, (18, 18))
    elif bullettype == "quad":
        image = pygame.transform.scale(b.quadFull, (18, 18))
    elif bullettype == "laser":
        image = pygame.transform.scale(b.laser, (18, 18))
    else:
        pygame.transform.scale(b.default, (18, 18))
    WIN.blit(image,positionTuple)





