#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
import pygame
import math
import numpy as np
from constants import *
from environment import Environment


if __name__ == "__main__":
    pygame.init()
    dims = (1800, 3200)
    running = True
    
    env = Environment(dims, '../images/map.png')
    env.addRobot((600,300), '../images/robot.png')
    env.addRobot((200,300), '../images/robot.png')
    env.addRobot((1500,300), '../images/robot.png')
    
    vels = [(0.01, -0.01), (0.07, 0.07), (0,0)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.step(vels)

        
