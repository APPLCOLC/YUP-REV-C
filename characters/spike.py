import pygame,time
from characters import shared

class img():
    idle1 = pygame.image.load("./assets/images/characters/SPIKE/SPIKE-1.png")
    idle2 = pygame.image.load("./assets/images/characters/SPIKE/SPIKE-2.png")
    idle3 = pygame.image.load("./assets/images/characters/SPIKE/SPIKE-3.png")
    idle = [idle1,idle2,idle3]
    del idle1,idle2,idle3
    release1 = pygame.image.load("./assets/images/characters/SPIKE/SPIKE-4.png")
    release2 = pygame.image.load("./assets/images/characters/SPIKE/SPIKE-5.png")
    release3 = pygame.image.load("./assets/images/characters/SPIKE/SPIKE-6.png")
    release = [release1, release2, release3]
    del release1, release2, release3
    bulletleft = pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-3.png")
    bulletright = pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-4.png")
    bulletup = pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-1.png")
    bulletdown = pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-2.png")
    bullet = [bulletleft,bulletright,bulletup,bulletdown]
    del bulletleft,bulletright,bulletup,bulletdown

    for i in range(len(idle)):idle[i]=pygame.transform.scale(idle[i],(50,50)).convert_alpha()
    for i in range(len(release)):release[i]=pygame.transform.scale(release[i],(50,50)).convert_alpha()
    for i in range(len(bullet)):bullet[i]=pygame.transform.scale(bullet[i],(20,20)).convert_alpha()

#SPIKE AND SPIKEBULLET CODE
class SPIKEBULLETS(pygame.sprite.Sprite):
    def __init__(self, direction, coord):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.image = img.bullet[direction]

        self.rect = self.image.get_rect()
        self.rect.center = coord
    def update(self):
        if self.direction == 0: self.rect.x -= 7.5
        if self.direction == 1: self.rect.x += 7.5
        if self.direction == 2: self.rect.y -= 7.5
        if self.direction == 3: self.rect.y += 7.5

        if self.rect.right <= 0 or self.rect.left >= 450 or self.rect.top <= 0 or self.rect.bottom >= 600: self.kill()
