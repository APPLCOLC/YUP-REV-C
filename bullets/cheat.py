import pygame,random


#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(pygame.sprite.Sprite):
    img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(img, "red", (0, 0), 30)
    screen_rect = pygame.Rect(0, 0, 450, 600)
    def __init__(self, sound=None, img=img, args={"center":(0,0),"direction":0, "enemy_sprites":None}):
        pygame.sprite.Sprite.__init__(self)


        if sound is not None: sound.play()
        # sounds.shoot_missile.play()

        self.enemyClass = args["enemy_sprites"]

        #this shit just picks a random character to touch and touches it :)

        if self.enemyClass != None and len(self.enemyClass) > 0:
            self.lockIndex = random.randint(0,(len(list(self.enemyClass))-1))
            self.lockChar = list(self.enemyClass)[self.lockIndex]
        else:self.kill() 
       
        self.health = 1

        self.image = pygame.transform.scale(img,(75,75))
        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        try:self.rect.center = self.lockChar.rect.center
        except:self.kill()

    def update(self):
        if self.health<=0:self.kill()
        self.kill()