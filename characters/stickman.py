import pygame
from characters import shared


class img():
    #definitons
    idle1=pygame.image. load("./assets/images/characters/STICKMAN/STICKMAN-1.png")
    idle2=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-2.png")
    idle3=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-3.png")
    idle4=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-4.png")
    idle5=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-5.png")
    prep1=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-6.png")
    prep2=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-7.png")
    prep3=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-8.png")
    prep4=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-9.png")
    prep5=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-10.png")
    prep6=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-11.png")
    prep7=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-12.png")
    freefall1=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-13.png")
    freefall2=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-14.png")
    freefall3=pygame.image.load("./assets/images/characters/STICKMAN/STICKMAN-15.png")
    #list creation
    idle=[idle1,idle2,idle3,idle4,idle5]
    prep=[prep1,prep2,prep3,prep4,prep5,prep6,prep7]
    freefall=[freefall1,freefall2,freefall3]
    #deletion of originals
    del idle1,idle2,idle3,idle4,idle5,prep1,prep2,prep3,prep4,prep5,prep6,prep7,freefall1,freefall2,freefall3
    #resizing
    for i in range(len(idle)): idle[i]=pygame.transform.scale(idle[i],(40,40)).convert_alpha()
    for i in range(len(prep)): prep[i]=pygame.transform.scale(prep[i],(40,40)).convert_alpha()
    for i in range(len(freefall)): freefall[i]=pygame.transform.scale(freefall[i],(40,40)).convert_alpha()
    
class Char(pygame.sprite.Sprite):
    def __init__(self,args :dict):

        # SELF-MADE CODE
        self.state = "enter"  # current behavior pattern for characters
        # always "enter" at the beginnning
        # behavior patterns: "enter" "idle" "attack" "return" "die"
        self.health = 1  # Health for characters.
        # Almost always 1.
        self.scorevalue = 15  # Score given to player
        self.RCM = False  # RCM = Return Condition Met.
        # This is only used in attack state.
        # This is to check if the character should return or not.
        self.offset = args['offset']  # offset that is used with the formation.
        # This never changes.
        self.formationPos = args['formation_position']  # position that the entire formation follows.

        self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[
            1])]  # current position, typically calculated with formationPos and offsets.
        # This is only not the case when you are in the attacking state.

        self.offScreen = False  # calculation to see if a character is visible onscreen
        # This is only used in attack state.

        # TIMERS
        self.animation_frame_counter = 0

        # STICKMAN-SPECIFIC CODE
        self.locked_in = False
        self.direction = None
        self.y_momentum = 0
        self.x_momentum = 0

        # PYGAME-SPECIFIC CODE
        pygame.sprite.Sprite.__init__(self)
        self.animation_frame = 0
        self.image = img.freefall[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.y = -100  # entrance state starting position
        self.groups = args['groups']
        self.player = args['player']

    def update(self):
        self.stateUpdate()
        # self.movementUpdate()
        self.collisionUpdate()
        # print(self.rect.center)
        # print(self.state)
        # print("-----")
        self.animUpdate()

    def animUpdate(self):
        # FRAME UPDATING
        self.animation_frame_counter += 1
        if self.animation_frame_counter >= 6:  # updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame += 1

            # IDLE IMAGE UPDATE
            if self.state == "idle":
                # RESETTING FRAME
                if self.animation_frame >= len(img.idle) - 1: self.animation_frame = 0
                # SETTING IMAGE
                self.image = img.idle[self.animation_frame]
            # ATTACKING IMAGE UPDATE
            elif self.state == "attack" or self.state == "enter":
                # RESETTING FRAME
                if self.animation_frame >= len(img.freefall) - 1: self.animation_frame = 0
                # SETTING IMAGE
                self.image = img.freefall[self.animation_frame]
                # FLIPPING IMAGE BASED ON DIRECTION
                if self.direction == "right": self.image = pygame.transform.flip(self.image, True, False)
            elif self.state == "prep":
                if self.animation_frame >= len(img.prep) - 1: self.animation_frame = 0 #this SHOULD NOT OCCUR since at this point he would have jumped
                self.image = img.prep[self.animation_frame]

        # if self.state == "enter":
        #     self.image = pygame.transform.scale(self.image, (20, 75))  # stretching image
        #     self.rect.x += 20  # centering image

    def stateUpdate(self):
        # except Exception as error:print(error)
        if self.state == "enter": self.state_enter()
        if self.state == "idle": self.state_idle()
        if self.state == "attack": self.state_attack()
        if self.state == "return": self.state_return()
        if self.state == "prep": self.state_prep()
        # print(self.state)

    def state_enter(self):
        # zooms down to the idle position
        # x will already match
        # starts at top

        # movement code
        self.rect.center = (self.idlePos[0], self.rect.center[1])  # matching x position
        if self.idlePos[1] > self.rect.center[1]:
            self.rect.y += 10
        elif self.idlePos[1] < self.rect.center[1]:
            self.rect.y -= 10
        if (30) > (self.idlePos[1] - self.rect.center[1]) > (-30):
            self.rect.center = self.idlePos
            self.state = "idle"
            # print("state is now idle")

    def state_idle(self):
        self.rect.center = self.idlePos

    #SPECIFIC TO STICKMAN CODE
    def state_prep(self):
        self.rect.center = self.idlePos
        #Creating variables to make the jump fine
        if self.animation_frame >= len(img.prep) - 2:
            self.animation_frame=0
            self.locked_in=True
            self.state="attack"
            #VISUAL EXPLOSION
            explosion=shared.dieBoom(self.rect.center,(50,50))
            self.groups["universal"].add(explosion)
        self.y_momentum=-5


    def state_attack(self):
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

    def state_return(self):pass

        # MOVING SIDE-TO-SIDE CODE

        # RETURN CONDITION MET CODE
        # self.rect.center=[(self.formationPos[0] + self.offset[0]),self.rect.center[1]]
        # self.rect.y+=10
        # if abs(self.rect.center[1]-(self.formationPos[1] + self.offset[1]))<5:self.state="idle"

    def state_die(self):
        pass

    # def movementUpdate(self): self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])];self.rect.center=self.idlePos
    def collisionUpdate(self):
        # please note that, with collision, there is no registration for touching YUP
        # this is because YUP handles collision with enemies herself
        # however, the enemies have to register how to collide with bullets
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

    def formationUpdate(self, formationPos):
        self.idlePos = [(self.formationPos[0] + self.offset[0]), (self.formationPos[1] + self.offset[1])]
        self.formationPos = formationPos

    def hitboxSwap(self):
        pass





