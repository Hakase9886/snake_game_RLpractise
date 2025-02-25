import time
import numpy as np
import pygame
from snake_env import SnakeEnv
from dqn_agent import DQNAgent

if __name__ == "__main__":
    pygame.init()
    env = SnakeEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    
    episodes = 500
    batch_size = 32
    
    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        done = False
        time_step = 0
        
        while not done:
            env.render()  # 顯示遊戲畫面
            action = agent.act(state[0])
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state[0], action, reward, next_state[0], done)
            state = next_state
            time_step += 1
            
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
                
            pygame.time.delay(50)  # 控制畫面更新速度
            
            if done:
                print("Episode: {}/{}, Score: {}, Epsilon: {:.2f}".format(e+1, episodes, time_step, agent.epsilon))
                time.sleep(1)
    
    agent.model.save("trained_dqn_snake.h5")
    print("模型已儲存至 trained_dqn_snake.h5")

    env.close()
