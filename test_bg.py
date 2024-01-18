import pygame
import os

# 初始化Pygame
pygame.init()

# 設定視窗大小
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("背景滾動")

# 載入背景圖片
background = pygame.image.load(os.path.join("img", "background.png")).convert()

# 初始化y軸偏移量
offset_y = 0

# 設定時脈
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新y軸偏移量，使背景滾動
    offset_y += 1

    # 如果超出背景高度，重設y軸偏移量
    if offset_y > background.get_height():
        offset_y = 0

    # 清除畫面
    screen.fill((0, 0, 0))

    # 繪製背景
    screen.blit(background, (0, offset_y - background.get_height()))
    screen.blit(background, (0, offset_y))

    # 更新視窗
    pygame.display.flip()

    # 控制幀數
    clock.tick(60)

# 關閉Pygame
pygame.quit()
