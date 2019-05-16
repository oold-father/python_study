import pygame
import sys

width =         1024
height =        288
SCREEN_SIZE =   (width,height)

FPS =           10


def main_game():
    global screen,clock
    #是否游戏结束
    over = False
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    map_1 = Map(0,0)
    map_2 = Map(1024,0)
    dinosaur = Dinosaur()
    obstacle = Obstacle(1024,158)
    #obstacle = [Obstacle(1024,158),Obstacle(1536,158),Obstacle(2048,158)]

#    dinosaurs = pygame.sprite.Group()
#    obstacles = pygame.sprite.Group()
#    dinosaurs.add(dinosaur)
#    for i in obstacle:
#        obstacles.add(i)

    pygame.display.set_caption('小恐龙')
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dinosaur.jump()
        if not over:
            map_1.map_rolling()
            map_1.map_update(screen)
            map_2.map_rolling()
            map_2.map_update(screen)
            obstacle.obstacle_rolling()
            obstacle.obstacle_update(screen)
#            for i in obstacle:
#                i.obstacle_rolling()
#                i.obstacle_update(screen)

#        if pygame.sprite.spritecollide(dinosaur, obstacles, False):
        if pygame.sprite.collide_rect(dinosaur,obstacle):
            #over = True
            pass

        dinosaur.move()
        dinosaur.draw_dinosaur(screen)
        pygame.display.update()

#障碍类
class Obstacle(pygame.sprite.Sprite):
    #加载障碍
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.obstacle_img = pygame.image.load('image/02.png').convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.obstacle_img.get_rect()
    def obstacle_rolling(self):
        if self.x < 0:
            self.x += 2048
        else:
            self.x -= 5
    def obstacle_update(self,surface):
        surface.blit(self.obstacle_img,(self.x,self.y))
#地图
class Map():
    #加载初始地图
    def __init__(self,x,y):
        self.bg = pygame.image.load('image/bg.jpg').convert_alpha()
        self.x = x
        self.y = y

    #地图滚动显示
    def map_rolling(self):
        if self.x < -1024:
            self.x = 1024
        else:
            self.x -= 5

    #更新地图
    def map_update(self,surface):
        surface.blit(self.bg,(self.x,self.y))

#恐龙类
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #跳跃参数
        self.jump_state =   False
        self.jump_height =  50
        self.jump_low =     180
        self.jump_value =   0

        self.dinosaur_img = pygame.image.load('image/04.png').convert_alpha()
        self.rect = self.dinosaur_img.get_rect()

        #坐标
        self.x = 50
        self.y = self.jump_low

    def jump(self):
        self.jump_state = True
    
    def move(self):
        if self.jump_state:
            if self.y >= self.jump_low:
                self.jump_value = -5
            if self.y <= self.jump_height:
                self.jump_value = 5
            self.y += self.jump_value
            if  self.y >= self.jump_low:
                self.jump_state = False
    def draw_dinosaur(self,surface):
        surface.blit(self.dinosaur_img,(self.x,self.y))




if __name__ == '__main__':
    main_game()