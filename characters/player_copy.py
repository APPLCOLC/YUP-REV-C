import pygame
from bullets.shared import *





class Player(pygame.sprite.Sprite):
    #IMAGE LOADING
    idle,shoot,hurt,dead,celebrate=[],[],[],[],[]
    for i in range(3):
        idle.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+1)+".png"),(50,50)).convert_alpha())
        hurt.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+9)+".png"),(50,50)).convert_alpha())
        dead.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+12)+".png"),(50,50)).convert_alpha())
        celebrate.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+15)+".png"),(50,50)).convert_alpha())
    for i in range(5):
        shoot.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+4)+".png"),(50,50)).convert_alpha())
   
    health_HI = pygame.image.load("./assets/images/UI/LIVES/000.png")
    health_HI=pygame.transform.scale(health_HI,(25,25)).convert_alpha()
    health_MID = pygame.image.load("./assets/images/UI/LIVES/001.png")
    health_MID = pygame.transform.scale(health_MID, (25, 25)).convert_alpha()
    health_LO = pygame.image.load("./assets/images/UI/LIVES/002.png")
    health_LO = pygame.transform.scale(health_LO, (25, 25)).convert_alpha()

    #startup code
    def __init__(self, enemy_group, bullet_group, universal_group, sounds, loaded_bullets):
        #timers
        self.animation_frame = 0
        self.animation_frame_counter = 0
        self.state_timer = 0
        self.invincible_timer = 0

        #image
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image = Player.idle[0]
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
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
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.universal_group = universal_group

        #sound init
        self.sounds=sounds

        #UI elements
        self.lives = 3
        self.score = 0
        self.player_died = False
        self.invincible = False
        self.invincible_transparent=False
        self.animation_state = "idle"
        self.deathCoord = (0,0)

        #inventory elements
        self.inventory_index = 0
        self.shield_meter=100
        self.inventory = ["default","cheat"]
        self.current_weapon = self.inventory[self.inventory_index]
        self.loaded_bullets=loaded_bullets

    def update(self):
        if not self.player_died:
            self.state_manager()
            self.collision()
            if self.shoot_auto:self.autoshoot()
        self.animation()

    def state_manager(self):
        self.state_timer += 1
        if self.state_timer >= 30:
            self.state_timer = 0
            if self.animation_state == "hurt":
                self.animation_state = "idle"
            if self.animation_state == "shoot":
                self.animation_state = "idle"

        self.invincible_timer += 1
        if self.invincible_timer >= 180:
            self.invincible_timer = 0
            self.invincible = False
        
    def animation(self):
        self.animation_frame_counter += 1
        if not self.player_died:
            #idle frame counting
            if self.animation_state == "idle":
                #preventing out of bounds index
                if self.animation_frame > 2:
                    self.animation_frame = 0
                #changing the idle animation frame
                if self.animation_frame_counter >= 6:
                    self.animation_frame_counter = 0
                    self.animation_frame += 1
                    if self.animation_frame > 2:
                        self.animation_frame = 0
                self.image = Player.idle[self.animation_frame]
            #shoot animation counting
            if self.animation_state == "shoot":
                #preventing out of bounds index
                if self.animation_frame > 2:
                    self.animation_frame = 0
                if self.animation_frame_counter >= 6:
                    #changing shoot animation frame
                    self.animation_frame_counter = 0
                    self.animation_frame += 1
                    if self.animation_frame > 5:
                        self.animation_frame = 0
                self.image = Player.shoot[self.animation_frame]
            #hurt animation counting
            if self.animation_state == "hurt" or self.invincible:
                #preventing out of bounds index
                if self.animation_frame > 2:
                    self.animation_frame = 0
                if self.animation_frame_counter >= 1:
                    self.animation_frame_counter = 0
                    self.animation_frame += 1
                    if self.animation_frame > 2:
                        self.animation_frame = 0
                self.image = Player.hurt[self.animation_frame]
        else:
            #dead animation
            if self.animation_frame_counter >= 1:
                self.animation_frame_counter = 0
                self.animation_frame += 1
                if self.animation_frame > 2:
                    self.animation_frame = 0
            self.image = Player.dead[self.animation_frame]

        if self.invincible: self.invincible_transparent=~self.invincible_transparent
        elif not self.invincible or self.player_died: self.invincible_transparent = False
        else:self.invincible_transparent=False
        if self.invincible_transparent: self.image.set_alpha(50)
        else:self.image.set_alpha(255)

    def controls(self, event):

        #######YUP'S CONTROLS#######
        # Checks for all of the keys being pressed down on the keyboard.
        if event.type == pygame.KEYDOWN:
            # How movement works:
            # There are 2 variables that get set when a key is being pressed down: player_[direction] and moving_[direction].
            # For example, when the left key is pressed, player_x gets changed by -5 and moving_left becomes True
            if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                self.player_x = -5
                self.moving_left = True
            if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                self.player_x = 5
                self.moving_right = True
            if event.key == pygame.K_UP or event.key==pygame.K_w:
                self.player_y = -5
                self.moving_up = True
            if event.key == pygame.K_DOWN  or event.key==pygame.K_s:
                self.player_y = 5
                self.moving_down = True
            if event.key == pygame.K_n: self.shoot_auto = ~self.shoot_auto

            # Space simply creates a bullet, which gets placed where YUP is.
            if event.key == pygame.K_j and self.player_died == False:
                self.animation_state = "shoot"
                self.state_timer=0
                shoot(
                    loaded=self.loaded_bullets,
                    bullet_name=self.inventory[self.inventory_index],
                    coordinates=self.rect.center,
                    all_sprites=self.universal_group,
                    enemy_sprites=self.enemy_group,
                    bullet_sprites=self.bullet_group,
                )

        # This is the code that checks for a key being released.
        if event.type == pygame.KEYUP:
            # For all the key-releases for the arrow keys:
            # Moving_[direction] becomes marked as false.
            # Then, after being marked as false, it will then check and see if the opposite direction's key is being pressed.
            # If it is not, it will fully stop the character.
            if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                self.moving_left = False
                if self.moving_right is False:
                    self.player_x = 0
                else:
                    self.player_x = 6

            if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                self.moving_right = False
                if self.moving_left is False:
                    self.player_x = 0
                else:
                    self.player_x = -6

            if event.key == pygame.K_UP or event.key==pygame.K_w:
                self.moving_up = False
                if self.moving_down is False:
                    self.player_y = 0
                else:
                    self.player_y = 6

            if event.key == pygame.K_DOWN or event.key==pygame.K_s:
                self.moving_down = False
                if self.moving_up is False:
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
        if tempRect.left+self.player_x >= -10 and tempRect.right+self.player_x <= 460:
            self.rect.x += self.player_x
        elif tempRect.left <= 0:
            self.rect.left = -5
        elif tempRect.right >= 450:
            self.rect.right = 455
        if tempRect.top+self.player_y >= 290 and tempRect.bottom+self.player_y <= 610:
            self.rect.y += self.player_y
        elif tempRect.top <= 300:
            self.rect.top = 295
        elif tempRect.bottom >= 600:
            self.rect.bottom = 605

        # YUP COLLISION WITH ENEMIES
        #hitbox is needed for collision, so hitbox becomes rect\

        Hit = pygame.sprite.spritecollide(self, self.enemy_group, False, collided=pygame.sprite.collide_mask)
        if not self.invincible:
            for item in Hit:
                self.animation_state = "hurt"
                self.state_timer = 0
                self.animation_frame=0
                self.lives -= 1;self.invincible=True
                self.sounds.sounds["ouch.mp3"].play()
                try: item.health-=1
                except: pass
        if self.lives <= 0:
            self.animation_state = "dead"
            self.player_died = True
            self.sounds.sounds["death.mp3"].play()
            self.image.set_alpha(255)
            self.deathCoord = (self.rect.center)

    def bulletmanager(self,event):
        # print(self.invenIndex)
        try:
            self.current_weapon = self.inventory[self.inventory_index]
        except Exception as e:
            self.inventory_index = 0
            # print(e)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k and self.player_died == False:
                self.inventory_index += 1
                self.sounds.sounds["select.mp3"].play()
    def autoshoot(self):
        shoot(
            loaded=self.loaded_bullets,
            bullet_name=self.inventory[self.inventory_index],
            coordinates=self.rect.center,
            all_sprites=self.universal_group,
            enemy_sprites=self.enemy_group,
            bullet_sprites=self.bullet_group,
        )

    def reset_movement(self):
        self.moving_up = self.moving_down = self.moving_left = self.moving_right = False
        self.player_x = self.player_y = 0

   