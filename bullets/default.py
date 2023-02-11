import pygame
from bullets import shared

class Bullet(shared.Bullet):
    def __init__(self, args={"center": (0, 0)}):
        shared.Bullet.__init__(self,args=args)