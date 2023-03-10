import pygame
from bullets.shared import *
import characters.shared as shared

class Player(pygame.sprite.Sprite):
    #IMAGE LOADING
    idle,shoot,land,hurt,dead,celebrate=[],[],[],[],[],[]
    for i in range(3):
        idle.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+1)+".png"),(50,50)).convert_alpha())
        land.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+4)+".png"),(50,50)).convert_alpha())
        shoot.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+7)+".png"),(50,50)).convert_alpha())
        hurt.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+10)+".png"),(50,50)).convert_alpha())
        dead.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+13)+".png"),(50,50)).convert_alpha())
        celebrate.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/YUP/YUP_-"+str(i+16)+".png"),(50,50)).convert_alpha())

    health = (
                 pygame.transform.scale(pygame.image.load("./assets/images/UI/LIVES/002.png"), (25, 25)).convert_alpha(),
                 pygame.transform.scale(pygame.image.load("./assets/images/UI/LIVES/001.png"), (25, 25)).convert_alpha(),
                 pygame.transform.scale(pygame.image.load("./assets/images/UI/LIVES/000.png"),(25,25)).convert_alpha()
    )

    def __init__(self,sounds,loaded_bullets,groups={}):
        pygame.sprite.Sprite.__init__(self)

        #timers
        self.animation_frame = self.animation_frame_counter = self.state_timer = self.invincible_timer = 0

        #image rendering
        self.image = Player.idle[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.rect.center = (225,500)

        #argument values
        self.sounds = sounds
        self.groups = groups

        #movement declarations
        self.moving = [False,False,False,False] #left, right, up, down
        self.speed = 0 #just x value. cannot move vertically
        self.jump_frames = 0

        #general values
        self.score = 0
        self.health = 3
        self.state = "idle"
        self.groups = groups
        self.loaded_bullets = loaded_bullets

        #inventory
        """the bullet counts as everything, including the shield.
        Instead of checking for a separate value, it just checks if bullet is anything but "default"
        It uses this for hit detection, and all that jazz."""
        self.bullet = "default" #can be changed for power-ups, temporarily

    
    def update(self):
        self.collision()
        self.animation_update()


    def animation_update(self):
        self.animation_frame_counter += 1
        if self.animation_frame_counter >= 3:
            self.animation_frame += 1
            self.animation_frame_counter = 0
            self.change_image()

    def change_image(self):
        # all animations are formatted as [resetting frame] ; [setting image], so i'm not commenting anything
        if self.state == "idle":
            if self.animation_frame > (len(Player.idle) - 1): self.animation_frame = 0; return
            self.image = Player.idle[self.animation_frame]
        if self.state == "land":
            if self.animation_frame > (len(Player.land) - 1):
                self.animation_frame = 0
                self.animation_change("idle")  # resetting frame here since no loop
                return
            self.image = Player.land[self.animation_frame]
        if self.state == "shoot":
            if self.animation_frame > (len(Player.shoot) - 1):
                self.animation_frame = 0
                self.animation_change("idle")  # resetting frame here since no loop
                return
            self.image = Player.shoot[self.animation_frame]
        if self.state == "hurt" or self.invincible_timer > 0:
            if self.animation_frame > (len(Player.hurt) - 1):
                self.animation_frame = 0
                self.animation_change("idle")  # resetting frame here since no loop
                return
            self.image = Player.hurt[self.animation_frame]


    def animation_change(self,name):
        # print(name)
        self.state = name
        self.animation_frame = self.animation_frame_counter = 0
        self.change_image() #forcing an image display since it usually hides the first image if this isn't done


    def controls(self,event):
        #moving characters left and right ; detecting button presses
        if event.type == pygame.KEYDOWN:

            #moving left
            if event.key == pygame.K_a:
                self.speed = -5
                self.moving[0] = True

            #moving right
            if event.key == pygame.K_d:
                self.speed = 5
                self.moving[1] = True

            #jumping up
            if event.key == pygame.K_w:
                #only jumps if not jumping down or already jumping up
                if not self.moving[3] and not self.moving[2]:
                    self.moving[2] = True
                    self.jump_frames = 0
                elif self.moving[3]:
                    self.jump_frames = 60
            
            #jumping down
            if event.key == pygame.K_s:
                #only jumps if not jumping up or already jumping down
                if not self.moving[2] and not self.moving[3]:
                    self.moving[3] = True
                    self.jump_frames = 0
                elif self.moving[2]:
                    self.jump_frames = 60

            #shooting
            if event.key == pygame.K_j or event.key == pygame.K_SPACE:
                #change animation
                if len(self.groups["bullet"])<2:self.animation_change("shoot")
                shoot(
                    loaded = self.loaded_bullets,
                    bullet_name = self.bullet,
                    coordinates = self. rect.center,
                    all_sprites = self.groups["universal"],
                    enemy_sprites = self.groups["enemy"],
                    bullet_sprites = self.groups["bullet"],
                    sounds = self.sounds,
                )

        #checking key lifting to stop movement 
        if event.type == pygame.KEYUP:
            #left
            if event.key == pygame.K_a:
                self.moving[0] = False 
                #checking opposite direction movement for exception
                self.speed = 6 if self.moving[1] else 0
            #right
            if event.key == pygame.K_d:
                self.moving[1] = False 
                #checking opposite direction movement for exception
                self.speed = -6 if self.moving[0] else 0


    def collision(self):
        #making sure character will stay in borders when moving
        if self.rect.left + self.speed > 0 and self.rect.right + self.speed < 450:
            self.rect.x += self.speed

        #collision with enemies -- only if not invincible 
        if self.invincible_timer == 0:
            for item in pygame.sprite.spritecollide(self,self.groups["enemy"], False, collided = pygame.sprite.collide_mask):
                
                """SHEDDING OFF SHIELD IF ONE IS EQUIPPED"""
                if self.bullet != "default":
                    self.bullet = "default"
                    self.groups["universal"].add(shared.dieBoom(self.rect.center,(50,50)))
                    
                else: 
                    """IF NO SHIELD IS EQUIPPED""" 
                    self.health = self.health - 1 if self.health > 0 else self.health

                try: item.health -= 1
                except AttributeError:pass
                self.invincible_timer = 120
                self.sounds.sounds["ouch.mp3"].play()
                # change animation
                self.animation_change("hurt")
                break #preventing multiple hits

        #kill code
        if self.health <= 0:
            self.state = "dead"
            self.sounds.sounds["death.mp3"].play()
            self.groups["universal"].add(shared.dieBoom(self.rect.center,(50,50)))
            # self.health = 3
            self.kill()

        #invincible timer 
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        #updating jump frames
        if self.moving[2] or self.moving[3]:
            #ending the jump
            if self.jump_frames >= 60: 
                self.jump_frames = 0
                #setting both to false in order to prevent duplicate jumping
                self.moving[2] = self.moving[3] = False
                #resetting position
                self.rect.center = (self.rect.center[0],500)
                #making bounce animation
                self.animation_change("land")
            #updating jump frames for parabola code
            self.jump_frames += 1
        
        #jump up animation
        if self.moving[2]:
            self.rect.center = (
                self.rect.center[0],
                (1/9)*(((self.jump_frames)-30)**2) + 400
            )
        #jump up animation
        elif self.moving[3]:
            self.rect.center = (
                self.rect.center[0],
                (1/-18)*(((self.jump_frames)-30)**2) + 550
            )
            

    def reset_movement(self):
        #movement declarations
        self.moving = [False,False,self.moving[2],self.moving[3]] #left, right, up, down
        self.speed = 0


    def display_health(self,WIN,location_y=0):
        #displaying health code
        for i in range(self.health):
            val = 2 if i > 2 else i
            WIN.blit(Player.health[val],(
                (i*25)-((i//10)*250),
                ((i//10)*25) + location_y
                ))
        if self.bullet != "default":
            WIN.blit(
                pygame.transform.scale(self.loaded_bullets[self.bullet].Bullet.image,(25,25)).convert_alpha(),
                (((i*25)+25),
                location_y)
            )
