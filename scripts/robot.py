import pygame
import math
import numpy as np
from constants import *
from lidar import Lidar

class Robot(pygame.sprite.Sprite):
    
    def __init__(self, startpose, robotImg):
        pygame.sprite.Sprite.__init__(self)
        self.m2p = 3779.52
        self.x = startpose[0]
        self.y = startpose[1]
        self.theta = 0
        self.vel = 0.0 * self.m2p
        self.ver = 0.0 * self.m2p
        self.image = pygame.image.load(robotImg)
        self.width = self.image.get_width() / self.m2p
        self.mask = pygame.mask.from_surface(self.image)
        self.rotated = self.image
        self.rect = self.rotated.get_rect(center = (self.x, self.y))
        self.lidar = Lidar(position=(self.x, self.y))
        self.rays = []
        self.lasttime = 0
        self.lidarData = []
        self.rllv = 0
        self.rlav = 0

    def draw(self, map):
        map.map.blit(self.rotated, self.rect)

    def scan(self, map):
        self.lidarData, self.rays = self.lidar.scan(map, self.theta)
                
    def drawRays(self,map):
        for ray in self.rays:
            x0 = int(ray[0])
            y0 = int(ray[1])
            xt = int(ray[2])
            yt = int(ray[3])
            pygame.draw.line(map.map, self.lidar.color, (x0,y0), (xt,yt))

    def move(self, linear, angular, ICC):
        self.rllv = linear
        self.rlav = angular
        # dt = (pygame.time.get_ticks() - self.lasttime) / 1000
        dt = 0.1
        self.ver = ( (linear * self.m2p) + (angular *  ( (ICC * self.m2p) + (self.width/2))) )
        self.vel = ( (linear * self.m2p) + (angular *  ( (ICC * self.m2p) - (self.width/2))) )

        self.x += ((self.vel+self.ver)/2) * math.cos(self.theta) * dt
        self.y -= ((self.vel+self.ver)/2) * math.sin(self.theta) * dt
        self.theta += (self.ver - self.vel) / self.width * dt

        self.rotated = pygame.transform.rotozoom(self.image, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center = (self.x, self.y))

        self.lidar.setPosition(self.x, self.y)

        # self.lasttime = pygame.time.get_ticks()

    def setPose(self, X, Y, Theta):
        self.x = X
        self.y = Y
        self.theta = Theta
        self.rotated = pygame.transform.rotozoom(self.image, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center = (self.x, self.y))
        self.lidar.setPosition(self.x, self.y)

