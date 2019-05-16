import pygame
import sys

SCREEN_SIZE =   (640,480)
SCREEN_COLOR =  (255,255,255)
BALL_SPEED =    [5,5]
CLOCK_VALUE =   60

ball = pygame.image.load('image/ball.jpg')
ballrect = ball.get_rect()

ballrect = ballrect.move([0,100])
clock = pygame.time.Clock()         #设置时钟

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

#一直显示窗口
while True:
    #每秒执行60次
    clock.tick(CLOCK_VALUE)
    #获取事件，等于退出就正常退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    ballrect = ballrect.move(BALL_SPEED)#移动小球
    #碰边就反向移动
    if ballrect.left < 0 or ballrect.right > 640 :
        BALL_SPEED[0] = -BALL_SPEED[0]
    if ballrect.top < 0 or ballrect.bottom > 480 :
        BALL_SPEED[1] = -BALL_SPEED[1]
    screen.fill(SCREEN_COLOR)           #改变窗口颜色
    screen.blit(ball,ballrect)          #画球
    pygame.display.flip()               #更新显示
pygame.quit()