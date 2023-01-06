import pygame,time,random
from characters import shared

class img():
    idle1 = pygame.image.load("./assets/images/characters/NOPE/NOPE-1.png")
    idle2 = pygame.image.load("./assets/images/characters/NOPE/NOPE-2.png")
    idle3 = pygame.image.load("./assets/images/characters/NOPE/NOPE-3.png")
    idle = [idle1, idle2, idle3]
    for i in range(len(idle)):idle[i]=pygame.transform.scale(idle[i],(35,35)).convert_alpha()
    del idle1, idle2, idle3
    death1 = pygame.image.load("./assets/images/characters/NOPE/NOPE-4.png")
    death1 = pygame.transform.scale(death1,(35,35)).convert_alpha()
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
        self.shootCounter=0 #counter for WHEN the bullet should shoot
        self.whenToShoot=random.randint(45,60) #HOW OFTEN a character should SHOOT
        # self.whenToShoot=5

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
        self.image = img.idle[self.frame] #sets current image
        end=time.time()
        if end-self.frameStart >= 0.1: #updates frame if enough time has passed
            self.frameStart = time.time()
            self.frame+=1
        if self.frame>=len(img.idle)-1:self.frame=0 #resets frame if out-of-index
        if self.state == "enter":
            self.image=pygame.transform.scale(self.image,(10,50)) #stretching image
            self.rect.x+=20 #centering image
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
        self.shootCounter+=1 #SHOOT COUNTER CODE
        if self.shootCounter>=self.whenToShoot:self.shootCounter=0;self.shoot() #SHOOT CODE
        self.rect.y+=5
        if self.rect.top>=600:
            self.rect.center=(self.offset[0],self.offset[1]-100)
            self.state="enter" #USUALLY 'return' BUT ENTRANCE FITS HERE
    def state_return(self):
        self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        self.rect.y+=10
        if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:self.state="idle"
    def state_die(self):pass
    # def movementUpdate(self): self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])];self.rect.center=self.idlePos
    def collisionUpdate(self):
        #please note that, with collision, there is no registration for touching YUP
        #this is because YUP handles collision with enemies herself
        #however, the enemies have to register how to collide with bullets
        BulletHit = pygame.sprite.spritecollide(self, self.bullets, False, collided=pygame.sprite.collide_mask)
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

    def hitboxSwap(self):pass

    def shoot(self):
        bullet=shared.hurtBullet(self.rect.center,self.player.rect.x)
        self.allsprites.add(bullet)
        self.enemies.add(bullet)
                         
        
         

