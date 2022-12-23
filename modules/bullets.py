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

class Cheat(pygame.sprite.Sprite):
    def __init__(self,arg1,arg2,sounds,enemyClass = None,b=b):
        pygame.sprite.Sprite.__init__(self)


        self.sounds=sounds #EXPERIMENTAL RAM TEST
        # sounds.shoot_missile.play()

        self.enemyClass = enemyClass

        #this shit just picks a random character to touch and touches it :)

        if self.enemyClass != None and len(self.enemyClass) > 0:
            self.lockIndex = random.randint(0,(len(list(self.enemyClass))-1))
            self.lockChar = list(self.enemyClass)[self.lockIndex]
        else:self.kill() 
       
        self.health = 1

        self.image = b.default
        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        try:self.rect.center = self.lockChar.rect.center
        except:self.kill()

    def update(self):
        if self.health<=0:self.kill()
        self.kill()

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
            bullet = Cheat(playerx,playery,sounds,enemyClass=HurtSprites)
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





