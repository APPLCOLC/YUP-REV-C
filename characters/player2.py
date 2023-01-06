import pygame,time
from modules.bullets import *


class YUPANIMATIONS():
    idle1 = pygame.image.load("./assets/images/characters/YUP/YUP_-1.png")
    idle2 = pygame.image.load("./assets/images/characters/YUP/YUP_-2.png")
    idle3 = pygame.image.load("./assets/images/characters/YUP/YUP_-3.png")
    idle = [idle1,idle2,idle3]
    del idle1,idle2,idle3
    for i in range(len(idle)): idle[i] = pygame.transform.scale(idle[i],(50,50)).convert_alpha()

    shoot1 = pygame.image.load("./assets/images/characters/YUP/YUP_-4.png")
    shoot2 = pygame.image.load("./assets/images/characters/YUP/YUP_-5.png")
    shoot3 = pygame.image.load("./assets/images/characters/YUP/YUP_-6.png")
    shoot4 = pygame.image.load("./assets/images/characters/YUP/YUP_-7.png")
    shoot5 = pygame.image.load("./assets/images/characters/YUP/YUP_-8.png")
    shoot = [shoot1,shoot2,shoot3,shoot4,shoot5]
    del shoot1,shoot2,shoot3,shoot4,shoot5
    for i in range(len(shoot)): shoot[i] = pygame.transform.scale(shoot[i],(50,50)).convert_alpha()

    hurt1 = pygame.image.load("./assets/images/characters/YUP/YUP_-9.png")
    hurt2 = pygame.image.load("./assets/images/characters/YUP/YUP_-10.png")
    hurt3 = pygame.image.load("./assets/images/characters/YUP/YUP_-11.png")
    hurt = [hurt1,hurt2,hurt3]
    del hurt1,hurt2,hurt3
    for i in range(len(hurt)): hurt[i] = pygame.transform.scale(hurt[i],(50,50)).convert_alpha()

    dead1 = pygame.image.load("./assets/images/characters/YUP/YUP_-12.png")
    dead2 = pygame.image.load("./assets/images/characters/YUP/YUP_-13.png")
    dead3 = pygame.image.load("./assets/images/characters/YUP/YUP_-14.png")
    dead = [dead1,dead2,dead3]
    del dead1,dead2,dead3
    for i in range(len(dead)): dead[i] = pygame.transform.scale(dead[i],(50,50)).convert_alpha()

    celebrate1 = pygame.image.load("./assets/images/characters/YUP/YUP_-15.png")
    celebrate2 = pygame.image.load("./assets/images/characters/YUP/YUP_-16.png")
    celebrate3 = pygame.image.load("./assets/images/characters/YUP/YUP_-17.png")
    celebrate = [celebrate1,celebrate2,celebrate3]
    del celebrate1,celebrate2,celebrate3
    for i in range(len(celebrate)): celebrate[i] = pygame.transform.scale(celebrate[i],(50,50)).convert_alpha()

    health_HI = pygame.image.load("./assets/images/UI/LIVES/000.png")
    health_HI=pygame.transform.scale(health_HI,(25,25)).convert_alpha()
    health_MID = pygame.image.load("./assets/images/UI/LIVES/001.png")
    health_MID = pygame.transform.scale(health_MID, (25, 25)).convert_alpha()
    health_LO = pygame.image.load("./assets/images/UI/LIVES/002.png")
    health_LO = pygame.transform.scale(health_LO, (25, 25)).convert_alpha()



