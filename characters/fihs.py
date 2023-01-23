import pygame,random
from characters import shared

 
class Char(shared.Char):

    #loading images
    idle,chomp = [],[]
    for i in range(3):
        idle.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/FIHS/FIHS-"+str(i+1)+".png"),(40,40)).convert_alpha())
    for i in range(4):
        chomp.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/FIHS/FIHS-"+str(i+4)+".png"),(40,40)).convert_alpha())

    def __init__(self,args :dict):
        
        shared.Char.__init__(self,args)
        
        self.scorevalue = 20

        #PIRAHNA-SPECIFIC CODE
        self.player = args["player"] #THIS is to get positions for when the sprite is in attack state
        self.direction = "right"
        self.y_momentum = 0
        self.x_momentum = 0

        #IMAGE CODE
        self.image = Char.chomp[self.animation_frame]
        self.rect = self.image.get_rect()
        
        #STARTUP CODE
        self.rect.center = ( 
            random.randint(25,425),
            610
        )
        #the entrance state will move in a cubic function, although x won't move 


    def animation_update(self):
        #FRAME UPDATING
        self.animation_frame_counter += 1

        if self.animation_frame_counter >= 6:  # updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame += 1

            if self.state=="idle" or self.state=="enter":
                #RESETTING FRAME
                if self.animation_frame >= len(Char.idle) - 1: self.animation_frame = 0
                #SETTING IMAGE
                self.image = Char.idle[self.animation_frame]

            elif self.state == "attack" or self.state == "return":
                #RESETTING FRAME
                if self.animation_frame >= len(Char.chomp) - 1: self.animation_frame = 0
                #SETTING IMAGE
                self.image = Char.chomp[self.animation_frame]
                #FLIPPING IMAGE BASED ON DIRECTION
                if self.direction=="left": self.image=pygame.transform.flip(self.image,True,False)

    def state_enter(self):
        #jump down code
        self.rect.center = (self.idlePos[0],self.rect.center[1]) #matching x position
        if self.idlePos[1] > self.rect.center[1]: 
            self.rect.y += 35
        elif self.idlePos[1] < self.rect.center[1]: 
            self.rect.y -= 35
        if (30)>(self.idlePos[1]-self.rect.center[1])>(-30):
            self.rect.center = self.idlePos
            self.state = "idle"

    def state_attack(self):
        #MOVING DOWN CODE
        self.y_momentum+=0.1
        #preventing too fast a speed
        self.y_momentum=5 if self.y_momentum>=5 else self.y_momentum

        #changing direction
        if (self.player.rect.x-self.rect.x)>10:
            self.x_momentum+=0.1
            self.direction="right"
        elif (self.player.rect.x-self.rect.x)<-10:
            self.x_momentum-=0.1
            self.direction = "left"
        #moving
        self.rect.x+=self.x_momentum
        self.rect.y+=self.y_momentum

        #CHANGING STATE TO RETURN STATE
        if self.rect.top>=450: #ends early to show the character turning around and coming back
            self.state="return"

    def state_return(self):
        #MOVING UP CODE
        y_distance = self.rect.center[1]-(self.idlePos[1])
        y_condition_met = (y_distance<10)and(y_distance>-10)
        #stop code
        if y_condition_met:
            self.y_momentum=0
        #up momentum
        if (not y_condition_met) and (y_distance>5):
            self.y_momentum-=0.1
        if (not y_condition_met) and (y_distance<-5):
            self.y_momentum+=0.1
        #momentum cap
        if self.y_momentum<=-10:
            self.y_momentum=-10
        if self.y_momentum>=10:
            self.y_momentum=10
        #moving
        self.rect.y+=self.y_momentum

        #MOVING HORIZONTAL CODE
        x_distance = self.rect.center[0] - (self.idlePos[1])
        x_condition_met = (x_distance < 10) and (x_distance > -10)
        #stop code
        if x_condition_met:
            self.x_momentum=0
        #horizontal momentum
        if (not x_condition_met) and (x_distance>5):
            self.x_momentum-=0.1
        if (not x_condition_met) and (x_distance<-5):
            self.x_momentum+=0.1
        #momentum cap
        if self.x_momentum<=-10: self.x_momentum=-10
        elif self.x_momentum>=10: self.x_momentum=10
        self.rect.x+=self.x_momentum

        #END CODE
        if x_condition_met and y_condition_met:
             self.state="idle"

   
        
         

