import os

import pygame

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

run_img = [pygame.transform.scale(img, (40, 60)) for img in RUNNING]
jump_img = pygame.transform.scale(JUMPING, (40, 60))
duck_img = [pygame.transform.scale(img, (60, 40)) for img in DUCKING]


class Dino:

    DINO_WIDTH = 40
    DINO_HEIGHT = 60
    DINO_COLOR = (30, 200, 50)

    jumpSpeed = 15
    jumpSteps = jumpSpeed
    isJumping = False
    isDucking = False
    isRunning = True
    isDead = False

    step = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.dino_rect = pygame.Rect(self.x, self.y, self.DINO_WIDTH, self.DINO_HEIGHT)
        self.image = run_img[0]

    def jump(self):
        self.isJumping = True
        self.isDucking = False
        self.isRunning = False

    def duck(self):
        if not self.isJumping:
            self.isJumping = False
            self.isDucking = True
            self.isRunning = False

    def run(self):
        if not self.isJumping:
            self.isJumping = False
            self.isDucking = False
            self.isRunning = True

    def running(self):
        if self.step == 20:
            self.step = 0
        self.step += 1
        if self.step < 10:
            self.image = run_img[0]
        else:
            self.image = run_img[1]
        self.dino_rect = pygame.Rect(self.x, self.y, self.DINO_WIDTH, self.DINO_HEIGHT)

    def jumping(self):
        if self.jumpSteps >= -self.jumpSpeed:
            neg = 1
            if self.jumpSteps < 0:
                neg = -1
            self.y -= (self.jumpSteps ** 2) * 0.045 * neg
            self.jumpSteps -= 1
        else:
            self.jumpSteps = self.jumpSpeed
            self.isJumping = False
            self.run()
        self.dino_rect = pygame.Rect(self.x, self.y, self.DINO_WIDTH, self.DINO_HEIGHT)
        self.image = jump_img

    def ducking(self):
        if self.step == 20:
            self.step = 0
        self.step += 1
        if self.step < 10:
            self.image = duck_img[0]
        else:
            self.image = duck_img[1]
        self.dino_rect = pygame.Rect(self.x, self.y+20, self.DINO_HEIGHT, self.DINO_WIDTH)

    def draw(self, display):
        if self.isJumping:
            self.jumping()
        if self.isDucking:
            self.ducking()
        else:
            self.running()
        display.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
