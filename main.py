import random
import pygame
import os
import game_module.game_setting as setting
import game_module.game_sprite as sprite

# 初始化 pygame
pygame.init()
pygame.mixer.init()  # 初始化音效
pygame.display.set_caption("太空大戰")
screen = pygame.display.set_mode((setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))

# 載入圖片 並轉換格式
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(setting.BLACK)
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

pygame.display.set_icon(player_mini_img)  # 設定視窗圖示

explosion_anim = {}
explosion_anim["large"] = []  # 大爆炸圖片
explosion_anim["small"] = []  # 小爆炸圖片
explosion_anim["player"] = []  # 玩家爆炸圖片
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(setting.BLACK)
    explosion_anim["large"].append(pygame.transform.scale(expl_img, (75, 75)))
    explosion_anim["small"].append(pygame.transform.scale(expl_img, (30, 30)))
    # 玩家爆炸圖片
    player_expl_img = pygame.image.load(
        os.path.join("img", f"player_expl{i}.png")
    ).convert()
    player_expl_img.set_colorkey(setting.BLACK)
    explosion_anim["player"].append(player_expl_img)

power_imgs = {}
power_imgs["shield"] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs["gun"] = pygame.image.load(os.path.join("img", "gun.png")).convert()

# 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
explosion_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav")),
]
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))  # 背景音樂
pygame.mixer.music.set_volume(0.5)  # 設定音量
pygame.mixer.music.play(loops=-1)  # 播放背景音樂 -1: 無限循環


# 載入字型
# font_name = pygame.font.match_font("arial")
font_name = os.path.join("font.ttf")

show_init = True  # 是否顯示初始畫面
running = True  # 遊戲是否正在執行
clock = pygame.time.Clock()  # 計時器

all_sprites = pygame.sprite.Group()
player = sprite.Player(player_img)
rocks = sprite.Rock.createRocks(rock_imgs, explosion_sounds, 8)
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(rocks)
background_offset_y = 0  # 背景圖片的y軸偏移量
score = 0  # 分數
player_explsion = None
# 遊戲內用到的函式


def init_game():
    global all_sprites, player, rocks, bullets, powers, background_offset_y, score, player_explsion
    all_sprites = pygame.sprite.Group()
    player = sprite.Player(player_img)
    rocks = sprite.Rock.createRocks(rock_imgs, explosion_sounds, 8)
    bullets = pygame.sprite.Group()
    powers = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(rocks)
    background_offset_y = 0  # 背景圖片的y軸偏移量
    score = 0  # 分數
    player_explsion = None


# 射擊
def shoot():
    bullet = player.createBullet(bullet_img)
    if bullet == None:
        return
    bullets.add(bullet)
    all_sprites.add(bullet)
    shoot_sound.play()  # 播放音效


# 繪製文字
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, setting.WHITE)  # True: 開啟反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# 捲動背景
def bg_scrolling():
    global background_offset_y  # 使用全域變數
    # 更新y軸偏移量，使背景滾動
    background_offset_y += 1

    # 如果超出背景高度，重設y軸偏移量
    if background_offset_y > background_img.get_height():
        background_offset_y = 0


# 產生新的石頭
def create_rock():
    rock = sprite.Rock(rock_imgs, explosion_sounds)
    rocks.add(rock)
    all_sprites.add(rock)


# 產生爆炸
def create_explosion(center, size):
    expl = sprite.Explosion(center, explosion_anim[size])
    all_sprites.add(expl)


# 繪製血條
def draw_health_bar(surf, x, y, health):
    if health < 0:
        health = 0
    fill = health / 100 * setting.HEALTH_BAR_LENGTH
    outline_rect = pygame.Rect(
        x, y, setting.HEALTH_BAR_LENGTH, setting.HEALTH_BAR_HEIGHT
    )
    fill_rect = pygame.Rect(x, y, fill, setting.HEALTH_BAR_HEIGHT)
    pygame.draw.rect(surf, setting.GREEN, fill_rect)
    pygame.draw.rect(surf, setting.WHITE, outline_rect, 2)  # 2: outline的寬度


# 繪製玩家生命數
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "太空大戰", 64, setting.SCREEN_WIDTH / 2, setting.SCREEN_HEIGHT / 4)
    draw_text(
        screen,
        "← → 移動，空白鍵射擊",
        22,
        setting.SCREEN_WIDTH / 2,
        setting.SCREEN_HEIGHT / 2,
    )
    draw_text(
        screen,
        "按任意鍵開始",
        18,
        setting.SCREEN_WIDTH / 2,
        setting.SCREEN_HEIGHT * 3 / 4,
    )
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(setting.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return True
            if event.type == pygame.KEYUP:
                waiting = False
                init_game()
                return False


def update():
    global running
    global score

    bg_scrolling()  # 滾動背景

    all_sprites.update()  # 更新遊戲物件

    # 檢查子彈是否擊中石頭，如果擊中石頭，則石頭消失，並產生新的石頭
    hits = pygame.sprite.groupcollide(rocks, bullets, dokilla=True, dokillb=True)
    for hit in hits:
        score += int(hit.radius)
        hit.sound.play()  # 播放音效
        create_rock()
        create_explosion(hit.rect.center, "large")
        if random.random() > 1 - setting.POWERUP_RATE:
            power = sprite.Power(hit.rect.center, power_imgs)
            all_sprites.add(power)
            powers.add(power)

    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == "shield":
            shield_sound.play()  # 播放音效
            player.health += setting.HEALTH_POWER
            if player.health > setting.HEALTH:
                player.health = setting.HEALTH
        elif hit.type == "gun":
            gun_sound.play()  # 播放音效
            player.gun_power_up()

    # 檢查石頭是否撞到玩家
    hits = pygame.sprite.groupcollide(
        pygame.sprite.Group(player),
        rocks,
        dokilla=False,
        dokillb=True,
        collided=pygame.sprite.collide_circle,
    )  # 使用圓形碰撞偵測 需在Player、Rock中定義radius

    for hit in hits:
        player.health -= hit.radius
        create_rock()
        create_explosion(hit.rect.center, "small")
        if player.health <= 0:
            global player_explsion
            player_explsion = sprite.Explosion(
                player.rect.center, explosion_anim["player"]
            )
            all_sprites.add(player_explsion)
            die_sound.play()  # 播放音效
            player.lives -= 1
            player.health = setting.HEALTH
            player.hide()

    # 檢查玩家是否死亡
    if player.lives <= 0 and player_explsion != None and not player_explsion.alive():
        global show_init
        show_init = True


# Game Loop
while running:
    clock.tick(setting.FPS)  # 60 FPS

    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False

    # 取得輸入
    for event in pygame.event.get():
        # 檢查是否關閉視窗
        if event.type == pygame.QUIT:
            running = False

        # 檢查是否按下按鍵
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot()

    # 更新遊戲狀態
    update()

    # 渲染畫面
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, background_offset_y - background_img.get_height()))
    screen.blit(background_img, (0, background_offset_y))
    all_sprites.draw(screen)
    draw_text(screen, f"分數: {score}", 18, setting.SCREEN_WIDTH / 2, 10)
    draw_health_bar(screen, 5, 18, player.health)
    draw_lives(screen, setting.SCREEN_WIDTH - 100, 5, player.lives, player_mini_img)
    pygame.display.update()

pygame.quit()
