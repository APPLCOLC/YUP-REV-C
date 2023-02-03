import pygame,random
# from modules.sounds import *
#from main import *

def shoot(loaded,bullet_name,coordinates,all_sprites,enemy_sprites,bullet_sprites):
    args={
        "center":coordinates,
        "enemy_sprites":enemy_sprites,
        "all_sprites":all_sprites,
        "bullet_sprites":bullet_sprites
    }
    if len(bullet_sprites)<2:
        bullet=loaded[bullet_name].Bullet(args=args)
        all_sprites.add(bullet)
        bullet_sprites.add(bullet)
        

def display_bullet(WIN,positionTuple,bullettype,loaded):
    pass
    # WIN.blit(pygame.transform.scale(loaded[bullettype].image,(25,25)),positionTuple)


class Bullet(pygame.sprite.Sprite):
    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(image, "black", (5, 5), 5)
    pygame.draw.circle(image, "white", (5, 5), 4)
    screen_rect = pygame.Rect(0, 0, 450, 600)

    def __init__(self, sound=None, img=None, args={"center": (0, 0)}):

        pygame.sprite.Sprite.__init__(self)
        self.health = 1

        if sound is not None:
            sound.play()

        self.rect = pygame.mask.from_surface(Bullet.image).get_rect()
        # This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        # These are, typically, fed with YUP's coordinates.
        self.rect.center = args["center"]

    def update(self):
        # Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 15
        if not self.on_screen() or self.health <= 0: self.kill()

    def on_screen(self) -> bool:
        return Bullet.screen_rect.colliderect(self.rect)


