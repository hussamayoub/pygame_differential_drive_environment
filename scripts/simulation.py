#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
import pygame
import math
import numpy as np
from constants import *
from environment import Environment
import time

robotImage = '../images/robot.png'
metersToPixels = 3779.52
robotwidthPixels = 50
robotWidth = robotwidthPixels / metersToPixels
R = robotWidth

def Position(x, y):
    xOffset = 960
    yOffset = 540
    return (x + xOffset, y + yOffset)

def InitEnv():
    pygame.init()
    dims = (1080, 1920)
    env = Environment(dims, '../images/map.png')
    return env

def FourRobotsEnv():
    env = InitEnv()

    env.addRobot(Position(50,50), robotImage)
    env.addRobot(Position(-50,50), robotImage)
    env.addRobot(Position(-50,-50), robotImage)
    env.addRobot(Position(50,-50), robotImage)

    running = True
    return running, env

def Circle(Radius):
    xOffset = 960
    yOffset = 540
    angle = 0.0
    """
    x   cos(θ) -sin(θ)  dX x
    y   sin(θ) cos(θ)   dY y
    1   0      0        1  1 
    """
    Poses = []
    array = np.arange(0.0, 6.28, 0.03)
    increment = (math.pi * 2)/len(array)
    for index in array:
        angle += increment

        a = np.array([[math.cos(index), -math.sin(index), math.cos(angle)*Radius],
                      [math.sin(index), math.cos(index), math.sin(angle)*Radius],
                      [0,0,1]])
        b1 = np.array([50,50,1])
        b2 = np.array([-50,50,1])
        b3 = np.array([-50,-50,1])
        b4 = np.array([50,-50,1])
        dot1 = a.dot(b1)
        dot2 = a.dot(b2)
        dot3 = a.dot(b3)
        dot4 = a.dot(b4)

        Poses.append((([dot1[0] + xOffset,dot1[1] + yOffset, index]), ([dot2[0] + xOffset,dot2[1] + yOffset, index]),
                    ([dot3[0] + xOffset,dot3[1] + yOffset, index]), ([dot4[0] + xOffset,dot4[1] + yOffset, index])))
    for index, Pose in enumerate(Poses):
        for i, robotPose in enumerate(Pose):
            try:
                yy = ( Poses[index+1][i][1] - robotPose[1] )
                xx = ( Poses[index+1][i][0] - robotPose[0] )
            except:
                alpha = alpha
            alpha = -math.atan(yy/xx)
                
            if yy < 0 and xx < 0:
                alpha += math.pi
            if yy > 0 and xx < 0:
                alpha -= math.pi

            robotPose[2] = alpha
    return Poses



if __name__ == "__main__":
    r = 0
    
    running, env = FourRobotsEnv()    
    
    while running:
        Poses = Circle(r)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in Poses:
            env.setManualPose(i)
        r += 50
        if r == 400:
            running = False


        
