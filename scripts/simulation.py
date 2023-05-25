#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
import pygame
import math
import numpy as np
from constants import *
from environment import Environment
import time
from ddpg import DDPG
import tensorflow as tf
import gym





if __name__ == "__main__":
    pygame.init()
    env = Environment() 
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    action_bound = env.action_space.high

    agent = DDPG(state_dim, action_dim, action_bound)
    agent.replay_buffer = []
    agent.train(env, num_episodes=10000000)
    
    # # Usage example
    # env = gym.make('LunarLanderContinuous-v2')
    # state_dim = env.observation_space.shape[0]
    # action_dim = env.action_space.shape[0]
    # action_bound = env.action_space.high

    # agent = DDPG(state_dim, action_dim, action_bound)
    # agent.replay_buffer = []
    # agent.train(env, num_episodes=100)