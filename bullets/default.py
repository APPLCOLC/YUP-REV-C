import pygame
from bullets import shared

class Bullet(shared.Bullet):
    def __init__(self, sound=None, img=None, args={"center": (0, 0)}):
        shared.Bullet.__init__(self, sound=sound, img=img, args=args)