class Char(pygame.sprite.Sprite):
    def __init__(self,allsprites,bullets,player,enemies,formationPos=(0,0), offset=(0,0)):
        
        #SELF-MADE CODE
        self.state="enter" #current behavior pattern for characters
                           #always "enter" at the beginnning
                           #this is what tells characters when to swoop down or when to remain in place
                           #behavior patterns: "enter" "idle" "attack" "return" "die"
        self.health=1 #Health for characters.
                      #Almost always 1.
        self.scorevalue=10 #Score given to player

        self.offset = offset #offset that is used with the formation.
                            #This never changes.
        self.formationPos = formationPos #position that the entire formation follows.

        self.idlePos = [(self.formationPos[0]+self.offset[0]),(self.formationPos[1]+self.offset[1])] # current position, typically calculated with formationPos and offsets.
                         # This is only not the case when you are in the attacking state.

        self.offScreen = False #calculation to see if a character is visible onscreen
                               #This is only used in attack state.

        #TIMERS
        self.frameStart=time.time()
        # self.whenToShoot=5
        
        #SPIKE-SPECIFIC CODE
        self.shot=False
        self.initial_attack=False
        self.y_momentum=0
        self.frames_since_attack=0


        #PYGAME-SPECIFIC CODE
        pygame.sprite.Sprite.__init__(self)
        self.frame=0;self.image = img.idle[self.frame]
        self.rect = self.image.get_rect()
        self.bullets,self.allsprites,self.player,self.enemies=bullets,allsprites,player,enemies
        self.rect.y = -100 #entrance state starting position

    def update(self):
        self.stateUpdate()
        # self.movementUpdate()
        self.collisionUpdate()
        # print(self.rect.center)
        # print(self.state)
        # print("-----")
        self.animUpdate()

    def animUpdate(self):
        #FRAME UPDATING
        end = time.time()
        if end - self.frameStart >= 0.1:  # updates frame if enough time has passed
            self.frameStart = time.time()
            self.frame += 1

            #IDLE IMAGE UPDATE
            if not self.shot:
                #RESETTING FRAME
                if self.frame >= len(img.idle) - 1: self.frame = 0
                #SETTING IMAGE
                self.image = img.idle[self.frame]
            #ATTACKING IMAGE UPDATE
            elif self.shot:
                #RESETTING FRAME
                if self.frame >= len(img.release) - 1: self.frame = 0
                #SETTING IMAGE
                self.image = img.release[self.frame]

        if self.state == "enter":
            self.image=pygame.transform.scale(self.image,(20,75)) #stretching image
            self.rect.x+=20 #centering image
        #updating hitbox
        # self.rect=self.image.get_rect()
    def stateUpdate(self):
        # except Exception as error:print(error)
        if self.state=="enter": self.state_enter()
        if self.state=="idle": self.state_idle()
        if self.state=="attack": self.state_attack()
        if self.state=="return": self.state_return()
        # print(self.state)

    def state_enter(self):
        #zooms down to the idle position
        #x will already match
        #starts at top

        #movement code
        self.rect.center = (self.idlePos[0],self.rect.center[1]) #matching x position
        if self.idlePos[1] > self.rect.center[1]: self.rect.y += 35
        elif self.idlePos[1] < self.rect.center[1]: self.rect.y -= 35
        if (30)>(self.idlePos[1]-self.rect.center[1])>(-30):
            self.rect.center = self.idlePos
            self.state = "idle"
            # print("state is now idle")

    def state_idle(self):
        self.rect.center=self.idlePos
    def state_attack(self):
        #start code, to launch spike
        if not self.initial_attack:
            self.y_momentum=10
            self.initial_attack=True
            self.frames_since_attack=0
        # print(str(self.frames_since_attack),"|",str(self.y_momentum),"|",str(abs((self.rect.center[1]-(self.formationPos[1]+self.offset[1])))))
        #movement update
        self.y_momentum-=0.1
        self.rect.y+=self.y_momentum
        self.frames_since_attack+=1
        self.rect.center=((self.formationPos[0]+self.offset[0]),self.rect.center[1])
        #shoot code
        if not self.shot and (abs(self.rect.center[0]-self.player.rect.center[0])<=5 or abs(self.rect.center[1]-self.player.rect.center[1])<=5):
            self.shot=True
            self.shoot()
        #return code
        if abs((self.rect.center[1]-(self.formationPos[1]+self.offset[1])))<=10 and self.frames_since_attack>=20: 
            self.shot=False
            self.initial_attack=False
            self.y_momentum=0
            self.state='idle'   
    def state_return(self):
        self.rect.center=[self.idlePos[0],self.rect.center[1]]
        self.rect.y+=10
        if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:self.state="idle"
    def shoot(self):
        for i in range(4):
            bullet=SPIKEBULLETS(i,self.rect.center)
            self.allsprites.add(bullet)
            self.enemies.add(bullet)
    def state_die(self):pass
    # def movementUpdate(self): self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])];self.rect.center=self.idlePos
    def collisionUpdate(self):
        #please note that, with collision, there is no registration for touching YUP
        #this is because YUP handles collision with enemies herself
        #however, the enemies have to register how to collide with bullets
        BulletHit = pygame.sprite.spritecollide(self, self.bullets, False)
        for item in BulletHit:
            item.health -= 1
            self.health -= 1
            if self.health < 1:
                die = shared.diePop(self.rect.center)
                self.allsprites.add(die)
                self.player.score += self.scorevalue
                self.state = "dead"
                self.kill()
    def formationUpdate(self,formationPos):
        self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])]
        self.formationPos=formationPos


        
         

