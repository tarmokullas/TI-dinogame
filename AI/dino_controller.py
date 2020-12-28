import pygame

from .Dinosaur import Dinosaur
from .Population import *

import sys
import os
sys.path.append(os.pardir)

class DinoController:
    def __init__(self, dino_x, dino_y, human, imgJump, imgDuck, num_dino=1, num_best_dino=1, threshold=0.55,
                 scr_size=(600, 150), play_sound=True, mutation_rate=0.5, mutation_range=(0.8, 1.2), crossing_points=1):
        self.dino_x, self.dino_y = dino_x, dino_y
        self.num_dino = num_dino
        self.imgJump, self.imgDuck = imgJump, imgDuck
        self.play_sound = play_sound
        self.dinos = [Dinosaur() for _ in range(self.num_dino)]
        if not human:
            self.generation = Population(pop_size=num_dino, best_candidates_size=num_best_dino, mutation_rate=mutation_rate,
                                         mutation_range=mutation_range, crossing_points=crossing_points)
            self.threshold = threshold
        (self.width, self.height) = scr_size

    def loadDinos(self, dino_weights):
        self.generation.loadPopulation(dino_weights)

    def loadSounds(self, die_sound, jump_sound):
        self.die_sound = die_sound
        self.jump_sound = jump_sound

    def update(self, status, score):
        for i in range(len(self.dinos)):
            if not self.dinos[i].isDead:
                self.dinos[i].isDead = status[i]
                self.dinos[i].score = score
                self.dinos[i].update(self.die_sound)

    def draw(self, screen, last_dead):
        for dino in self.dinos:
            dino.draw(screen, last_dead)

    # movements
    def moveHuman(self):
        dino = self.dinos[0]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.run()

    def moveAI(self, input):
        movements = self.generation.get_outputs(input)
        for i in range(len(movements)):
            dino = self.dinos[i]
            if dino.isDead:
                continue

            jump, duck = movements[i]
            if jump >= self.threshold:
                dino.jump()
            if duck >= self.threshold:
                dino.duck()
            else:
                dino.run()

            self.generation.population[i].fitness = self.dinos[i].score

    def nextGeneration(self):
        self.dinos = [Dinosaur() for _ in range(self.num_dino)]
        self.generation.keep_best_candidates()
        self.generation.generate_new_population()

    def getBestCandidatesData(self):
        if not self.generation.get_best_candidates():
            self.generation.keep_best_candidates()
        candidates = self.generation.get_best_candidates()
        weights = []
        for c in candidates:
            weight = c.getData()
            weights.append(weight)
        return weights
