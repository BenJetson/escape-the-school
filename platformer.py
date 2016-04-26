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
LIGHT_GREY = (220, 220, 220)
DARKER_GREY = (150, 150, 150)
RED = (175, 0, 0)
PASTEL_BLUE = ()

# Fonts
FONT_SM = pygame.font.Font(None, 30)

# Character Images
student_img = graphic_loader("img/student.png")
teacher_img = graphic_loader("img/teacher.png")
# administrator_img = graphic_loader("img/admin.png")
# bad_student_img = graphic_loader("img/bad_student.png")

# Item Images
laptop_img = graphic_loader("img/laptop.png")
phone_img = graphic_loader("img/phone.png")
card_img = graphic_loader("img/playing_card.png")
staffbadge_img = graphic_loader("img/staff_badge.png")
exit_img = graphic_loader("img/exit.png")

# Physics
H_SPEED = 4
JUMP_POWER = 12
GRAVITY = 0.4
TERMINAL_VELOCITY = 10


class Student:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        
        self.vx = 0
        self.vy = 0
        self.speed = H_SPEED

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def jump(self, platforms):
        can_jump = False
        
        self.y += 1

        student_rect = self.get_rect()
                
        #if intersects.rect_rect(student_rect, ground.get_rect()):
            #can_jump = True
    
        for p in platforms:
            platform_rect = p.get_rect()

            if intersects.rect_rect(student_rect, platform_rect):
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
         self.vy = min(self.vy, TERMINAL_VELOCITY)
         
    def process_platforms(self, platforms):
        self.x += self.vx

        student_rect = self.get_rect()
        
        for p in platforms:
            platform_rect = p.get_rect()

            if intersects.rect_rect(student_rect, platform_rect):
                if self.vx > 0:
                    self.x = p.x - self.w
                elif self.vx < 0:
                    self.x = p.x + p.w
                    self.y += self.vy

        self.y += self.vy
        
        student_rect = self.get_rect()
        
        for p in platforms:
            platform_rect = p.get_rect()
            
            if intersects.rect_rect(student_rect, platform_rect):
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
    
    def check_ground(self, ground):
        if self.y + self.h > ground.y:
            self.y = ground.y - self.h
            self.vy = 0
                 
    def process_coins(self, coins):
        global score
        
        student_rect = self.get_rect()
        coins_to_remove = []
        
        for c in coins:
            coin_rect = c.get_rect()

            if intersects.rect_rect(student_rect, coin_rect):
                coins_to_remove.append(c)
                score += 1
                print(score)

        for c in coins_to_remove:
            coins.remove(c)

    def process_teachers(self, teachers):
        student_rect = self.get_rect()

        is_touching = False
            
        for t in teachers:
            teachers_rect = t.get_rect()

            if intersects.rect_rect(student_rect, teachers_rect):
                    print("bonk!")
                    is_touching = True

        if is_touching:
            self.speed = H_SPEED - 1
        else:
            self.speed = H_SPEED
            
        print(self.speed)
        
    def update(self, platforms, teachers):
        self.apply_gravity()
        self.process_platforms(platforms)
        self.check_screen_edges()
        #self.check_ground()
        #self.process_coins(coins)
        self.process_teachers(teachers)
        
    def draw(self):
        screen.blit(self.img, [self.x, self.y])


class OtherPeople:

    def __init__(self, x, y, img, vx=1, platform_bound=True):
        self.x = x
        self.y = y
        self.img = img
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.platform_bound = platform_bound

        self.vx = vx
        self.vy = 0

    def move_and_process_platforms(self, platforms):
        self.x += self.vx

        person_rect = self.get_rect()

        for p in platforms:
            platform_rect = p.get_rect()

            if intersects.rect_rect(person_rect, platform_rect):
                if self.vx > 0:
                    self.x = p.x - self.w
                    self.vx *= -1
                elif self.vx < 0:
                    self.x = p.x + p.w
                    self.vx *= -1

            if self.platform_bound:
                if (person_rect[0] == platform_rect[0] and
                        platform_rect[1] == person_rect[1] + person_rect[3]
                        and self.vx == -1):
                    self.vx *= -1
                elif (person_rect[0] + person_rect[2] == platform_rect[0] + platform_rect[2] and
                      person_rect[1] + person_rect[3] == platform_rect[1] and
                      self.vx == 1):
                    self.vx *= -1


        self.y += self.vy

        person_rect = self.get_rect()

        for p in platforms:
            platform_rect = p.get_rect()

            if intersects.rect_rect(person_rect, platform_rect):
                if self.vy > 0:
                    self.y = p.y - self.h
                if self.vy < 0:
                    self.y = p.y + p.h
                self.vy = 0


    def update(self, platforms):
        self.move_and_process_platforms(platforms)

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
        screen.blit(self.img, [self.x, self.y])


class Platform:

    def __init__(self, x, y, w, h, color=RED):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])


class Belongings:

    def __init__(self, x, y, img, is_visible=True, can_collect=True):
        self.x = x
        self.y = y
        self.img = img

        self.w = self.img.get_width()
        self.h = self.img.get_height()

        self.is_visible = is_visible
        self.can_collect = can_collect

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
        if self.is_visible:
            screen.blit(self.img, [self.x, self.y])


class BackgroundObjects:

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
student = Student(0, 250, student_img)
platforms = [Platform(0, 250, 100, 10),
             Platform(0, 475, 100, 10),
             Platform(125, 365, 100, 10),
             Platform(310, 550, 100, 10),
             Platform(580, 550, 100, 10),
             Platform(450, 350, 100, 10),
             Platform(0, 700, 100, 10),
             Platform(900, 700, 100, 10),
             Platform(450, 700, 100, 10),
             Platform(850, 100, 150, 10),
             Platform(0, 710, 1000, 90)]
background_objects = []
belongings = []
teachers = [OtherPeople(0, 411, teacher_img)]
administrators = []
bad_students = []

# Game stats
score = 0

# game loop
done = False

while not done:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                 student.jump(platforms)
            

    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_RIGHT]:
         student.move(student.speed)
    elif pressed[pygame.K_LEFT]:
         student.move(-student.speed)
    else:
         student.stop()

    # game logic
    # player.update(ground, platforms)
    student.update(platforms, teachers)

    for t in teachers:
        t.update(platforms)

    # Draw game objects on-screen.
    screen.fill(DARKER_GREY)

    for b in background_objects:
        b.draw()

    for p in platforms:
        p.draw()

    for b in belongings:
        b.draw()

    for a in administrators:
        a.draw()

    for t in teachers:
        t.draw()

    for b in bad_students:
        b.draw()

    student.draw()    
    # Messages
    SCORE = FONT_SM.render("Score:" + format(score), True, WHITE)
    screen.blit(SCORE, [0, 0])

    # update screen
    pygame.display.update()
    clock.tick(FPS)

# close window on quit
pygame.quit()

