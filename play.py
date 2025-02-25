# manual_play.py
import pygame
import time
from snake_env import SnakeEnv

def get_joystick_direction(joystick):
    """
    根據方向盤軸值判斷方向：
    返回值：
      0 -> 向上, 1 -> 向下, 2 -> 向左, 3 -> 向右
      若無足夠輸入則返回 None
    """
    x_axis = joystick.get_axis(0)  # 左右軸
    y_axis = joystick.get_axis(1)  # 上下軸
    threshold = 0.5  # 閾值，可根據實際情況調整

    if abs(x_axis) > abs(y_axis):
        if x_axis < -threshold:
            return 2  # 向左
        elif x_axis > threshold:
            return 3  # 向右
    else:
        if y_axis < -threshold:
            return 0  # 向上
        elif y_axis > threshold:
            return 1  # 向下
    return None

def game_over_screen(env):
    """
    顯示 Game Over 畫面與 Play Again 按鈕，等待玩家點擊。
    若玩家點擊 Play Again，返回 True；若退出遊戲，返回 False。
    """
    # 使用 pygame 字型建立文字
    font_big = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 36)
    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    play_again_text = font_small.render("Play Again", True, (255, 255, 255))
    
    # 根據文字建立一個按鈕的矩形範圍
    button_rect = play_again_text.get_rect()
    button_rect.center = (env.width // 2, env.height // 2 + 50)
    
    while True:
        env.win.fill((0, 0, 0))
        # 繪製 Game Over 文字（置中顯示）
        text_rect = game_over_text.get_rect(center=(env.width//2, env.height//2 - 50))
        env.win.blit(game_over_text, text_rect)
        
        # 畫出 Play Again 按鈕的背景（可點擊區域）
        pygame.draw.rect(env.win, (0, 128, 0), button_rect.inflate(20, 20))
        # 繪製 Play Again 文字
        env.win.blit(play_again_text, button_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
        pygame.time.delay(100)

def main():
    pygame.init()
    
    # 初始化方向盤（若有連接）
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("方向盤初始化成功:", joystick.get_name())
    else:
        print("未檢測到方向盤，將改用鍵盤控制。")
    
    env = SnakeEnv()
    env.reset()
    clock = pygame.time.Clock()
    # 記錄最後一次有效操作，初始預設向右（3）
    last_action = 3
    
    # 外層循環：每次遊戲結束後可重玩
    while True:
        # 進入新一局遊戲前，重置環境
        env.reset()
        done = False
        
        # 遊戲主循環
        while not done:
            env.render()
            
            # 處理退出事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
            if done:
                break
            
            # 優先讀取方向盤輸入
            action = None
            if joystick is not None:
                action = get_joystick_direction(joystick)
            
            # 若無方向盤輸入，改用鍵盤
            if action is None:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    action = 0
                elif keys[pygame.K_DOWN]:
                    action = 1
                elif keys[pygame.K_LEFT]:
                    action = 2
                elif keys[pygame.K_RIGHT]:
                    action = 3
            
            # 若沒有新的操作，則使用上一次的動作
            if action is None:
                action = last_action
            else:
                last_action = action
            
            # 更新環境狀態
            state, reward, done, _ = env.step(action)
            
            clock.tick(10)  # 控制遊戲更新速度
        
        # 當遊戲結束，顯示 Game Over 畫面
        play_again = game_over_screen(env)
        if not play_again:
            break  # 玩家選擇退出，則離開外層循環
    
    env.close()
    pygame.quit()

if __name__ == '__main__':
    main()
