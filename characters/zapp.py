import pygame,random
from characters import shared

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
    def __init__(self,args :dict):
        
        #SELF-MADE CODE
        self.state="enter" #current behavior pattern for characters
                           #always "enter" at the beginnning
                           #this is what tells characters when to swoop down or when to remain in place
                           #behavior patterns: "enter" "idle" "attack" "return" "die"
        self.health=1 #Health for characters.
                      #Almost always 1.
        self.scorevalue=20 #Score given to player
        self.offset = args["offset"] #offset that is used with the formation.
                            #This never changes.
        self.formationPos = args["formation_position"] #position that the entire formation follows.

        self.idlePos = [(self.formationPos[0]+self.offset[0]),(self.formationPos[1]+self.offset[1])] # current position, typically calculated with formationPos and offsets.
                         # This is only not the case when you are in the attacking state.

        #TIMERS
        self.animation_frame_counter = 0

        #PYGAME-SPECIFIC CODE
        pygame.sprite.Sprite.__init__(self)
        self.animation_frame=0
        self.image = img.idle[self.animation_frame]
        self.rect = self.image.get_rect()
        self.groups = args["groups"]
        self.rect.y = -100 #entrance state starting position

        #ZAPP-SPECIFIC CODE
        self.frames=0
        self.zapping=False
        self.player = args ["player"]

    def update(self):
        self.stateUpdate()
        # self.movementUpdate()
        self.collisionUpdate()
        # print(self.rect.center)
        # print(self.state)
        # print("-----")
        self.animUpdate()

    def animUpdate(self):

        self.animation_frame_counter += 1

        if self.animation_frame_counter >= 6: #updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame+=1

        if self.state == "enter":
            self.image=pygame.transform.scale(self.image,(50,100)) #stretching image
        
        if self.zapping:
            self.image=pygame.transform.scale(self.image,(100,50))
            # self.rect.x-=50

        else:
            if self.animation_frame >= len(img.idle) - 1: self.animation_frame = 0  # resets frame if out-of-index
            self.image = img.idle[self.animation_frame]  # sets current image

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
        if self.rect.top>=600:
            self.rect.center=(self.offset[0],self.offset[1]-100)
            self.state="enter" #USUALLY 'return' BUT ENTRANCE FITS HERE
        
        #ZAPPING ZAPP AROUND
        self.frames+=1
        if self.frames>=15:
            self.frames=0
            self.rect.center=(random.randint(self.rect.center[0]-100,self.rect.center[0]+100),self.rect.center[1])
            self.zapping=True
        else:self.zapping=False

        if self.rect.left<0:self.rect.left=0
        if self.rect.right>450:self.rect.right=450

    def state_return(self):
        self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        self.rect.y+=10
        if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:self.state="idle"

    def collisionUpdate(self):
        #please note that, with collision, there is no registration for touching YUP
        #this is because YUP handles collision with enemies herself
        #however, the enemies have to register how to collide with bullets
        bullet_hit = pygame.sprite.spritecollide(self, self.groups["bullet"], False)
        for item in bullet_hit:
            item.health -= 1
            self.health -= 1
            if self.health < 1:
                die = shared.diePop(self.rect.center)
                self.groups["universal"].add(die)
                self.player.score += self.scorevalue
                self.state = "dead"
                self.kill()

    def formationUpdate(self,formationPos):
        self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])]
        self.formationPos=formationPos


        
         

