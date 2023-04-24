import pygame
import math
import numpy as np
from constants import *
from robot import Robot

class Environment:
    def __init__(self, dimentions, mapImg):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.yellow = (255,255,0)
        self.height = dimentions[0]
        self.width = dimentions[1]
        pygame.display.set_caption("env")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.mapImg = pygame.image.load(mapImg)
        self.maprect = self.mapImg.get_rect()
        self.map.blit(self.mapImg, self.maprect)
        self.robots = []

    def addRobot(self, position, imagePath):
        self.robots.append(Robot(position, imagePath))

    def refresh(self):
        self.map.blit(self.mapImg, self.maprect)
        for robot in self.robots:
            robot.draw(self)
        for robot in self.robots:
            robot.scan(self)
        for robot in self.robots:
            robot.drawRays(self)

    def step(self, velocitiesArray):
        counter = 0
        for robot in self.robots:
            robot.move(velocitiesArray[counter][0], velocitiesArray[counter][1])
            counter += 1
        pygame.display.update()
        self.refresh()