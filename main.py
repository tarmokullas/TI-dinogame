import os
import pickle
import time

import neat
import pygame
import random

from Dino import Dino

pygame.init()
pygame.font.init()

# Global variables
global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT, GROUND_TICKNESS, MIN_GAP, MAX_GAP, STAT_FONT

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 1000, 400
GROUND_TICKNESS = 100
GROUND_HEIGHT = WIN_HEIGHT - GROUND_TICKNESS
STAT_FONT = pygame.font.SysFont("calibri", 20)
gen = 0
best_score = 0
all_time_best_score = 0
läbitud_takistus = []

# Takistuste pildid
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
            self.y = GROUND_HEIGHT - 80
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
            global läbitud_takistus
            läbitud_takistus.append(obstacles.pop(0))

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

    global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT
    WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 1000, 400

    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
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

    load_all_time_best_score()

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
                rnd4 = random.randint(1, 5)  # Kui on 1, siis tuleb lind

                obstacles.append(Obstacle(rnd1, rnd2, rnd3, rnd4))

        obs_id = 0
        if len(dinos) > 0:
            if len(obstacles) > 1 and dinos[0].x > obstacles[0].x + obstacles[0].obs_width:
                obs_id = 1
        else:
            run = False
            game_over_overlay(window)
            break

        for x, dino in enumerate(dinos):

            dist_to_obs = obstacles[obs_id].x - (dino.x + dino.dino_rect.width)
            obs_width = obstacles[obs_id].obs_width
            obs_height = obstacles[obs_id].obs_height
            obs_bottom_y = obstacles[obs_id].y + obs_height
            dino_y = dino.y

            if obstacles[obs_id].isBird:
                obs_width = obstacles[obs_id].obs_width
                obs_height = obstacles[obs_id].obs_height
                obs_bottom_y = obstacles[obs_id].y + obs_height
                dino_y = dino.y
            else:
                obs_width = obstacles[obs_id].obs_width
                obs_height = obstacles[obs_id].obs_height
                obs_bottom_y = 0
                dino_y = dino.y

            dino_pos = 0
            if dino.isRunning:
                dino_pos = 0
            if dino.isJumping:
                dino_pos = 1
            if dino.isDucking:
                dino_pos = 2

            output = nets[x].activate((GAME_SPEED, dist_to_obs, obs_width, obs_height, obs_bottom_y, dino_pos))

            if output[0] < 0.5:
                dino.jump()
            if output[1] < 0.5:
                dino.duck()
            if output[2] < 0.5:
                dino.run()

        for x, dino in enumerate(dinos):
            if not dino.dino_rect.colliderect(obstacles[obs_id].obs_rect):
                ge[x].fitness += 10  # Kui kokkupõrget pole, siis suurendada fitness
                if len(läbitud_takistus) > 0:
                    ge[x].fitness += 20  # Läbitud takistus annab fitnessi
                    läbitud_takistus.pop()
                if obstacles[obs_id].isBird and dino.ducking():
                    ge[x].fitness += 5

            else:
                ge[x].fitness -= 100  # Kui kokkupõrge, siis vähenda fitness

                if not obstacles[obs_id].isBird:  # Kui takistus on kaktus
                    if dino.isJumping:
                        ge[x].fitness += 15  # Kui dinasaurus põrkab hüppel kokku, siis suurenda fitnessi
                    elif dino.dino_rect.height == dino.DINO_HEIGHT:
                        ge[x].fitness += 15  # Kui dinasaurus ei kummarda, siis suurenda fitnessi

                else: # Kui takistus on lind
                    if dino.x > obstacles[obs_id].x:
                        ge[x].fitness += 20  # Kui dinosaurus põrkab kokku linnuga, sest unduckib liiga vara, siis suurenda fitnessi
                    if dino.isJumping or dino.isRunning:
                        ge[x].fitness -= 75  # Kui dinosaurus põrkab kokku linnuga, sest jookseb või hüppab, siis vähenda ftinessi

                dinos.pop(x)
                nets.pop(x)
                ge.pop(x)

        score()

        draw(window, dinos, obstacles, gen, len(dinos), best_score, all_time_best_score)  # Kõikide elementide kuvamine

    WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 600, 600
    pygame.display.set_mode(WIN_SIZE)


