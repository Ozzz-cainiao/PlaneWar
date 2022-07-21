import time
import random

import pygame
from pygame.constants import *


class HeroPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        # 这个精灵类的初始化方法必须调用
        pygame.sprite.Sprite.__init__(self)

        # 创建一个玩家飞机图片，当作真正的飞机
        self.image = pygame.image.load("./images/me1.png")

        # 根据图片image获取矩形对象
        self.rect = self.image.get_rect()  # rect:矩形
        self.rect.topleft = [Manager.bg_size[0] / 2 - 102 / 2, Manager.bg_size[1] - 126]
        # 飞机速度
        self.speed = 10
        # 窗口
        self.screen = screen
        # 创建一个子弹列表
        self.bullets = pygame.sprite.Group()

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            # print("上")
            self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            # print('下')
            self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            # print("左")
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            # print('右')
            self.rect.right += self.speed
        if key_pressed[K_SPACE]:
            # print('空格')
            # 按下空格键发射子弹
            bullet = Bullet(self.screen, self.rect.left, self.rect.top)
            # 把子弹放到列表里
            self.bullets.add(bullet)

    def display(self):
        # 将飞机图片放入窗口中
        self.screen.blit(self.image, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹添加到屏幕上
        self.bullets.draw(self.screen)

    def update(self):
        self.key_control()
        self.display()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.left > Manager.bg_size[0] - 102:
            self.rect.left = Manager.bg_size[0] - 102

        # # 遍历所有子弹
        # for bullet in self.bullets:
        #     # 让子弹飞，修改子弹y坐标
        #     bullet.auto_move()
        #     # 子弹显示在窗口
        #     bullet.display()


# 创建一个子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        # 创建图片
        self.image = pygame.image.load('./images/bullet2.png')

        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 102 / 2 - 4 / 2, y - 11]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 20

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹移出屏幕上方  销毁子弹对象
        if self.rect.top < -11:
            self.kill()


# 创建敌方飞机类
class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        # 创建一个敌方飞机图片，当作真正的飞机
        self.image = pygame.image.load("./images/enemy1.png")
        # 根据图片image获取矩形对象，
        self.rect = self.image.get_rect()  # rect：矩形
        self.rect.topleft = [0, 0]

        # 创建一个子弹列表
        self.bullets = pygame.sprite.Group()

        # 飞机速度
        self.speed = 5

        # 窗口
        self.screen = screen
        # 方向属性
        self.direct = 'right'

    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()

    def auto_move(self):
        if self.direct == 'right':
            self.rect.right += self.speed
        elif self.direct == 'left':
            self.rect.right -= self.speed

        if self.rect.right < 0:
            self.direct = 'right'
        elif self.rect.right > Manager.bg_size[0] - 57:
            self.direct = 'left'

    def display(self):
        # 将敌方飞机图片放入窗口中
        self.screen.blit(self.image, self.rect)

        # 更新子弹坐标
        self.bullets.update()

        # 把 所有子弹添加到屏幕
        self.bullets.draw(self.screen)

    def auto_fire(self):
        """自动开火 创建子弹对象 添加进列表 """

        random_num = random.randint(1, 10)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)

        # # 遍历所有子弹
        # for bullet in self.bullets:
        #     # 让子弹飞，修改子弹y坐标
        #     bullet.auto_move()
        #     # 子弹显示在窗口
        #     bullet.display()


# 创建敌方子弹类
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        # 创建图片
        self.image = pygame.image.load('./images/bullet1.png')

        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 56 / 2 - 4 / 2, y + 43]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 20

    def update(self):
        # 修改子弹坐标
        self.rect.top += self.speed
        # 如果子弹移出屏幕上方  销毁子弹对象
        if self.rect.top > 743:
            self.kill()


