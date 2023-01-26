import pygame,random
from characters import shared


#SPIKE AND SPIKEBULLET CODE
class SPIKEBULLETS(pygame.sprite.Sprite):
    bullet_images = [
        pygame.transform.scale(pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-3.png"),(20,20)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-4.png"),(20,20)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-1.png"),(20,20)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("./assets/images/characters/SPIKE/SPIKEBULLET-2.png"),(20,20)).convert_alpha(), 
    ]
    def __init__(self, direction, coord):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.image = SPIKEBULLETS.bullet_images[direction]

        self.rect = self.image.get_rect()
        self.rect.center = coord
    def update(self):
        if self.direction == 0: self.rect.x -= 7.5
        if self.direction == 1: self.rect.x += 7.5
        if self.direction == 2: self.rect.y -= 7.5
        if self.direction == 3: self.rect.y += 7.5

        if self.rect.right <= 0 or self.rect.left >= 450 or self.rect.top <= 0 or self.rect.bottom >= 600: self.kill()


class Char(shared.Char):
    #IMAGE LOADING
    idle = []
    release = []
    for i in range(3):
        idle.append(
            pygame.transform.scale(pygame.image.load("./assets/images/characters/SPIKE/SPIKE-"+str(i+1)+".png"),(50,50)).convert_alpha(),
        )
    for i in range(3):
        release.append(
            pygame.transform.scale(pygame.image.load("./assets/images/characters/SPIKE/SPIKE-"+str(i+4)+".png"),(50,50)).convert_alpha(),
        )
    def __init__(self,args :dict):
        
        shared.Char.__init__(self,args)
        self.scorevalue = 400 #Score given to player

        #IMAGE CODE
        self.image = Char.idle[self.animation_frame]
        self.rect = self.image.get_rect()
        
        #SPIKE-SPECIFIC CODE
        self.shot=False
        self.initial_attack=False
        self.y_momentum=0
        self.frames_since_attack=0

        # ENTRANCE CODE
        self.entrance_direction = random.choice([1, -1])
        self.rect.x = -10 if self.entrance_direction == 1 else 450

    def animation_update(self):
        #FRAME UPDATING
        self.animation_frame_counter += 1
        if self.animation_frame_counter >= 6:  # updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame += 1

            #IDLE IMAGE UPDATE
            if not self.shot:
                #RESETTING FRAME
                if self.animation_frame >= len(Char.idle) - 1: self.animation_frame = 0
                #SETTING IMAGE
                self.image = Char.idle[self.animation_frame]
            #ATTACKING IMAGE UPDATE
            elif self.shot:
                #RESETTING FRAME
                if self.animation_frame >= len(Char.release) - 1: self.animation_frame = 0
                #SETTING IMAGE
                self.image = Char.release[self.animation_frame]

    def state_enter(self):
        #TEMPORARY
        shared.Char.state_enter(self)

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
        self.rect.center=(self.idlePos[0],self.rect.center[1])
        #shoot code
        if not self.shot and (abs(self.rect.center[0]-self.player.rect.center[0])<=5 or abs(self.rect.center[1]-self.player.rect.center[1])<=5):
            self.shot=True
            self.shoot()
        #return code
        if abs((self.rect.center[1]-(self.idlePos[1])))<=10 and self.frames_since_attack>=20: 
            self.shot=False
            self.initial_attack=False
            self.y_momentum=0
            self.state='idle'   
        
    def shoot(self):
        for i in range(4):
            bullet=SPIKEBULLETS(i,self.rect.center)
            self.groups["universal"].add(bullet)
            self.groups["enemy"].add(bullet)
    



        
         

