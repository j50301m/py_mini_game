from typing import Final

# 遊戲內設定值

# 螢幕寬高
SCREEN_WIDTH: Final[int] = 500
SCREEN_HEIGHT: Final[int] = 600

# 遊戲更新率
FPS: Final[int] = 60  # 邏輯更新率 (每一秒更新幾次)
ANIM_FRAME_RATE: Final[int] = 50  # 動畫更新率 (多少毫秒更新一次)

# 血條  生命數
HEALTH = 100
HEALTH_BAR_LENGTH = 100
HEALTH_BAR_HEIGHT = 10
LIVES = 3

# 調寶機率
POWERUP_RATE = 0.1
HEALTH_POWER = 20
GUN_POWER_TIME = 5000  # 強化持續時間

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
