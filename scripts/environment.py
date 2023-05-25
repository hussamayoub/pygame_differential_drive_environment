import pygame
import math
import numpy as np
from constants import *
from robot import Robot
import gym
import random

def Position(x, y):
    xOffset = 960
    yOffset = 540
    return (x + xOffset, y + yOffset)

class Environment(pygame.sprite.Sprite, gym.Env):
    def __init__(self, dimentions=(1080,1920), mapImg='../images/map.png'):
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
        self.steps = 0
        self.map.blit(self.image, self.rect)
        self.robot = Robot(Position(0,0), '../images/robot.png')

        self.goal = (Position(800, 800))

        #GYM ENvironment
        self.initialDistanceToGoal = 1000
        self.action_space = gym.spaces.Box(low=np.array([0, -2]), high=np.array([0.1, 2]), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32) #60rays + xy0 robot + xy goal
        self.times = 0
        self.reset()
        




    def reset(self):
        self.times += 1
        self.steps = 0
        self.goal = Position(random.randint(-300, 275),random.randint(-350, 350))

        position = Position(random.randint(-300, 275),random.randint(-350, 350))
        self.robot.setPose(position[0],position[1], 0)
        self.refresh()
        _reached, self.initialDistanceToGoal = self.goalReached()
        return self.getObservation()

    def updateGoal(self, x, y):
        self.goalx = x
        self.goaly = y

    def addRobot(self, position, imagePath):
        self.robots = Robot(position, imagePath)

    def refresh(self):
        self.map.blit(self.image, self.rect)
        self.robot.draw(self)
        self.robot.scan(self)
        self.robot.drawRays(self)

    def checkCollision(self):
        pygame.draw.line(self.map, self.red, (self.robot.x,self.robot.y), (self.goal[0],self.goal[1]))

        if self.mask.overlap(self.robot.mask, (self.robot.x, self.robot.y)):
            return True
        
        return False      

    def step(self, action):
        self.steps += 1
        self.robot.move(action[0], action[1], 0)
        colision = self.checkCollision()
        self.refresh()
        return self.getObservation(), self.getReward(self.goal, colision, action[0], action[1], self.steps),  self.done(), {} ## fix get reward
    
    def getObservation(self):
        scan = np.array(self.robot.lidarData)
        robotPose = np.array([self.robot.x, self.robot.y, self.robot.theta])
        goalPose = np.array([self.goal[0], self.goal[1]])
        vels = np.array([self.robot.rlav, self.robot.rllv])
        obs = np.concatenate((scan, robotPose, vels ,goalPose))
        return obs

    def getReward(self, distance_to_goal, obstacle_collision, linear_velocity, angular_velocity, time_step):
    # Goal-reaching reward
        reached, distance_to_goal = self.goalReached()
        if reached:
            goal_reward = 100.0
        else:
            goal_reward = 0.0   
        # Proximity reward
        # proximity_reward = max(-self.initialDistanceToGoal/500, (self.initialDistanceToGoal - distance_to_goal)/500)  # Adjust the scaling factor as needed   
        proximity_reward = -distance_to_goal / 1000  # Adjust the scaling factor as needed
        # Obstacle avoidance penalty
        obstacle_penalty = -100.0 if obstacle_collision else 0.0
        # Smoothness reward (linear velocity)
        linear_smoothness_reward = 0#linear_velocity - angular_velocity#max(0.0, 1.0 - abs(linear_velocity))  # Adjust the scaling factor as needed
        # Smoothness reward (angular velocity)
        angular_smoothness_reward = 0#max(0.0, 1.0 - abs(angular_velocity))  # Adjust the scaling factor as needed
        # Time penalty
        time_penalty = -1     # Adjust the scaling factor as needed
        # Energy efficiency reward (optional)
        energy_efficiency_reward = 0.0  # Add your implementation based on energy consumption metrics
        # Calculate the total reward
        total_reward = (
            goal_reward
            + proximity_reward
            + obstacle_penalty
            + linear_smoothness_reward
            + angular_smoothness_reward
            + time_penalty
            + energy_efficiency_reward
        )
        return total_reward
    
    def done(self):
        gr, _ = self.goalReached()
        if self.checkCollision() == True or gr == True or self.steps > 200:
        # if gr == True or self.steps > 75:
            return True
        return False

    def goalReached(self):
        tol = 0
        x = self.robot.x - self.goal[0]
        y = self.robot.y - self.goal[1]
        reached = math.sqrt(x**2+y**2)
        if self.times < 1000:
            tol = 100
        else:
            tol = 25
        if reached <= tol:
            return True, reached
        return False, reached
    
    def render(self):
        pygame.display.update()