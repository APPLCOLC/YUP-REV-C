import pygame,random
from characters import shared

#TEST
class Char(shared.Char):
    idle = []
    for i in range(4):
        idle.append(
            pygame.transform.scale(pygame.image.load("./assets/images/characters/NOPE/NOPE-"+str(i+1)+".png"),(35,35)).convert_alpha()
        )
    def __init__(self,args:dict):
        shared.Char.__init__(self,args)

        #spritesheet
        self.image = Char.idle[self.animation_frame]
        self.rect = self.image.get_rect() 

        #most of nope's arguments are default, so no value rewrites

        #entrance values
        self.shoot_times = Char.generate_shoot_times(level=self.level,starttime=15,endtime=45)
        self.entrance_direction = random.choice(['l','r']) #this is the entrance they are COMING FROM, NOT the direction they are MOVING
        self.vertex = ( 0,0 )
        if self.entrance_direction == 'r':
            self.rect.center = (450,300) #location
            self.vertex = (450,400) #vertex for algebra
        elif self.entrance_direction == 'l':
            self.rect.center = (0,300) #location
            self.vertex = (25,400) #vertex for algebra

    #ANIMATED SPRITESHEETS
    def animation_update(self):
        self.image = Char.idle[self.animation_frame] #sets current image
        self.animation_frame_counter += 1

        if self.animation_frame_counter >= 6: #updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame+=1

        if self.animation_frame>=len(Char.idle)-1:
            self.animation_frame=0 #resets frame if out-of-index
    

    #ALGEBRAIC-CENTERED ENTRANCE
    def state_enter(self):
        #shoot code
        if len(self.shoot_times) > 0:
            self.frames_in_state += 1
            if self.frames_in_state == self.shoot_times[0]:
                self.shoot()
                self.shoot_times.pop(0)

        #movement parabola code
        if self.entrance_direction == 'l':
            #moving to the right, coming from left
            self.rect.x += 2
            self.rect.y = (-(1 / 50) * ((self.rect.x + self.vertex[0]) ** 2) + self.vertex[1])


        elif self.entrance_direction == 'r':
            # moving to the right, coming from left
            self.rect.x -= 2
            self.rect.y = (-(1 / 50) * ((self.rect.x - self.vertex[0]) ** 2) + self.vertex[1])

        if abs(225-self.rect.x) <= 100 or abs(100 - self.rect.y) <= 50:
            self.state = "idle_search"
            self.frames_in_state = 0
    
    def state_attack(self):
        #checks if it's the first frame through checking if self.frames_in_state is zero
        #it will then run startup code
        if self.frames_in_state == 0:
            # picking shoot times for the first time
            self.shoot_times = Char.generate_shoot_times(level=self.level,starttime=15,endtime=45)

        self.frames_in_state += 1

        # shooting based on timers
        if len(self.shoot_times) > 0:
            if self.frames_in_state == self.shoot_times[0]:
                self.shoot()
                self.shoot_times.pop(0)

        self.rect.y+=5
        if self.rect.top>=600:
            self.rect.center=(self.idlePos[0],self.idlePos[1]-100)
            self.frames_in_state = 0
            self.state="return" #USUALLY 'return' BUT ENTRANCE FITS HERE

    def state_return(self):
        self.rect.center=[self.idlePos[0],self.rect.center[1]]
        self.rect.y+=5
        if abs(self.rect.center[1]-self.idlePos[1])<5:
            self.state="idle"



              
