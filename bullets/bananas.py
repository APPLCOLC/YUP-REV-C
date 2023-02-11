import pygame
from bullets import shared


#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(shared.Bullet):
    image = pygame.transform.scale(pygame.image.load("./assets/images/bullets/bananas.png"),(100,25)).convert_alpha()

    def __init__(self, args:dict={"center":(0,0)}):
        shared.Bullet.__init__(self, args, sound_play=False)
        self.rect = pygame.mask.from_surface(Bullet.image).get_rect()
        self.rect.center=args["center"]
        args["sounds"].sounds["bananas.mp3"].play()