def human_plays():

    global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT
    WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 1000, 400

    window = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Dino Run AI")
    clock = pygame.time.Clock()

    global obstacles, GAME_SPEED, MIN_GAP, MAX_GAP, points, gen

    gen += 1
    GAME_SPEED = 8
    MIN_GAP = 280
    MAX_GAP = 800
    points = 0

    load_all_time_best_score()

    obstacles = []

    dino = Dino(100, GROUND_HEIGHT - 60)

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
                    dino.jump()
                    pass
                if event.key == pygame.K_DOWN:
                    dino.duck()
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.run()
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
                rnd4 = random.randint(1, 5)  # Kui on 1, siis tuleb lind

                obstacles.append(Obstacle(rnd1, rnd2, rnd3, rnd4))

        score()

        draw2(window, dino, obstacles, best_score, all_time_best_score)  # Kõikide elementide kuvamine

        # Kui dino läheb takistuse pihta on mäng läbi
        for obs in obstacles:
            if dino.dino_rect.colliderect(obs.obs_rect):
                game_over_overlay(window)
                run = False

    WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 600, 600
    pygame.display.set_mode(WIN_SIZE)


def game_over_overlay(window):
    game_over_img = pygame.image.load(os.path.join("Assets/Other", "GameOver.png"))
    img_rect = game_over_img.get_rect()
    window.blit(game_over_img, (WIN_WIDTH/2 - img_rect.width/2, WIN_HEIGHT/2 - img_rect.height/2))
    pygame.display.update()
    pygame.time.wait(2000)


def draw(win, dinos, obstacles, gen, alive, best_score, all_time_best_score):
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

    text = STAT_FONT.render("ALL-TIME BEST: " + str(all_time_best_score), 1, (0, 0, 0))
    win.blit(text, (20, 110))

    for dino in dinos:
        dino.draw(win)  # Dinosauruse joonistamine

    # Takistuste joonistamine
    for obs in obstacles:
        obs.draw(win)

    pygame.display.update()  # Akna uuendamine


def draw2(win, dino, obstacles, best_score, all_time_best_score):
    pygame.draw.rect(win, (240, 240, 240), (0, 0, WIN_WIDTH, WIN_HEIGHT))  # Tausta joonistamine
    pygame.draw.rect(win, (100, 100, 100), (0, GROUND_HEIGHT, WIN_WIDTH, GROUND_TICKNESS))  # Maapinna joonistamine

    text = STAT_FONT.render("SCORE: " + str(points), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 20))

    text = STAT_FONT.render("GAMESPEED: " + str(GAME_SPEED), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 50))

    text = STAT_FONT.render("BESTSCORE: " + str(best_score), 1, (0, 0, 0))
    win.blit(text, (20, 20))

    text = STAT_FONT.render("ALL-TIME BEST: " + str(all_time_best_score), 1, (0, 0, 0))
    win.blit(text, (20, 50))

    dino.draw(win)  # Dinosauruse joonistamine

    # Takistuste joonistamine
    for obs in obstacles:
        obs.draw(win)

    pygame.display.update()  # Akna uuendamine


# Puktide suurendamine
def score():
    global points, GAME_SPEED, MIN_GAP, MAX_GAP, best_score, all_time_best_score
    if GAME_SPEED != 0:
        points += 1
        if points % 250 == 0:
            GAME_SPEED += 1  # Suurenda mängukiirust
            MIN_GAP += 60  # Suurenda minimaalset takistuste vahet
            MAX_GAP += 70  # Suurenda maksimaalset takistuste vahet
        if points > best_score:
            best_score = points
            if best_score > all_time_best_score:
                all_time_best_score = best_score
                save_all_time_best_score()


