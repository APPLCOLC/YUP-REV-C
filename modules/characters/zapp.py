import pygame,time
from modules.characters import shared

class img():
    idle1 = pygame.image.load("./assets/images/characters/ZAPP/ZAPP-1.png")
    idle2 = pygame.image.load("./assets/images/characters/ZAPP/ZAPP-2.png")
    idle3 = pygame.image.load("./assets/images/characters/ZAPP/ZAPP-3.png")
    idle4 = pygame.image.load("./assets/images/characters/ZAPP/ZAPP-4.png")
    idle=[idle1,idle2,idle3,idle4]
    for i in range(len(idle)):
        idle[i]=pygame.transform.scale(idle[i],(50,50)).convert_alpha()
    del idle1,idle2,idle3,idle4

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

        #TIMERS
        self.frameStart=time.time()

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

        end=time.time()

        if end-self.frameStart >= 0.1: #updates frame if enough time has passed
            self.frameStart = time.time()
            self.frame+=1

        if self.state == "enter":
            self.image=pygame.transform.scale(self.image,(10,50)) #stretching image
            self.rect.x+=20 #centering image

        else:
            if self.frame >= len(img.idle) - 1: self.frame = 0  # resets frame if out-of-index
            self.image = img.idle[self.frame]  # sets current image

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
        self.rect.y+=5
        if self.rect.top>=800:
            self.rect.center=(self.offset[0],self.offset[1]-100)
            self.state="enter" #USUALLY 'return' BUT ENTRANCE FITS HERE

    def state_return(self):
        self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        self.rect.y+=10
        if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:self.state="idle"

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


        
         

