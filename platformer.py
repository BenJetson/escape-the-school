#  Escape the School

import pygame
import random
import intersects
from graphic_handler import *

pygame.init()

# Window settings
WIDTH = 1000
HEIGHT = 800
TITLE = "Escape the School"
FPS = 60

# Make the window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (175, 0, 0)

# Fonts
FONT_SM = pygame.font.Font(None, 30)

# Images


# Physics
H_SPEED = 4
JUMP_POWER = 12
GRAVITY = 0.4

class Student():

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        
        self.vx = 0
        self.vy = 0

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def jump(self, ground, platforms):
        can_jump = False
        
        self.y += 1

        student_rect = self.get_rect()
                
        if intersects.rect_rect(student_rect, ground.get_rect()):
            can_jump = True
    
        for p in platforms:
            platform_rect = p.get_rect()

            if intersects.rect_rect(spaceman_rect, platform_rect):
                can_jump = True

        if can_jump:
            self.vy = -JUMP_POWER

        self.y -= 1

    def move(self, vx):
        self.vx = vx

    def stop(self):
        self.vx = 0

    def apply_gravity(self):
         self.vy += GRAVITY

    def process_platforms(self, platforms):
        self.x += self.vx

        spaceman_rect = self.get_rect()
        
        for p in platforms:
            platform_rect = p.get_rect()

            if intersects.rect_rect(spaceman_rect, platform_rect):
                if self.vx > 0:
                    self.x = p.x - self.w
                elif self.vx < 0:
                    self.x = p.x + p.w
                    self.y += self.vy

        self.y += self.vy
        
        spaceman_rect = self.get_rect()
        
        for p in platforms:
            platform_rect = p.get_rect()
            
            if intersects.rect_rect(spaceman_rect, platform_rect):
                if self.vy > 0:
                    self.y = p.y - self.h
                if self.vy < 0:
                    self.y = p.y + p.h
                    self.vy = 0

    def check_screen_edges(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.w > WIDTH:
            self.x = WIDTH - self.w

    def check_ground(self):
        if self.y + self.h > ground.y:
            self.y = ground.y - self.h
            self.vy = 0
                
    def process_coins(self, coins):
        global score
        
        spaceman_rect = self.get_rect()
        coins_to_remove = []
        
        for c in coins:
            coin_rect = c.get_rect()

            if intersects.rect_rect(spaceman_rect, coin_rect):
                coins_to_remove.append(c)
                score += 1
                print(score)

        for c in coins_to_remove:
            coins.remove(c)

    def process_monsters(self, monsters):
        spaceman_rect = self.get_rect()

        for m in monsters:
            monster_rect = m.get_rect()

            if intersects.rect_rect(spaceman_rect, monster_rect):
                    print("bonk!")
            
    def update(self, ground, platforms):
        self.apply_gravity()
        self.process_platforms(platforms)
        self.check_screen_edges()
        self.check_ground()
        self.process_coins(coins)
        self.process_monsters(monsters)
        
    def draw(self):
        screen.blit(self.img, [self.x, self.y])

class Monster():

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        
        self.vx = 0
        self.vy = 0

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
        screen.blit(self.img, [self.x, self.y])

'''
class Ground():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.w = self.img.get_width()
        self.h = self.img.get_height()

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]
        
    def draw(self):
        screen.blit(self.img, [self.x, self.y])
  '''      
class UFO():

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def update(self):
        self.x -= 3

        if self.x < -200:
            self.x = 1000
            self.y = random.randrange(30, 150)

    def draw(self):
        screen.blit(self.img, [self.x, self.y])
"""             
class Planet():

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.w = self.img.get_width()
        self.h = self.img.get_height()

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]
    
    def update(self):
        pass

    def draw(self):
        screen.blit(self.img, [self.x, self.y])

"""
"""
class Stars():

    def __init__(self, num_stars):
        self.stars = []

        for i in range(num_stars):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            r = random.randrange(1, 3)
            self.stars.append([x, y, r])

    def draw(self):
        for s in self.stars:
            pygame.draw.circle(screen, WHITE, [s[0], s[1]], s[2])            
"""

class Platform():

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
        pygame.draw.rect(screen, RED, [self.x, self.y, self.w, self.h])

class Coin():

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.w = self.img.get_width()
        self.h = self.img.get_height()

        self.value = 1

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
        screen.blit(self.img, [self.x, self.y])


# Make game objects
platforms = [Platform(0, 250, 100, 10),
             Platform(0, 600, 100, 10),
             Platform(100, 375, 100, 10),
             Platform(350, 600, 100, 10)]

# Game stats
score = 0
'''
# game loop
done = False

while not done:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump(ground, platforms)
            

    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_RIGHT]:
        player.move(H_SPEED)
    elif pressed[pygame.K_LEFT]:
        player.move(-H_SPEED)
    else:
        player.stop()

    # game logic
    player.update(ground, platforms)
    ufo.update()
 '''
    #drawing
screen.fill(BLACK)
'''
    stars.draw()
    planet.draw()
    ufo.draw()
    ground.draw()
    player.draw()
'''
for p in platforms:
    p.draw()
'''
    for c in coins:
        c.draw()

    for m in monsters:
        m.draw()

    # Messages
    SCORE = FONT_SM.render("Score:" + format(score), True, WHITE)
    screen.blit(SCORE, [0, 0])
 '''
    # update screen
pygame.display.update()
clock.tick(FPS)

# close window on quit
#pygame.quit ()
