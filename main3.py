import os
import neat
import pygame
import random

from Dino import Dino

pygame.init()
pygame.font.init()

# Global variables
global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT, GROUND_TICKNESS, MIN_GAP, MAX_GAP, STAT_FONT

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 400
GROUND_TICKNESS = 100
GROUND_HEIGHT = WIN_HEIGHT - GROUND_TICKNESS
STAT_FONT = pygame.font.SysFont("calibri", 20)
gen = 0
best_score = 0


SMALL_CACTUSES = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                  pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                  pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUSES = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                  pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                  pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRDS = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
         pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

small_cactus_img = [pygame.transform.scale(img, (30 * (i + 1), 20)) for i, img in enumerate(SMALL_CACTUSES)]
large_cactus_img = [pygame.transform.scale(img, (30 * (i + 1), 45)) for i, img in enumerate(LARGE_CACTUSES)]
bird_img = [pygame.transform.scale(img, (30, 30)) for img in BIRDS]


class Obstacle:
    OBS_WIDTHS = [30, 60, 90]
    OBS_HEIGTHS = [20, 45]
    OBS_COLOR = [200, 0, 0]

    x = WIN_WIDTH
    y = 0
    obs_width = 0
    obs_height = 0

    step = 0
    isBird = False

    def __init__(self, rnd1, rnd2, rnd3, rnd4):

        self.x = rnd3  # Kaugus eelmisest takistusest

        if rnd4 == 1:  # Siis on lind
            self.y = GROUND_HEIGHT - 75
            self.obs_width = 30
            self.obs_height = 30
            self.obs_rect = pygame.Rect(self.x, self.y, self.obs_width, self.obs_height)
            self.image = bird_img[0]
            self.isBird = True
        else:  # Muul juhul tavaline takistus
            self.obs_width = self.OBS_WIDTHS[rnd1]
            self.obs_height = self.OBS_HEIGTHS[rnd2]
            self.y = GROUND_HEIGHT - self.obs_height
            self.obs_rect = pygame.Rect(self.x, self.y, self.obs_width, self.obs_height)
            if rnd2 == 0:
                self.image = small_cactus_img[rnd1]
            else:
                self.image = large_cactus_img[rnd1]

    def move(self):
        self.x -= GAME_SPEED
        self.obs_rect = pygame.Rect(self.x, self.y, self.obs_width, self.obs_height)
        if self.x < 0 - self.obs_width:
            obstacles.pop(0)

    def bird_flying(self):
        if self.step == 20:
            self.step = 0
        self.step += 1
        if self.step < 10:
            self.image = bird_img[0]
        else:
            self.image = bird_img[1]

    def draw(self, display):
        if self.isBird:
            self.bird_flying()
        self.move()
        display.blit(self.image, (self.obs_rect.x, self.obs_rect.y))


def main(genomes, config):
    nets = []
    ge = []
    dinos = []

    for __, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(100, GROUND_HEIGHT - 60))
        g.fitness = 0
        ge.append(g)

    window = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Dino Run AI")
    clock = pygame.time.Clock()

    global obstacles, GAME_SPEED, MIN_GAP, MAX_GAP, points, gen

    gen += 1
    GAME_SPEED = 8
    MIN_GAP = 280
    MAX_GAP = 800
    points = 0

    obstacles = []

    run = True
    while run:

        clock.tick(60)  # Mängu fps

        # Mängu evendid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # dino.jump()
                    pass
                if event.key == pygame.K_DOWN:
                    # dino.duck()
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    # dino.move()
                    pass

        # Takistuste genereerimine
        if len(obstacles) < 4:
            for i in range(4 - len(obstacles)):

                rnd1 = random.randint(0, 2)  # Sellega määratakse takistuse laius
                rnd2 = random.randint(0, 1)  # Sellega määratakse takistuse kõrgus
                if len(obstacles) > 0:
                    rnd3 = random.randint(obstacles[len(obstacles) - 1].x + MIN_GAP, obstacles[
                        len(obstacles) - 1].x + MAX_GAP)  # Takistuse kaugus eelmisest takistusest
                else:
                    rnd3 = WIN_WIDTH  # Kõige esimene takistus paigutatakse kohe kuva äärde
                rnd4 = random.randint(0, 5)  # Kui on 1, siis tuleb lind

                obstacles.append(Obstacle(rnd1, rnd2, rnd3, rnd4))

        obs_id = 0
        if len(dinos) > 0:
            if len(obstacles) > 1 and dinos[0].x > obstacles[0].x + obstacles[0].obs_width:
                obs_id = 1
        else:
            run = False
            break

        for x, dino in enumerate(dinos):

            dist_to_obs = obstacles[obs_id].x - (dino.x + dino.dino_rect.width)
            obs_width = obstacles[obs_id].obs_width
            obs_height = obstacles[obs_id].obs_height
            obs_bottom_y = obstacles[obs_id].y + obs_height
            dino_y = dino.y

            output = nets[x].activate((GAME_SPEED, dist_to_obs, obs_width, obs_height, obs_bottom_y, dino_y))

            if output[0] == 1:
                dino.jump()
            if output[1] == 1:
                dino.duck()

        for obs in obstacles:
            for x, dino in enumerate(dinos):
                if dino.dino_rect.colliderect(obs.obs_rect):
                    ge[x].fitness -= 5
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        score()
        for g in ge:
            g.fitness += 2

        draw(window, dinos, obstacles, gen, len(dinos), best_score)  # Kõikide elementide kuvamine


def draw(win, dinos, obstacles, gen, alive, best_score):
    pygame.draw.rect(win, (240, 240, 240), (0, 0, WIN_WIDTH, WIN_HEIGHT))  # Tausta joonistamine
    pygame.draw.rect(win, (100, 100, 100), (0, GROUND_HEIGHT, WIN_WIDTH, GROUND_TICKNESS))  # Maapinna joonistamine

    text = STAT_FONT.render("SCORE: " + str(points), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 20))

    text = STAT_FONT.render("GAMESPEED: " + str(GAME_SPEED), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 50))

    text = STAT_FONT.render("GEN: " + str(gen), 1, (0, 0, 0))
    win.blit(text, (20, 20))

    text = STAT_FONT.render("ALIVE: " + str(alive), 1, (0, 0, 0))
    win.blit(text, (20, 50))

    text = STAT_FONT.render("BESTSCORE: " + str(best_score), 1, (0, 0, 0))
    win.blit(text, (20, 80))

    for dino in dinos:
        dino.draw(win)  # Dinosauruse joonistamine

    # Takistuste joonistamine
    for obs in obstacles:
        obs.draw(win)

    pygame.display.update()  # Akna uuendamine


# Puktide suurendamine
def score():
    global points, GAME_SPEED, MIN_GAP, MAX_GAP, best_score
    if GAME_SPEED != 0:
        points += 1
        if points % 250 == 0:
            GAME_SPEED += 1  # Suurenda mängukiirust
            MIN_GAP += 40  # Suurenda minimaalset takistuste vahet
            MAX_GAP += 45  # Suurenda maksimaalset takistuste vahet
        if points > best_score:
            best_score = points


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
