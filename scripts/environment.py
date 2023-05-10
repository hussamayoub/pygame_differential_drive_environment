import pygame
import math
import numpy as np
from constants import *
from robot import Robot

class Environment(pygame.sprite.Sprite):
    def __init__(self, dimentions, mapImg):
        pygame.sprite.Sprite.__init__(self)
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

        self.image = pygame.image.load(mapImg)
        self.rect = self.image.get_rect()


        self.mask_image = self.image.convert()
        self.mask_image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.mask_image)
        self.mask.invert()

        self.map.blit(self.image, self.rect)
        self.robots = []

    def addRobot(self, position, imagePath):
        self.robots.append(Robot(position, imagePath))

    def refresh(self):
        self.map.blit(self.image, self.rect)
        for robot in self.robots:
            robot.draw(self)
        for robot in self.robots:
            robot.scan(self)
        for robot in self.robots:
            robot.drawRays(self)

        ## Lines
            pygame.draw.line(self.map, self.red, (self.robots[0].x,self.robots[0].y), (self.robots[1].x,self.robots[1].y))
            pygame.draw.line(self.map, self.red, (self.robots[1].x,self.robots[1].y), (self.robots[2].x,self.robots[2].y))
            pygame.draw.line(self.map, self.red, (self.robots[2].x,self.robots[2].y), (self.robots[3].x,self.robots[3].y))
            pygame.draw.line(self.map, self.red, (self.robots[0].x,self.robots[0].y), (self.robots[3].x,self.robots[3].y))





    def checkCollision(self):
        collisionrects = []
        index = 0
        for idx, robot in enumerate(self.robots):
            collisionrects.append(robot.rect.inflate(100,100))
            if self.mask.overlap(robot.mask, (robot.x, robot.y)):
                return True

        for i in range(len(collisionrects)):
            for j in range(i+1, len(collisionrects)):
                if collisionrects[i].colliderect(collisionrects[j]):
                    pass
                    return True
        return False      

    def step(self, velocitiesArray):
        counter = 0
        for robot in self.robots:
            robot.move(velocitiesArray[counter][0], velocitiesArray[counter][1], velocitiesArray[counter][2])
            counter += 1
        terminating = self.checkCollision()
        pygame.display.update()
        self.refresh()
        return terminating
    
    def setManualPose(self, pose):
        counter = 0
        for robot in self.robots:
            try:
                robot.setPose(pose[counter][0], pose[counter][1], pose[counter][2])
            except:
                pass
            counter += 1
        pygame.display.update()
        self.refresh()