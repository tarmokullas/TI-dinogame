
import pygame
import random
pygame.init()

# Global variables
global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT, GROUND_TICKNESS, GROUND_HEIGHT, GAME_SPEED, MIN_GAP, MAX_GAP

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 400
GROUND_TICKNESS = 100
GROUND_HEIGHT = WIN_HEIGHT - GROUND_TICKNESS
GAME_SPEED = 8
MIN_GAP = 280
MAX_GAP = 800

def main():

    global obstacles, points

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
                if event.key == pygame.K_SPACE:
                    dino.jump()

        # Takistuste genereerimine
        if len(obstacles) < 4:
            for i in range(4-len(obstacles)):
                rnd1 = random.randint(0, 2) # Sellega määratakse takistuse laius
                rnd2 = random.randint(0, 1) # Sellega määratakse takistuse kõrgus
                if len(obstacles) > 1:
                    rnd3 = random.randint(obstacles[len(obstacles)-1].x+MIN_GAP, obstacles[len(obstacles)-1].x+MAX_GAP) # Takistuse kaugus eelmisest takistusest
                else:
                    rnd3 = WIN_WIDTH # Kõige esimene takistus paigutatakse kohe kuva äärde
                obstacles.append(Obstacle(rnd1, rnd2, rnd3))

        draw(window, dino, obstacles) # Kõikide elementide kuvamine

    pygame.quit()
    quit()

def draw(win, dino, obstacles):

    pygame.draw.rect(win, (240, 240, 240), (0, 0, WIN_WIDTH, WIN_HEIGHT)) # Tausta joonistamine
    pygame.draw.rect(win, (100, 100, 100), (0, GROUND_HEIGHT, WIN_WIDTH, GROUND_TICKNESS)) # Maapinna joonistamine

    dino.draw(win) # Dinosauruse joonistamine

    # Takistuste joonistamine
    for obs in obstacles:
        obs.draw(win)
        if dino.dino_rect.colliderect(obs.obs_rect):
            pygame.quit()

    pygame.display.update() # Akna uuendamine

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

    def jump(self):
        self.isJump = True

    def jumper(self):
        if self.jumpSteps >= -self.jumpSpeed:

            neg = 1
            if self.jumpSteps < 0:
                neg = -1
            self.y -= (self.jumpSteps ** 2) * 0.1 * neg
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

    def __init__(self, rnd1, rnd2, rnd3):
        self.obs_width = self.OBS_WIDTHS[rnd1]
        self.obs_height = self.OBS_HEIGTHS[rnd2]
        self.x = rnd3
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