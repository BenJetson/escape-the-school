#  Escape the School

import pygame
import random
import intersects
import calendar
import time
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

# Stages
START = 0
PLAYING = 1
END = 2

# Other Documents


# Character Images
student_img = graphic_loader("img/student.png")
teacher_img = graphic_loader("img/teacher.png")
admin_img = graphic_loader("img/admin.png")
bad_student_img = graphic_loader("img/bad_student.png")

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


def fix_inventory(inventory):
    pass


def get_current_time():
    return calendar.timegm(time.gmtime())


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
        self.temp_speed_changes = []

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

    def change_speed_temp(self, expiry_time, amount):
        self.temp_speed_changes.append({
            "expiryTime" : expiry_time,
            "changeAmount" : amount
        })

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

            if t.is_touching(student_rect):
                    print("bonk!")
                    # is_touching = True
                    self.change_speed_temp(get_current_time() + 5, H_SPEED/2)
            
        #print(self.speed)

    def process_admin(self, admin):
        student_rect = self.get_rect()
            
        for a in admin:
            admin_rect = a.get_rect()

            if intersects.rect_rect(student_rect, admin_rect):
                    print("ahh!")

    def process_bad_student(self, bad_student):
        student_rect = self.get_rect()
            
        for b in bad_student:
            bad_student_rect = b.get_rect()

            if intersects.rect_rect(student_rect, bad_student_rect):
                    print("ugh")

    def process_belongings(self, belongings, inventory):

        student_rect = self.get_rect()

        for b in belongings:
            if b.is_collectible:
                item_rect = b.get_rect()

                if intersects.rect_rect(student_rect, item_rect):
                    belongings.remove(b)
                    inventory.append(b)
                    fix_inventory(inventory)

                    if len(belongings) > 0:
                        belongings[0].activate()

    def process_speed_changes(self):
        self.speed = H_SPEED
        current_time = get_current_time()

        for p in self.temp_speed_changes:
            if not (p['expiryTime'] < current_time):
                self.speed -= p['changeAmount']
            else:
                self.temp_speed_changes.remove(p)

        self.speed = 1 if self.speed < 1 else self.speed

    def update(self, platforms, teachers, admin, bad_students, belongings, inventory):
        self.process_speed_changes()
        self.apply_gravity()
        self.process_platforms(platforms)
        self.check_screen_edges()
        #self.check_ground()
        #self.process_coins(coins)
        self.process_teachers(teachers)
        self.process_admin(admin)
        self.process_bad_student(bad_students)
        self.process_belongings(belongings, inventory)
        
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

        self.is_untouchable = False
        self.last_touch = 0

        self.vx = vx
        self.vy = 0

    def process_touchability(self):
        if self.last_touch + 5 == get_current_time():
            self.is_untouchable = False

    def is_touching(self, other_rect, dont_set_flag=False, ignore_untouchable=False):
        if (not self.is_untouchable) or ignore_untouchable:
            if intersects.rect_rect(self.get_rect(), other_rect):
                if not dont_set_flag:
                    self.is_untouchable = True
                    self.last_touch = get_current_time()

                return True

        return False

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

    def is_touching(self, other_rect, dont_set_flag=False, ignore_untouchable=False):
        if (not self.is_untouchable) or ignore_untouchable:
            if intersects.rect_rect(self.get_rect(), other_rect):
                if not dont_set_flag:
                    self.is_untouchable = True
                    self.last_touch = get_current_time()

                return True

        return False

    def update(self, platforms):
        self.process_touchability()
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

    def __init__(self, x, y, img, is_visible=False, is_collectible=False):
        self.x = x
        self.y = y
        self.img = img

        self.is_visible = is_visible
        self.is_collectible = is_collectible

        self.w = self.img.get_width()
        self.h = self.img.get_height()

        self.value = 1

    def set_visibility(self, status):
        self.is_visible = status

    def set_collectibility(self, status):
        self.is_collectible = status

    def activate(self):
        self.is_collectible = True
        self.is_visible = True

    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def draw(self):
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


def load_config():

    global OPENING_TEXT

    # Load opening text from disk.
    f = open('Open.txt')
    lines = f.readlines()
    f.close()

    # text_rect = text.get_rect()
    # text_rect.center_x = screen.get_rect().centerx
    # text_rect.center_y = screen.get_rect().centery

    # for i in lines:
    #     OPENING_TEXT = FONT_SM.render(i[:-1], True, WHITE)
    #     text_rect.center_y += 50


# Make game objects

def setup():
    global student, platforms, background_objects, \
        belongings, teachers, admins, bad_students, \
        done, score, stage, inventory

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
    background_objects = [BackgroundObjects(950, 0, exit_img)]
    belongings = [Belongings(475, 300, laptop_img),
                  Belongings(475, 650, phone_img),
                  Belongings(25, 440, staffbadge_img),
                  Belongings(25, 210, card_img)]
    teachers = [OtherPeople(0, 411, teacher_img)]
    admins = [OtherPeople(0, 186, admin_img)]
    bad_students = [OtherPeople(125, 301, bad_student_img)]
    inventory = []

    belongings[0].activate()

    # Game stats
    score = 0

    # game loop
    done = False
    stage = START


# Initialize variables
setup()
load_config()

while not done:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:

            if stage == START:

                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    
            if stage == PLAYING:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                     student.jump(platforms)

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_RIGHT]:
             student.move(student.speed)
        elif pressed[pygame.K_LEFT]:
             student.move(-student.speed)
        else:
             student.stop()

    # game logic
    # player.update(ground, platforms)
    if stage == PLAYING:
        student.update(platforms, teachers, admins, bad_students, belongings, inventory)

        for t in teachers:
            t.update(platforms)

        for a in admins:
            a.update(platforms)

        for b in bad_students:
            b.update(platforms)    

 # Messages
    START_TEXT = FONT_SM.render("Press space to start.", True, WHITE)
    SCORE = FONT_SM.render("Score:" + format(score), True, WHITE)

    # Draw game objects on-screen.
    if stage == START:
        screen.fill(DARKER_GREY)
        screen.blit(OPENING_TEXT, [295, 200])

    elif stage == PLAYING:
        screen.fill(DARKER_GREY)

        for b in background_objects:
            b.draw()

        for p in platforms:
            p.draw()

        for b in belongings:
            if b.is_visible:
                b.draw()

        for a in admins:
            a.draw()

        for t in teachers:
            t.draw()

        for b in bad_students:
            b.draw()

        for i in inventory:
            i.draw()

        student.draw()

        screen.blit(SCORE, [0, 0])

    # update screen
    pygame.display.update()
    clock.tick(FPS)

# close window on quit
pygame.quit()