# 创建背景音乐
class GameSound(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load('./sound/game_music.ogg')
        pygame.mixer.music.set_volume(0.5)  # 声音大小

        self._bomb = pygame.mixer.Sound('./sound/use_bomb.wav')

    def playbackgroundmusic(self):
        pygame.mixer.music.play(-1)  # 循环

    def playbombsound(self):
        pygame.mixer.Sound.play(self._bomb)


# 添加一个碰撞类
class Bomb(object):
    # 初始化碰撞
    def __init__(self, screen, type):
        self.screen = screen
        if type == "enemy":
            # 加载爆炸资源
            self.mImage = [pygame.image.load("./images/enemy1_down" + str(v) + ".png") for v in range(1, 5)]
        else:
            self.mImage = [pygame.image.load("./images/me_destroy_" + str(v) + ".png") for v in range(1, 5)]
        # 设置当前爆炸索引播放序列
        self.mIndex = 0
        # 爆炸设置
        self.mPos = [0, 0]
        # 是否可见
        self.mVisible = False

    def action(self, rect):
        # 爆炸触发方法

        # 爆炸触发的坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # 打开爆炸的开关
        self.mVisible = True

    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImage[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImage):
            # 如果下表到最后了  代表爆炸结束
            # 下标位置重置 mVisible重置
            self.mIndex = 0
            self.mVisible = False


# 地图
class Map(object):
    # 初始化地图
    def __init__(self, screen):
        self.mImage1 = pygame.image.load("./images/background.png")
        self.mImage2 = pygame.image.load("./images/background.png")
        # 窗口
        self.screen = screen
        # 地图初始位置
        self.y1 = 0
        self.y2 = -Manager.bg_size[1]

    # 移动地图
    def move(self):
        self.y1 += 2
        self.y2 += 2
        if self.y1 >= Manager.bg_size[1]:
            self.y1 = 0
        elif self.y2 >= 0:
            self.y2 = -Manager.bg_size[1]

    # 移动地图
    def draw(self):
        self.screen.blit(self.mImage1, (0, self.y1))
        self.screen.blit(self.mImage2, (0, self.y2))


class Manager(object):
    bg_size = (480, 700)

    def __init__(self):
        pygame.init()
        # 创建窗口
        self.screen = pygame.display.set_mode(Manager.bg_size, 0, 32)
        # 创建背景图片
        # self.background = pygame.image.load('./images/background.png')
        self.map = Map(self.screen)

        # 初始化一个装玩家精灵的group
        self.players = pygame.sprite.Group()
        # 初始化一个装敌方精灵的group
        self.enemies = pygame.sprite.Group()
        # 初始化一个玩家爆炸的对象
        self.player_bomb = Bomb(self.screen, "player")
        # 初始化一个敌机爆炸的对象
        self.enemy_bomb = Bomb(self.screen, "enemy")
        # 初始化一个声音播放的对象
        self.sound = GameSound()

    def exit(self):
        print("退出")
        pygame.quit()
        exit()

    def new_player(self):
        # 创建飞机对象，添加到玩家的组
        player = HeroPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        # 创建敌机的对象 添加到敌机的组
        enemy = EnemyPlane(self.screen)
        self.enemies.add(enemy)

    # 绘制文字
    def drawtext(self, text, x, y, textheight=30, fontcolor=(255, 0, 0), backgroundcolor=None):
        # 通过字体文件获取字体对象
        font_obj = pygame.font.Font("./font/font.ttf",textheight)
        #   配置要显示的文字
        text_obj = font_obj.render(text, True, fontcolor, backgroundcolor)
        # 获取要显示的对象的rect
        text_rect = text_obj.get_rect()
        # 设置显示对象的坐标
        text_rect.topleft = (x, y)
        # 绘制字到指定区域
        self.screen.blit(text_obj, text_rect)

    def main(self):
        # 播放背景音乐
        self.sound.playbackgroundmusic()
        # 创建一个玩家
        self.new_player()
        # 创建一个敌机
        self.new_enemy()
        while True:
            # 把背景图片贴到窗口
            # self.screen.blit(self.background, (0, 0))
            self.map.move()
            self.map.draw()
            # 绘制文字
            self.drawtext("HP:1000",20,10)
            # 遍历所有的事件
            for event in pygame.event.get():
                # 判断事件类型 如果是退出
                if event.type == QUIT:
                    self.exit()

            # 调用爆炸的对象
            self.player_bomb.draw()
            self.enemy_bomb.draw()

            # 判断碰撞
            iscollide = pygame.sprite.groupcollide(self.players, self.enemies, True, True)

            if iscollide:
                items = list(iscollide.items())[0]
                print(items)
                x = items[0]
                y = items[1][0]
                # 玩家爆炸图片
                self.player_bomb.action(x.rect)
                # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                # 爆炸的声音
                self.sound.playbombsound()

            # 玩家飞机和子弹的显示
            self.players.update()
            # 敌方飞机和子弹的显示
            self.enemies.update()

            # 刷新窗口内容
            pygame.display.update()
            time.sleep(0.01)


if __name__ == "__main__":
    manager = Manager()
    manager.main()

# def main():
#     """完整的整个程序的控制"""
#     sound = GameSound()
#     sound.playbackgroundmusic()
#
#     # 创建一个窗口，用来显示内容
#     screen = pygame.display.set_mode((480, 700), 0, 32)
#     # 创建一个和窗口大小一样的图片，用来充当背景
#     background = pygame.image.load('./images/background.png')
#     # 创建玩家飞机对象
#     player = HeroPlane(screen)
#     # 创建一个地方飞机的图片
#     enemyplane = EnemyPlane(screen)
#
#     # 设定需要显示的背景图
#     while True:
#         # 将背景图片显示到窗口中
#         screen.blit(background, (0, 0))
#
#         # 遍历所有的事件
#         for event in pygame.event.get():
#             # 判断事件类型 如果是退出
#             if event.type == QUIT:
#                 # pygame的退出
#                 pygame.quit()
#                 # 程序的退出
#                 exit()
#
#         # 执行飞机的按键监听
#         player.key_control()
#         # 飞机的显示
#         player.display()
#         # 敌方飞机的显示
#         enemyplane.display()
#         # 敌方飞机自动移动
#         enemyplane.auto_move()
#         # 敌方飞机开火
#         enemyplane.auto_fire()
#
#         pygame.display.update()
#         time.sleep(0.05)
#
#
# if __name__ == "__main__":
#     main()
