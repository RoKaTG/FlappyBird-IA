import time
import os
import random

import pygame as pg
import neat as nt

WIN_WIDTH = 600
WIN_HEIGHT = 800


BIRD_IMG = [pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird1.png"))),
            pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird2.png"))),
            pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","base.png")))
BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","bg.png")))


class Bird:
    IMG = BIRD_IMG
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMG[0]

    def jump(self):
        self.velocity = -10
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count = self.tick_count + 1

        distance = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if distance >= 16:
            distance = 16

        if distance < 0:
            distance = distance - 5

        self.y = self.y + distance

        if distance < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.tilt + 10

        if distance >= 16 or self.y >= self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.tilt - 10