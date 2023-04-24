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
    env.addRobot((200,200), '../images/robot.png')
    env.addRobot((350,350), '../images/robot.png')
    
    vels = [(0.1, -0.1), (0.2, 0.2)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.step(vels)

        
