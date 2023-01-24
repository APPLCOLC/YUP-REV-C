import pygame,random,math
from characters import shared


class Char(shared.Char):
    idle = []
    for i in range(4):
        idle.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/ZAPP/ZAPP-"+str(i+1)+".png"),(50,50)).convert_alpha(),)

    def __init__(self,args :dict):

        shared.Char.__init__(self,args)
    
        self.scorevalue= 250 #Score given to player

        self.rect.y = -100 #entrance state starting position

        #ZAPP-SPECIFIC CODE
        self.frames=0
        self.zapping=False
        self.player = args ["player"]

        #ENTRANCE CODE
        self.entrance_direction = random.choice([1,-1])
        if self.entrance_direction == 1: self.rect.x = -10
        else: self.rect.x = 450


    def animation_update(self):

        self.animation_frame_counter += 1

        if self.animation_frame_counter >= 6: #updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame+=1

        if self.state == "enter":
            self.image=pygame.transform.scale(self.image,(50,100)) #stretching image
        
        if self.zapping:
            self.image=pygame.transform.scale(self.image,(100,50))
            self.zapping=False
            # self.rect.x-=50

        else:
            if self.animation_frame >= len(Char.idle) - 1: self.animation_frame = 0  # resets frame if out-of-index
            self.image = Char.idle[self.animation_frame]  # sets current image

    def state_enter(self):
        self.rect.x += self.entrance_direction
        self.rect.center = (
            self.rect.center[0],
            (math.sin((self.rect.center[0]+200)/25)*200 + 300)
        )
        if abs(self.rect.center[0]-225) <= 10:
            self.state = "idle_search"

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
        else:
            self.zapping=False

        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>450:
            self.rect.right=450

    def state_return(self):
        self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        self.rect.y+=5
        if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:
            self.state="idle"


        
         

