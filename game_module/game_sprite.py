import pygame
import game_module.game_setting as setting
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(setting.GREEN)
        self.image = pygame.transform.scale(image, (50, 40))  # 調整圖片大小
        self.image.set_colorkey(setting.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = setting.SCREEN_WIDTH / 2
        self.rect.bottom = setting.SCREEN_HEIGHT - 10
        self.speed = 5
        self.radius = 20  # 設定碰撞半徑
        self.__health = setting.HEALTH  # 生命值
        self.lives = setting.LIVES
        self.hidden = False
        self.hide_time = 0
        self.gun_power = 1
        self.gun_power_time = 0

    def createBullet(self, bullet_image):
        if not self.hidden:
            if self.gun_power >= 2:
                return [
                    Bullet(bullet_image, self.rect.left, self.rect.centery),
                    Bullet(bullet_image, self.rect.right, self.rect.centery),
                ]
            else:
                return Bullet(bullet_image, self.rect.centerx, self.rect.top)

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (setting.SCREEN_WIDTH / 2, setting.SCREEN_HEIGHT + 200)

    def gun_power_up(self):
        self.gun_power += 1
        self.gun_power_time = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = setting.SCREEN_WIDTH / 2
            self.rect.bottom = setting.SCREEN_HEIGHT - 10

        if (
            self.gun_power > 1
            and pygame.time.get_ticks() - self.gun_power_time > setting.GUN_POWER_TIME
        ):
            self.gun_power -= 1
            self.gun_power_time = pygame.time.get_ticks()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if self.rect.right > setting.SCREEN_WIDTH:
            self.rect.right = setting.SCREEN_WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value > setting.HEALTH:
            self.__health = setting.HEALTH
        else:
            self.__health = value


class Rock(pygame.sprite.Sprite):
    def __init__(self, images: [], sounds: []):
        super().__init__()
        # self.image = pygame.Surface((30, 40))
        # self.image.fill(setting.RED)
        self.image_orignal = random.choice(images)  # 原始圖片
        self.image_orignal.set_colorkey(setting.BLACK)
        self.image = self.image_orignal.copy()  # 複製原始圖片到image上
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)  # 設定碰撞半徑
        # pygame.draw.circle(self.image, setting.BLACK, self.rect.center,
        #    self.radius)  # 繪製碰撞半徑
        self.__refresh()
        self.total_degree = 0  # 總共旋轉角度
        self.rot_degree = random.randrange(-3, 3)  # 轉動角度
        self.sound = random.choice(sounds)

    def __refresh(self):
        self.rect.x = random.randrange(0, setting.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rotate()  # 石頭旋轉
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 石頭超出畫面時，重設位置
        if (
            self.rect.top > setting.SCREEN_HEIGHT
            or self.rect.right < 0
            or self.rect.left > setting.SCREEN_WIDTH
        ):
            self.__refresh()

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_orignal, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    @classmethod
    def createRocks(cls, images, sounds, count):
        rocks = pygame.sprite.Group()
        for i in range(count):
            rock = cls(images, sounds)
            rocks.add(rock)
        return rocks


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        # self.image = pygame.Surface((10, 20))
        self.image = image
        self.image.set_colorkey(setting.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, images):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = setting.ANIM_FRAME_RATE  # 每50毫秒換一張圖片

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame += 1

            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pygame.sprite.Sprite):
    def __init__(self, center, images: {}):
        super().__init__()
        self.type = random.choice(list(images.keys()))
        self.image = images[self.type]
        self.image.set_colorkey(setting.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > setting.SCREEN_HEIGHT:
            self.kill()
