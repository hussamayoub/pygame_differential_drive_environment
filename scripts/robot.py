import pygame
import math
import numpy as np
from constants import *
from lidar import Lidar

class Robot:
    def __init__(self, startpose, robotImg):
        self.m2p = 3779.52
        self.x = startpose[0]
        self.y = startpose[1]
        self.theta = 0
        self.vel = 0.01 * self.m2p
        self.ver = 0.01 * self.m2p
        self.img = pygame.image.load(robotImg)
        self.width = self.img.get_width()

        self.rotated = self.img
        self.rect = self.rotated.get_rect(center = (self.x, self.y))
        self.lidar = Lidar(position=(self.x, self.y))
        self.rays = []
        self.lasttime = 0

    def draw(self, map):
        map.map.blit(self.rotated, self.rect)

    def scan(self, map):
        data, self.rays = self.lidar.scan(map)

    def drawRays(self,map):
        for ray in self.rays:
            x0 = int(ray[0])
            y0 = int(ray[1])
            xt = int(ray[2])
            yt = int(ray[3])
            pygame.draw.line(map.map, self.lidar.color, (x0,y0), (xt,yt))

    def move(self, ver, vel):
        dt = (pygame.time.get_ticks() - self.lasttime) / 1000
        self.vel = vel * self.m2p
        self.ver = ver * self.m2p
        self.x += ((self.vel+self.ver)/2) * math.cos(self.theta) * dt
        self.y -= ((self.vel+self.ver)/2) * math.sin(self.theta) * dt
        self.theta += (self.ver - self.vel) / self.width * dt
        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center = (self.x, self.y))
        self.lidar.setPosition(self.x, self.y)
        self.lasttime = pygame.time.get_ticks()
