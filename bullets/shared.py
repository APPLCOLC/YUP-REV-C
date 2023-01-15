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

    # elif bullettype == "missile":
    #         bullet = Missile(playerx,playery,sounds,enemyClass=HurtSprites)
    #         allsprites.add(bullet)
    #         bulletsprites.add(bullet)
        

def display_bullet(WIN,positionTuple,bullettype,loaded):
    WIN.blit(pygame.transform.scale(loaded[bullettype].img,(25,25)),positionTuple)





