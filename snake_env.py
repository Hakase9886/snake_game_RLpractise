import gym
from gym import spaces
import numpy as np
import random
import pygame
import sys

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, width=600, height=400, block_size=10):
        super(SnakeEnv, self).__init__()
        self.width = width
        self.height = height
        self.block_size = block_size
        
        # 動作：0=上, 1=下, 2=左, 3=右
        self.action_space = spaces.Discrete(4)
        # 狀態：簡單向量表示 [snake_head_x, snake_head_y, food_x, food_y, direction_x, direction_y]
        self.observation_space = spaces.Box(low=0, high=max(width, height), shape=(6,), dtype=np.int32)
        
        self.win = None  # 延後初始化 pygame 畫面
        self.reset()
        
    def reset(self):
        self.snake_pos = [self.width // 2, self.height // 2]
        self.snake_body = [self.snake_pos[:]]
        self.direction = 3  # 預設向右移動
        self._place_food()
        self.score = 0
        return self._get_state()
    
    def _place_food(self):
        self.food_pos = [
            random.randrange(0, self.width, self.block_size),
            random.randrange(0, self.height, self.block_size)
        ]
    
    def _get_state(self):
        if self.direction == 0:      # UP
            d = [0, -1]
        elif self.direction == 1:    # DOWN
            d = [0, 1]
        elif self.direction == 2:    # LEFT
            d = [-1, 0]
        else:                        # RIGHT
            d = [1, 0]
        state = np.array(self.snake_pos + self.food_pos + d, dtype=np.int32)
        return state
    
    def step(self, action):
        # 動作映射，避免直接反向
        if action == 0 and self.direction != 1:
            self.direction = 0
        elif action == 1 and self.direction != 0:
            self.direction = 1
        elif action == 2 and self.direction != 3:
            self.direction = 2
        elif action == 3 and self.direction != 2:
            self.direction = 3
        
        # 更新蛇頭位置
        if self.direction == 0:
            self.snake_pos[1] -= self.block_size
        elif self.direction == 1:
            self.snake_pos[1] += self.block_size
        elif self.direction == 2:
            self.snake_pos[0] -= self.block_size
        elif self.direction == 3:
            self.snake_pos[0] += self.block_size
        
        self.snake_body.insert(0, list(self.snake_pos))
        
        reward = 0
        done = False
        
        # 判斷是否吃到食物
        if self.snake_pos == self.food_pos:
            reward = 10
            self.score += 1
            self._place_food()
        else:
            self.snake_body.pop()
            reward = -0.1
        
        # 撞牆檢查
        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= self.width or
            self.snake_pos[1] < 0 or self.snake_pos[1] >= self.height):
            done = True
            reward = -10
        
        # 撞自己檢查
        if self.snake_pos in self.snake_body[1:]:
            done = True
            reward = -10
        
        state = self._get_state()
        return state, reward, done, {}
    
    def render(self, mode='human'):
        if self.win is None:
            self.win = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Snake Game - Training')
        self.win.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.win, GREEN, pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))
        pygame.draw.rect(self.win, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], self.block_size, self.block_size))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def close(self):
        if self.win is not None:
            pygame.display.quit()
            pygame.quit()