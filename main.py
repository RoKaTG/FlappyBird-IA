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

        if distance < 0 or self.y < self.height - 15:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = min(self.tilt + 10, self.MAX_ROTATION)
        else:
            if self.tilt > -self.MAX_ROTATION:
                self.tilt = max(self.tilt - 10, -self.MAX_ROTATION)

    def draw(self,windows):
        self.img_count = self.img_count + 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMG[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMG[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMG[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMG[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMG[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMG[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        windows.blit(rotated_image, new_rect.topleft)

class Pipe:
    VELOCITY = 0




def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pg.display.update()

def main():
    pg.init()
    win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pg.time.Clock()
    bird = Bird(100, 300)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bird.jump()

        bird.move()
        draw_window(win, bird)
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
        main()