def run_new_game():
    global gen, best_score
    gen = 0
    best_score = 0

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 10)

    # Salvestab parima genoomi andmed faili
    save_best_genome(winner)


def save_all_time_best_score(all_time_best_score_path="all_time_best_score.txt"):
    with open(all_time_best_score_path, "w") as f:
        f.write(str(all_time_best_score))
        f.close()


def load_all_time_best_score(all_time_best_score_path="all_time_best_score.txt"):
    if os.path.exists(all_time_best_score_path):
        with open(all_time_best_score_path, "r") as f:
            global all_time_best_score
            all_time_best_score = int(f.readline())
            f.close()
        print("All-time best score loaded from", all_time_best_score_path)


def save_best_genome(best_genome, best_genome_path="best_genome.pkl"):
    with open(best_genome_path, "wb") as f:
        pickle.dump(best_genome, f)
        f.close()
    print("Saved best genome to", best_genome_path)


# https://stackoverflow.com/questions/61365668/applying-saved-neat-python-genome-to-test-environment-after-training
def run_best_genome(config_path="config-feedforward.txt", best_genome_path="best_genome.pkl"):
    global gen, best_score
    gen = 0
    best_score = 0

    # Load required NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(best_genome_path, "rb") as f:
        genome = pickle.load(f)
        f.close()

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    main(genomes, config)


def main_menu():

    WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = (600, 600)

    window = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Dino Run AI")

    title_font = pygame.font.SysFont('Corbel', 60)
    title_text = title_font.render('Dino Run Game', True, (50, 50, 50))

    authors_font = pygame.font.SysFont('Corbel', 20)
    authors_text = authors_font.render('Made by Tarmo Kullas & Mikko Maran', True, (50, 50, 50))

    button_font = pygame.font.SysFont('Corbel', 35)
    quit_text = button_font.render('Quit', True, (50, 50, 50))
    best_genome_text = button_font.render('Run all-time best genome', True, (50, 50, 50))
    new_population_text = button_font.render('Run game with new population', True, (50, 50, 50))
    play_yourself_text = button_font.render('Play it yourself!', True, (50, 50, 50))

    button_texts = [play_yourself_text, new_population_text, best_genome_text, quit_text]

    while True:

        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Hiire vajutuste jälgimine
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # Nuppude vajutamine
                for i, button_text in enumerate(button_texts):
                    button_width = button_text.get_rect().width + 50
                    button_height = 50
                    button_x = WIN_WIDTH / 2 - button_width / 2
                    button_y = 250 + i * 75

                    # Nuppude vajutamine
                    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
                        # Inimene mängib ise
                        if i == 0:
                            human_plays()
                        # Run game with new population nupu vajutamine
                        if i == 1:
                            run_new_game()
                        # Run all-time best genome nupu vajutamine
                        elif i == 2:
                            run_best_genome()
                        # Quit nupu vajutamine
                        elif i == 3:
                            pygame.quit()
                            quit()
        # Ekraani taustavärv
        window.fill((240, 240, 240))

        # Mängu pealkiri
        title_rect = title_text.get_rect(center=(WIN_WIDTH/2, 120))
        window.blit(title_text, title_rect)

        # Autorid
        authors_rect = title_text.get_rect(center=(WIN_WIDTH/2 + 25, 190))
        window.blit(authors_text, authors_rect)

        # Nuppude kuvamine
        for i, button_text in enumerate(button_texts):
            button_width = button_text.get_rect().width + 50
            button_height = 50
            button_x = WIN_WIDTH/2 - button_width/2
            button_y = 250 + i * 75
            draw_button(window, button_text, button_width, button_height, button_x, button_y)

        pygame.display.update()


def draw_button(window, text, button_width, button_height, button_x, button_y):
    # Nupu kuvamine
    pygame.draw.rect(window, (200, 200, 200), [button_x, button_y, button_width, button_height])

    # Kiri nupul
    text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
    window.blit(text, text_rect)


if __name__ == "__main__":
    main_menu()
