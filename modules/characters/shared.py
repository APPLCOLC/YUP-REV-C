import pygame,time

#IMAGES
class SHARECHAR():
    hats = {
        "sunglasses":pygame.image.load("./assets/images/SHARED/HATS/SunglassHat.png").convert_alpha(),
        "owo": pygame.image.load("./assets/images/SHARED/HATS/OwOHat.png").convert_alpha(),
        "hardhat": pygame.image.load("./assets/images/SHARED/HATS/HardHat.png").convert_alpha(),
        "eye": pygame.image.load("./assets/images/SHARED/HATS/EyeHat.png").convert_alpha(),
        "void": pygame.image.load("./assets/images/SHARED/HATS/VoidHat.png").convert_alpha()
    }
    deathPop=[];deathBoom=[]
    for i in range(3):deathPop.append(pygame.transform.scale(pygame.image.load("./assets/images/SHARED/POP/Death_Pop-"+(str(i+1))+".png"),(60,60)).convert_alpha()) #creates,resizes,and appends
    for i in range(17):deathBoom.append(pygame.image.load("./assets/images/SHARED/BOOM/Death_Explosion-" + str(i+1) + ".png").convert_alpha()) #creates, doesn't resize
    hurtBullet=pygame.image.load("./assets/images/bullets/hurtBullet.png").convert_alpha()

#UNIVERSAL SPRITES
class charHat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        pass
class diePop(pygame.sprite.Sprite):
    def __init__(self,coordCENTER=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = SHARECHAR.deathPop[self.index]
        self.rect = self.image.get_rect(); self.rect.center = coordCENTER
        self.start=time.time()
    def update(self):
        end=time.time()
        if end-self.start >= 0.05: self.index += 1;self.start = time.time()
        if self.index>2:self.index=0;self.kill()
        self.image = SHARECHAR.deathPop[self.index]
class dieBoom(pygame.sprite.Sprite):
    def __init__(self,coordCENTER=(0,0),size=None):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = SHARECHAR.deathBoom[self.index]
        self.rect = self.image.get_rect(); self.rect.center = coordCENTER
        self.start=time.time()
        self.size=size
        self.coordCENTER=coordCENTER
    def update(self):
        end=time.time()

        if end-self.start >= 0.05: self.index += 1;self.start = time.time()

        if self.index>16:self.index=0;self.kill()

        self.image = SHARECHAR.deathBoom[self.index]

        if self.size!=None:self.image=pygame.transform.scale(self.image,self.size)
        self.rect=self.image.get_rect()
        self.rect.center=self.coordCENTER

class hurtBullet(pygame.sprite.Sprite):
    def __init__(self,pos=(0,0),aimX=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(SHARECHAR.hurtBullet,(10,10))
        self.rect = self.image.get_rect()
        self.pos,self.aim=pos,aimX #pos is the central bullet spawn position (tuple), aim is the position it aims towards (int - x)
        self.rect.center=self.pos
    def update(self):
        self.rect.y+=7.5
        self.rect.x+=(self.aim-self.pos[0])/50
        if self.rect.y>=800 or self.rect.y<=0 or self.rect.x >=600 or self.rect.x <=0: self.kill()

