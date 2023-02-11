import pygame
from bullets import shared

class Bullet(shared.Bullet):
    image = pygame.transform.scale(pygame.image.load('./assets/images/bullets/strawberry.png'),(10,20)).convert_alpha()
    def __init__(self,args={"center": (0, 0)}):
        shared.Bullet.__init__(self, args=args)
        self.rect = pygame.mask.from_surface(Bullet.image).get_rect()
        self.rect.center = args['center']
    def update(self):
        # Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 45
        if not self.on_screen() or self.health <= 0: self.kill()