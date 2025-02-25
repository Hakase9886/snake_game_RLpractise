import numpy as np
import pygame
from tensorflow.keras.models import load_model
from snake_env import SnakeEnv

if __name__ == "__main__":
    pygame.init()
    env = SnakeEnv()
    state_size = env.observation_space.shape[0]
    
    # 載入訓練好的模型
    model = load_model("trained_dqn_snake.h5")
    
    # 不需要訓練智能體，因此直接使用模型做推論
    done = False
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    
    while not done:
        env.render()
        # 模型預測各個動作的 Q 值，選擇最大的作為動作
        q_values = model.predict(state, verbose=0)
        action = np.argmax(q_values[0])
        
        next_state, reward, done, _ = env.step(action)
        state = np.reshape(next_state, [1, state_size])
        
        pygame.time.delay(50)  # 控制畫面更新速度
        
    env.close()
    pygame.quit()
