import pygame
from characters import shared

    
class Char(shared.Char):
    idle,prep,freefall=[],[],[]
    for i in range(5):
        idle.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-"+str(i+1)+".png"),(40,40)).convert_alpha())
    for i in range(7):
        prep.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-"+str(i+6)+".png"),(40,40)).convert_alpha())
    for i in range(3):
        freefall.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-"+str(i+13)+".png"),(40,40)).convert_alpha())
        

    def __init__(self,args :dict):
        #INIT
        shared.Char.__init__(self,args)
        
        self.scorevalue= 50
        # STICKMAN-SPECIFIC CODE
        self.locked_in = False
        self.y_momentum = self.x_momentum = 0
        #IMAGE
        self.image = Char.freefall[self.animation_frame]
        self.rect = self.image.get_rect()

    def animation_update(self):
        # FRAME UPDATING
        self.animation_frame_counter += 1
        if self.animation_frame_counter >= 6:  # updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame += 1
           #SETTING IMAGE 
            if self.state == "idle":# IDLE IMAGE UPDATE
                if self.animation_frame >= len(Char.idle) - 1: self.animation_frame = 0 # RESETTING FRAME
                self.image = Char.idle[self.animation_frame]# SETTING IMAGE
            elif self.state == "attack" or self.state == "enter":# ATTACKING IMAGE UPDATE
                if self.animation_frame >= len(Char.freefall) - 1: self.animation_frame = 0 # RESETTING FRAME
                self.image = Char.freefall[self.animation_frame]# SETTING IMAGE
            elif self.state == "prep":
                if self.animation_frame >= len(Char.prep) - 1: self.animation_frame = 0 #this SHOULD NOT OCCUR since at this point he would have jumped
                self.image = Char.prep[self.animation_frame]


    def state_update(self):
        if self.state == "enter": self.state_enter()
        if self.state == "idle": self.state_idle()
        if self.state == "attack": self.state_attack()
        if self.state == "return": self.state_return()
        if self.state == "prep": self.state_prep()


    def state_enter(self):
        # zooming up or down
        self.rect.center = (self.idlePos[0], self.rect.center[1])  # matching x position
        if self.idlePos[1] > self.rect.center[1]:
            self.rect.y += 10
        elif self.idlePos[1] < self.rect.center[1]:
            self.rect.y -= 10
        if (30) > (self.idlePos[1] - self.rect.center[1]) > (-30):
            self.rect.center = self.idlePos
            self.state = "idle"


    def state_prep(self):
        self.rect.center = self.idlePos
        #Creating variables to make the jump fine
        if self.animation_frame >= len(Char.prep) - 2:
            #WAHOO JUMP
            self.animation_frame=0
            self.locked_in=True
            self.state="attack"
            #VISUAL EXPLOSION
            explosion=shared.dieBoom(self.rect.center,(50,50))
            self.groups["universal"].add(explosion)
        self.y_momentum=-5


    def state_attack(self):
        #SENDING BACK IF MANUALLY_ATTACKED
        if not self.locked_in:
            self.animation_frame=0
            self.state="prep"
            return

        # MOVING DOWN CODE
        self.y_momentum+=0.2
        self.rect.y+=self.y_momentum

        #RETURN CODE
        if self.rect.top>=600:
            self.locked_in=False
            self.rect.bottom=0
            self.state="enter"







