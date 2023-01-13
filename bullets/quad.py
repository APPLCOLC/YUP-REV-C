import pygame



img = (
    pygame.image.load("./assets/images/bullets/quadLeft.png").convert_alpha(),
    pygame.image.load("./assets/images/bullets/quadRight.png").convert_alpha(),
    pygame.image.load("./assets/images/bullets/quadUp.png").convert_alpha(),
    pygame.image.load("./assets/images/bullets/quadDown.png").convert_alpha()
    )

b = pygame.image.load("./assets/images/bullets/quadFull.png").convert_alpha()

#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, sound=None, img=img, args={"center":(0,0),"direction":0}):
        pygame.sprite.Sprite.__init__(self)
        self.direction = args["direction"]
        self.health = 1

        self.image = img[self.direction]
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.center = args["center"]

        if sound is not None: sound.play()

    def update(self):
        if self.direction == 0: self.rect.x -= 25
        if self.direction == 1: self.rect.x += 25
        if self.direction == 2: self.rect.y -= 25
        if self.direction == 3: self.rect.y += 25

        if self.direction == 0 and self.rect.right <= 0: self.kill()
        if self.direction == 1 and self.rect.left >= 600: self.kill()
        if self.direction == 2 and self.rect.top <= 0: self.kill()
        if self.direction == 3 and self.rect.bottom >= 800: self.kill()

        if self.health <= 0:
            self.kill()