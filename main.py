import time
import random

import pygame
from pygame.constants import *


class HeroPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        # 这个精灵类的初始化方法必须调用
        pygame.sprite.Sprite.__init__(self)

        # 创建一个玩家飞机图片，当作真正的飞机
        self.player = pygame.image.load("./images/me1.png")

        # 根据图片image获取矩形对象
        self.rect = self.image.get_rect()  # rect:矩形
        self.rect.topleft = [480 / 2 - 102 / 2, 700]
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
        self.screen.blit(self.player, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹添加到屏幕上
        self.bullets.draw(self.screen)

    def update(self):
        self.key_control()
        self.display()

        # if self.x < 0:
        #     self.x = 0
        # elif self.x > 480 - 102:
        #     self.x = 480 - 102

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
        self.player = pygame.image.load("./images/enemy1.png")
        # 根据图片image获取矩形对象，
        self.rect = self.image.get_rect()
        self.rect.topleft[0, 0]

        # 创建一个子弹列表
        self.bullets = pygame.sprite.Group()

        # 飞机速度
        self.speed = 15

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
        elif self.rect.right > 480 - 57:
            self.direct = 'left'

    def display(self):
        # 将敌方飞机图片放入窗口中
        self.screen.blit(self.player, self.rect)

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
        if self.rect.top < 743:
            self.kill()


# 创建背景音乐
class GameSound(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load('./sound/game_music.ogg')
        pygame.mixer.music.set_volume(0.5)  # 声音大小

    def playbackgroundmusic(self):
        pygame.mixer.music.play(-1)  # 循环


def main():
    """完整的整个程序的控制"""
    sound = GameSound()
    sound.playbackgroundmusic()

    # 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480, 700), 0, 32)
    # 创建一个和窗口大小一样的图片，用来充当背景
    background = pygame.image.load('./images/background.png')
    # 创建玩家飞机对象
    player = HeroPlane(screen)
    # 创建一个地方飞机的图片
    enemyplane = EnemyPlane(screen)

    # 设定需要显示的背景图
    while True:
        # 将背景图片显示到窗口中
        screen.blit(background, (0, 0))

        # 遍历所有的事件
        for event in pygame.event.get():
            # 判断事件类型 如果是退出
            if event.type == QUIT:
                # pygame的退出
                pygame.quit()
                # 程序的退出
                exit()

        # 执行飞机的按键监听
        player.key_control()
        # 飞机的显示
        player.display()
        # 敌方飞机的显示
        enemyplane.display()
        # 敌方飞机自动移动
        enemyplane.auto_move()
        # 敌方飞机开火
        enemyplane.auto_fire()

        pygame.display.update()
        time.sleep(0.05)


if __name__ == "__main__":
    main()
