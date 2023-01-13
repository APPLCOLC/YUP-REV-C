import pygame

#ARGUMENT PSEUDOCODE
#self, sounds, img, args={}
#args are a dictionary so multiple arguments can be provided but only some need to be utilized

img = pygame.image.load("./assets/images/bullets/bullet.png")
#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, sound=None, img=img, args={"center":(0,0)}):
        # shoot_bap[random.randint(0,3)].play()

        pygame.sprite.Sprite.__init__(self)
        self.health = 1
        self.image = img
        self.image = pygame.transform.scale(self.image, (20, 20))

        if sound is not None:
            sound.play()

        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = args["center"]

    def update(self):
    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 25
        if self.rect.top <= 0:
            self.kill()
        if self.health <= 0:
            self.kill()