class Player(pygame.sprite.Sprite):
    # Player, of course, is the main character that you control and play as.
    def __init__(self, HurtSprites ,bulletsprites,allsprites,sounds):
        self.frame = 0
        self.animStart = time.time()
        self.stateStart = time.time()
        self.iStart = time.time()

        # All of the .image code has to do with the image that the character is using.
        # This will change later on depending on the frame of the spritesheet. This is just a placeholder.
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image = YUPANIMATIONS.idle[0]
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)

        # self.rect.
        self.rect.center = (300, 500)

        #movement code
        self.moving_left = False  # Checks if the left key is being held down or released
        self.moving_right = False  # Checks if the right key is being held down or released
        self.moving_up = False  # Checks if the up key is being held down or released
        self.moving_down = False  # Checks if the down key is being held down or released
        self.player_x = 0  # A value that is set if the left or right key is being pressed. It determines how much the character moves.
        self.player_y = 0  # A value that is set if the up or down key is being pressed. It determines how much the character moves.
        self.velocity = 10  # The value that player_x or player_y is set to when an arrow key is being pressed.
        self.shoot_auto = False

        #code for registering the many sprite classes
        self.HurtSprites = HurtSprites
        self.bulletsprites = bulletsprites
        self.allsprites = allsprites

        #sound init
        self.sounds=sounds

        #UI elements
        self.lives = 3
        self.score = 0
        self.playerdied = False
        self.invincible = False
        self.invenTrans=False
        self.animState = "idle"
        self.deathCoord = (0,0)

        #inventory elements
        self.invenIndex = 0
        self.shield_meter=100
        self.inventory = ["default","quad","laser"]
        self.currentweapon = self.inventory[self.invenIndex]

    def update(self):
        if not self.playerdied:
            self.stateManager()
            self.collision()
            if self.shoot_auto:self.autoshoot()
        self.animation()

    def stateManager(self):
        animStateEnd = time.time()
        if animStateEnd - self.stateStart >= 0.5:
            self.stateStart = time.time()
            if self.animState == "hurt":self.animState = "idle"
            if self.animState == "shoot":self.animState = "idle"
        iStateEnd=time.time()
        if iStateEnd-self.iStart >= 2.5: self.iStart=time.time();self.invincible = False
        
    def animation(self):
        animEnd = time.time()
        if not self.playerdied:
            if self.animState == "idle":
                if self.frame > 2:
                    self.frame = 0
                if animEnd - self.animStart >= 0.1:
                    self.animStart = time.time()
                    self.frame += 1
                    if self.frame > 2:
                        self.frame = 0
                self.image = YUPANIMATIONS.idle[self.frame]
            if self.animState == "shoot":
                if self.frame > 2:
                    self.frame = 0
                if animEnd - self.animStart >= 0.1:
                    self.animStart = time.time()
                    self.frame += 1
                    if self.frame > 5:
                        self.frame = 0
                self.image = YUPANIMATIONS.shoot[self.frame]
            if self.animState == "hurt" or self.invincible:
                if self.frame > 2:
                    self.frame = 0
                if animEnd - self.animStart >= 0.05:
                    self.animStart = time.time()
                    self.frame += 1
                    if self.frame > 2:
                        self.frame = 0
                self.image = YUPANIMATIONS.hurt[self.frame]
        else:
            if animEnd - self.animStart >= 0.05:
                self.animStart = time.time()
                self.frame += 1
                if self.frame > 2:
                    self.frame = 0
            self.image = YUPANIMATIONS.dead[self.frame]

        if self.invincible: self.invenTrans=~self.invenTrans
        elif not self.invincible or self.playerdied: self.invenTrans = False
        else:self.invenTrans=False
        if self.invenTrans: self.image.set_alpha(50)
        else:self.image.set_alpha(255)

    def controls(self, event):

        #######YUP'S CONTROLS#######
        # Checks for all of the keys being pressed down on the keyboard.
        if event.type == pygame.KEYDOWN:
            # How movement works:
            # There are 2 variables that get set when a key is being pressed down: player_[direction] and moving_[direction].
            # For example, when the left key is pressed, player_x gets changed by -5 and moving_left becomes True
            if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                self.player_x = -6
                self.moving_left = True
            if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                self.player_x = 6
                self.moving_right = True
            if event.key == pygame.K_UP or event.key==pygame.K_w:
                self.player_y = -6
                self.moving_up = True
            if event.key == pygame.K_DOWN  or event.key==pygame.K_s:
                self.player_y = 6
                self.moving_down = True
            if event.key == pygame.K_n: self.shoot_auto = ~self.shoot_auto

            # Space simply creates a bullet, which gets placed where YUP is.
            if event.key == pygame.K_j and self.playerdied == False:
                self.animState = "shoot";self.stateStart=time.time()
                shoot(self.rect.center[0], self.rect.center[1], self.allsprites, self.bulletsprites, self.HurtSprites,self.sounds,bullettype=self.currentweapon)

        # This is the code that checks for a key being released.
        if event.type == pygame.KEYUP:
            # For all of the key-releases for the arrow keys:
            # Moving_[direction] becomes marked as false.
            # Then, after being marked as false, it will then check and see if the opposite direction's key is being pressed.
            # If it is not, it will fully stop the character.
            if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                self.moving_left = False
                if self.moving_right == False:
                    self.player_x = 0
                else:
                    self.player_x = 6

            if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                self.moving_right = False
                if self.moving_left == False:
                    self.player_x = 0
                else:
                    self.player_x = -6

            if event.key == pygame.K_UP or event.key==pygame.K_w:
                self.moving_up = False
                if self.moving_down == False:
                    self.player_y = 0
                else:
                    self.player_y = 6

            if event.key == pygame.K_DOWN or event.key==pygame.K_s:
                self.moving_down = False
                if self.moving_up == False:
                    self.player_y = 0
                else:
                    self.player_y = -6

        #This is the inventory manager code
        self.bulletmanager(event)
        #########################
    def collision(self):
        
        tempRect=self.mask.get_rect()
        tempRect.center=self.rect.center
        # YUP COLLISION WITH WALLS
        #self.rect is not used here, since both are being compared through non-pygame means.
        if tempRect.left+self.player_x >= 0 and tempRect.right+self.player_x <= 450:
            self.rect.x += self.player_x
        elif tempRect.left <= 0:
            self.rect.left = 5
        elif tempRect.right >= 450:
            self.rect.right = 445
        if tempRect.top+self.player_y >= 0 and tempRect.bottom+self.player_y <= 600:
            self.rect.y += self.player_y
        elif tempRect.top <= 0:
            self.rect.top = 5
        elif tempRect.bottom >= 600:
            self.rect.bottom = 595

        # YUP COLLISION WITH ENEMIES
        #hitbox is needed for collision, so hitbox becomes rect\

        Hit = pygame.sprite.spritecollide(self, self.HurtSprites, False, collided=pygame.sprite.collide_mask)
        if not self.invincible:
            for item in Hit:
                self.animState = "hurt";self.stateStart=time.time();self.frame=0
                self.lives -= 1;self.invincible=True
                self.sounds.ouch.play()
                try: item.health-=1
                except: pass
        if self.lives <= 0:
            self.animState = "dead"
            self.playerdied = True
            self.sounds.death.play()
            self.image.set_alpha(255)
            self.deathCoord = (self.rect.center)

    def bulletmanager(self,event):
        # print(self.invenIndex)
        try:
            self.currentweapon = self.inventory[self.invenIndex]
        except Exception as e:
            self.invenIndex = 0
            # print(e)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k and self.playerdied == False:
                self.invenIndex += 1
                self.sounds.select.play()
    def autoshoot(self):
        shoot(self.rect.center[0], self.rect.center[1], self.allsprites, self.bulletsprites, self.HurtSprites, self.sounds, self.inventory[self.invenIndex])

    # This is the code loaded as a temporary save whenever you exit states.
    # This takes your inventory, your health, your coodinates, etc.
    def pack_data(self):
        data = {"lives": self.lives, "inventory": self.inventory, "inventory index": self.invenIndex,
                "score": self.score, "coord": (self.rect.x, self.rect.y)}
        return data
    def reset_movement(self):
        self.moving_up = self.moving_down = self.moving_left = self.moving_right = False
        self.player_x = self.player_y = 0
    def load_data(self,dataDict):
        self.inventory = dataDict["inventory"]
        self.invenIndex = dataDict["inventory index"]
        self.lives = dataDict["lives"]
        self.score = dataDict["score"]
        self.rect.x = dataDict["coord"][0]
        self.rect.y = dataDict["coord"][1]
    #UI elements
    def display_health(self,WIN,location):
        if self.lives <= 1: WIN.blit(YUPANIMATIONS.health_LO,location)
        if self.lives == 2: WIN.blit(YUPANIMATIONS.health_MID,location)
        if self.lives >= 3: WIN.blit(YUPANIMATIONS.health_HI,location)
   