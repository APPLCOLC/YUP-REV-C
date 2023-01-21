import pygame,random
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
    def __init__(self,args :dict):
        
        #DEFAULT CHARACTER CODE
        self.state="enter" #current behavior pattern for characters
                           #always "enter" at the beginning
                           #this is what tells characters when to swoop down or when to remain in place
                           #behavior patterns: "enter" "idle" "attack" "return" "die"
        self.health=1 #Health for characters.
                      #Almost always 1.
        self.scorevalue=10 #Score given to player
        self.offset = args["offset"] #offset that is used with the formation.
                            #This never changes.
        self.formationPos = args["formation_position"] #position that the entire formation follows.

        self.idlePos = [(self.formationPos[0]+self.offset[0]),(self.formationPos[1]+self.offset[1])] # current position, typically calculated with formationPos and offsets.
                         # This is only not the case when you are in the attacking state.

        self.offScreen = False #calculation to see if a character is visible onscreen
                               #This is only used in attack state.

        #TIMERS
        self.animation_frame_counter=0
        # self.whenToShoot=5

        #PYGAME-SPECIFIC CODE
        pygame.sprite.Sprite.__init__(self)
        self.animation_frame=0
        self.image = img.idle[self.animation_frame]
        self.rect = self.image.get_rect()
        self.groups = args["groups"]
        self.player = args["player"]

        #NOPE CODE
        self.level = args["level"]
        self.shoot_times = [] #the maximum amount will be like 10, which would only be achieved after level 100 or so
        self.frames_in_state = 0 #counter for shooting ; used for entrance, attack, etc

        self.shoot_times = Char.generate_shoot_times(level=self.level,starttime=15,endtime=45)
        

        #entrance code
        self.entrance_direction = random.choice(['l','r']) #this is the entrance they are COMING FROM, NOT the direction they are MOVING
        self.vertex = ( 0,0 )
        if self.entrance_direction == 'r':
            self.rect.center = (450,300) #location
            self.vertex = (450,400) #vertex for algebra
        elif self.entrance_direction == 'l':
            self.rect.center = (0,300) #location
            self.vertex = (25,400) #vertex for algebra


    def update(self):
        self.state_update()
        # self.movementUpdate()
        self.collision_update()
        # print(self.rect.center)
        # print(self.state)
        # print("-----")
        self.animation_update()

    def animation_update(self):
        self.image = img.idle[self.animation_frame] #sets current image
        self.animation_frame_counter += 1

        if self.animation_frame_counter >= 6: #updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame+=1

        if self.animation_frame>=len(img.idle)-1:
            self.animation_frame=0 #resets frame if out-of-index

    def state_update(self):
        # except Exception as error:print(error)
        if self.state=="enter": self.state_enter()
        if self.state=="idle_search": self.state_idle_search()
        if self.state=="idle": self.state_idle()
        if self.state=="attack": self.state_attack()
        if self.state=="return": self.state_return()
        # print(self.state)

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
            # print(self.rect.x)
            pass

        if abs(225-self.rect.x) <= 100 or abs(100 - self.rect.y) <= 50:
            self.state = "idle_search"
            self.frames_in_state = 0

    def state_idle_search(self):
        percent_complete = 0
        if abs(self.idlePos[0] - self.rect.center[0]) >= 10:
            if self.idlePos[0] < self.rect.center[0]:
                self.rect.x -= 5
            elif self.idlePos[0] > self.rect.center[0]:
                self.rect.x += 5
        else: percent_complete += 50
        if abs(self.idlePos[1] - self.rect.center[1]) >= 10:
            if self.idlePos[1] < self.rect.center[1]:
                self.rect.y -= 3
            elif self.idlePos[1] > self.rect.center[1]:
                self.rect.y += 3
        else: percent_complete += 50

        if percent_complete >= 100:
            self.state = "idle"

    def state_idle(self):
        self.rect.center=self.idlePos

    def state_attack(self):
        #checks if it's the first frame through checking if self.frames_in_state is zero
        #it will then run startup code
        if self.frames_in_state == 0:
            # print("SHOOT STATE")
            # picking shoot times for the first time
            self.shoot_times = Char.generate_shoot_times(level=self.level,starttime=15,endtime=45)

        # shooting based on timers
        if len(self.shoot_times) > 0:
            self.frames_in_state += 1
            if self.frames_in_state == self.shoot_times[0]:
                self.shoot()
                self.shoot_times.pop(0)

        self.rect.y+=5
        if self.rect.top>=600:
            self.rect.center=(self.idlePos[0],self.idlePos[1]-100)
            self.frames_in_state = 0
            self.state="return" #USUALLY 'return' BUT ENTRANCE FITS HERE

    def state_return(self):
        self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        self.rect.y+=5
        if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:
            self.state="idle"

    # def movementUpdate(self): self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])];self.rect.center=self.idlePos

    def collision_update(self):
        #please note that, with collision, there is no registration for touching YUP
        #this is because YUP handles collision with enemies herself
        #however, the enemies have to register how to collide with bullets
        bullet_hit = pygame.sprite.spritecollide(self, self.groups["bullet"], False, collided=pygame.sprite.collide_mask)
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

    def shoot(self):
        pos = pygame.Vector2(self.rect.center)
        player_pos = pygame.Vector2(self.player.rect.center)
        bullet=shared.Bullet(pos = pos , direction = (player_pos - pos))
        self.groups["universal"].add(bullet)
        self.groups["enemy"].add(bullet)
                         
    #picking shoot times for the first time
    def generate_shoot_times(level,starttime=1,endtime=45):
        shoot_times = []
        min,max = level // 10 , 1 + level // 5
        if min > 5: min = 0
        if max > 5: max = 5
        for i in range(random.randint((level // 10), (1 + level // 5))):
            shoot_times.append(random.randint(starttime,endtime))
        shoot_times.sort()   
        return shoot_times
         

