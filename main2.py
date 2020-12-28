
import pygame
import random
pygame.init()
pygame.font.init()

# Global variables
global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT, GROUND_TICKNESS, MIN_GAP, MAX_GAP, STAT_FONT

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 400
GROUND_TICKNESS = 100
GROUND_HEIGHT = WIN_HEIGHT - GROUND_TICKNESS
GAME_SPEED = 8
MIN_GAP = 280
MAX_GAP = 800
STAT_FONT = pygame.font.SysFont("calibri", 20)
points = 0

def main():

    global obstacles

    window = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Dino Run AI")

    clock = pygame.time.Clock()

    dino = Dino(100, GROUND_HEIGHT - 60)
    obstacles = []

    run = True
    while run:

        clock.tick(60) # Mängu fps

        # Mängu evendid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.move()


        # Takistuste genereerimine
        if len(obstacles) < 4:
            for i in range(4-len(obstacles)):

                rnd1 = random.randint(0, 2) # Sellega määratakse takistuse laius
                rnd2 = random.randint(0, 1) # Sellega määratakse takistuse kõrgus
                if len(obstacles) > 0:
                    rnd3 = random.randint(obstacles[len(obstacles)-1].x+MIN_GAP, obstacles[len(obstacles)-1].x+MAX_GAP) # Takistuse kaugus eelmisest takistusest
                else:
                    rnd3 = WIN_WIDTH # Kõige esimene takistus paigutatakse kohe kuva äärde
                rnd4 = random.randint(0, 5) # Kui on 1, siis tuleb lind

                obstacles.append(Obstacle(rnd1, rnd2, rnd3, rnd4))

        score()
        draw(window, dino, obstacles) # Kõikide elementide kuvamine

    pygame.quit()
    quit()

def draw(win, dino, obstacles):

    pygame.draw.rect(win, (240, 240, 240), (0, 0, WIN_WIDTH, WIN_HEIGHT)) # Tausta joonistamine
    pygame.draw.rect(win, (100, 100, 100), (0, GROUND_HEIGHT, WIN_WIDTH, GROUND_TICKNESS)) # Maapinna joonistamine

    text = STAT_FONT.render("SCORE: " + str(points), 1,(0,0,0))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 20))

    text = STAT_FONT.render("GAMESPEED: " + str(GAME_SPEED), 1,(0,0,0))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 50))

    dino.draw(win) # Dinosauruse joonistamine

    # Takistuste joonistamine
    for obs in obstacles:
        obs.draw(win)
        if dino.dino_rect.colliderect(obs.obs_rect):
            pygame.quit()

    pygame.display.update() # Akna uuendamine

# Puktide suurendamine
def score():
    global points, GAME_SPEED, MIN_GAP, MAX_GAP
    points += 1
    if points % 250 == 0:
        GAME_SPEED += 1 # Suurenda mängukiirust
        MIN_GAP += 40 # Suurenda minimaalset takistuste vahet
        MAX_GAP += 45 # Suurenda maksimaalset takistuste vahet

class Dino:

    DINO_WIDTH = 40
    DINO_HEIGHT = 60
    DINO_COLOR = (30, 200, 50)

    jumpSpeed = 15
    jumpSteps = jumpSpeed
    isJump = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.dino_rect = pygame.Rect(self.x, self.y, self.DINO_WIDTH, self.DINO_HEIGHT)

    def move(self):
        self.dino_rect = pygame.Rect(self.x, self.y, self.DINO_WIDTH, self.DINO_HEIGHT)

    def duck(self):
        self.dino_rect = pygame.Rect(self.x, self.y+20, self.DINO_HEIGHT, self.DINO_WIDTH)

    def jump(self):
        self.isJump = True

    def jumper(self):

        if self.jumpSteps >= -self.jumpSpeed:
            neg = 1
            if self.jumpSteps < 0:
                neg = -1
            self.y -= (self.jumpSteps ** 2) * 0.05 * neg
            self.jumpSteps -= 1
        else:
            self.jumpSteps = self.jumpSpeed
            self.isJump = False

        self.dino_rect = pygame.Rect(self.x, self.y, self.DINO_WIDTH, self.DINO_HEIGHT)

    def draw(self, display):
        if self.isJump:
            self.jumper()
        pygame.draw.rect(display, self.DINO_COLOR, self.dino_rect)

class Obstacle:

    OBS_WIDTHS = [30, 40, 50]
    OBS_HEIGTHS = [20, 45]
    OBS_COLOR = [200,0,0]

    x = WIN_WIDTH
    y = 0
    obs_width = 0
    obs_height = 0

    def __init__(self, rnd1, rnd2, rnd3, rnd4):

        self.x = rnd3 # Kaugus eelmisest takistusest

        if rnd4 == 1: # Siis on lind
            self.y = GROUND_HEIGHT - 75
            self.obs_width = 30
            self.obs_height = 30
            self.obs_rect = pygame.Rect(self.x, self.y, self.obs_width, self.obs_height)
        else: # Muul juhul tavaline takistus
            self.obs_width = self.OBS_WIDTHS[rnd1]
            self.obs_height = self.OBS_HEIGTHS[rnd2]
            self.y = GROUND_HEIGHT - self.obs_height
            self.obs_rect = pygame.Rect(self.x, self.y, self.obs_width, self.obs_height)

    def move(self):
        self.x -= GAME_SPEED
        self.obs_rect = pygame.Rect(self.x, self.y, self.obs_width, self.obs_height)
        if self.x < 0-self.obs_width:
            obstacles.pop(0)

    def draw(self, display):
        self.move()
        pygame.draw.rect(display, self.OBS_COLOR, self.obs_rect)

main()