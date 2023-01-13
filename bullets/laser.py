import pygame

img = pygame.image.load("./assets/images/bullets/laser.png")
#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, sound=None, img=img, args={"center":(0,0),"direction":0}):
        # shoot_laser.play()
        pygame.sprite.Sprite.__init__(self)
        self.health = 15
        self.image = pygame.Surface((30,100))
        self.image = img
        self.image = pygame.transform.scale(self.image, (30, 100))

        if sound is not None:
            sound.play()

        self.rect = self.image.get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = args["center"]

    def update(self):
    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 50
        if self.rect.bottom <= 0:
            self.kill()
        if self.health <= 0:
            self.kill()
