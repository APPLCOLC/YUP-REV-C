import pygame,time,random
from modules.characters import shared

class img():
    idle1=pygame.image.load("./assets/images/characters/FIHS/FIHS-1.png")
    idle2=pygame.image.load("./assets/images/characters/FIHS/FIHS-2.png")
    idle3=pygame.image.load("./assets/images/characters/FIHS/FIHS-3.png")
    idle=[idle1,idle2,idle3]
    chomp1=pygame.image.load("./assets/images/characters/FIHS/FIHS-4.png")
    chomp2=pygame.image.load("./assets/images/characters/FIHS/FIHS-5.png")
    chomp3=pygame.image.load("./assets/images/characters/FIHS/FIHS-6.png")
    chomp4=pygame.image.load("./assets/images/characters/FIHS/FIHS-7.png")
    chomp=[chomp1,chomp2,chomp3,chomp4]
    del idle1,idle2,idle3,chomp1,chomp2,chomp3

    for i in range(len(idle)): idle[i]=pygame.transform.scale(idle[i],(40,40)).convert_alpha()
    for i in range(len(chomp)): chomp[i]=pygame.transform.scale(chomp[i],(40,40)).convert_alpha()
    
class Char(pygame.sprite.Sprite):
    def __init__(self,allsprites,bullets,player,enemies,formationPos=(0,0), offset=(0,0)):
        
        #SELF-MADE CODE
        self.state="enter" #current behavior pattern for characters
                           #always "enter" at the beginnning
                           #behavior patterns: "enter" "idle" "attack" "return" "die"
        self.health=1 #Health for characters.
                      #Almost always 1.
        self.scorevalue=10 #Score given to player
        self.RCM=False #RCM = Return Condition Met.
                       #This is only used in attack state.
                       #This is to check if the character should return or not.
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
        self.whenToShoot=random.randint(10,60) #HOW OFTEN a character should SHOOT
        # self.whenToShoot=5

        #PIRAHNA-SPECIFIC CODE
        self.player=player #THIS is to get positions for when the sprite is in attack state
        self.direction="right"
        self.y_momentum=0
        self.x_momentum=0

        #PYGAME-SPECIFIC CODE
        pygame.sprite.Sprite.__init__(self)
        self.frame=0;self.image = img.chomp[self.frame]
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
            if self.state=="idle" or self.state=="enter":
                #RESETTING FRAME
                if self.frame >= len(img.idle) - 1: self.frame = 0
                #SETTING IMAGE
                self.image = img.idle[self.frame]
            #ATTACKING IMAGE UPDATE
            else:
                #RESETTING FRAME
                if self.frame >= len(img.chomp) - 1: self.frame = 0
                #SETTING IMAGE
                self.image = img.chomp[self.frame]
                #FLIPPING IMAGE BASED ON DIRECTION
                if self.direction=="left": self.image=pygame.transform.flip(self.image,True,False)

        if self.state == "enter":
            self.image=pygame.transform.scale(self.image,(20,75)) #stretching image
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
        #SHOOT CODE
        self.shootCounter+=1 
        if self.shootCounter>=self.whenToShoot:self.shootCounter=0;self.shoot() 

        #MOVING DOWN CODE
        self.y_momentum+=0.1
        if self.y_momentum>=5:self.y_momentum=5 #prevents too fast of a speed
        if (self.player.rect.x-self.rect.x)>10:
            self.x_momentum+=0.1
            self.direction="right"
        elif (self.player.rect.x-self.rect.x)<-10:
            self.x_momentum-=0.1
            self.direction = "left"
        self.rect.x+=self.x_momentum
        self.rect.y+=self.y_momentum

        #CHANGING STATE TO RETURN STATE
        if self.rect.top>=600: #ends early to show the character turning around and coming back
            self.state="return"
    def state_return(self):
        #MOVING UP CODE
        y_distance=self.rect.center[1]-(self.formationPos[1]+self.offset[1])
        y_condition_met=(y_distance<10)and(y_distance>-10)
        if y_condition_met:self.y_momentum=0
        if (not y_condition_met) and (y_distance>5):self.y_momentum-=0.1
        if (not y_condition_met) and (y_distance<-5):self.y_momentum+=0.1
        if self.y_momentum<=-10:self.y_momentum=-10
        if self.y_momentum>=10:self.y_momentum=10
        self.rect.y+=self.y_momentum

        x_distance = self.rect.center[0] - (self.formationPos[0]+self.offset[0])
        x_condition_met = (x_distance < 10) and (x_distance > -10)
        if x_condition_met:self.x_momentum=0
        if (not x_condition_met) and (x_distance>5):self.x_momentum-=0.1
        if (not x_condition_met) and (x_distance<-5):self.x_momentum+=0.1
        if self.x_momentum<=-10:self.x_momentum=-10
        if self.x_momentum>=10:self.x_momentum=10
        self.rect.x+=self.x_momentum

        if x_condition_met and y_condition_met: self.state="idle"


        #MOVING SIDE-TO-SIDE CODE

        
        #RETURN CONDITION MET CODE
        # self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        # self.rect.y+=10
        # if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:self.state="idle"
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

    def hitboxSwap(self):pass

    def shoot(self):
        bullet=shared.hurtBullet(self.rect.center,self.player.rect.x)
        self.allsprites.add(bullet)
        self.enemies.add(bullet)
                         
        
         

