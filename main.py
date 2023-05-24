import time
import os
import random

import pygame as pg
import neat

pg.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800


BIRD_IMG = [pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird1.png"))),
            pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird2.png"))),
            pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","base.png")))
BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","bg.png")))

SCORE = pg.font.SysFont("TimesNewRoman", 50, bold = True, italic = False)

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

        distance = self.velocity * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2

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
    GENERATION = 175
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_T = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_B = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(35,400)
        self.top = self.height - self.PIPE_T.get_height()
        self.bottom = self.height + self.GENERATION

    def move(self):
        self.x = self.x - self.VELOCITY

    def draw(self, win):
        win.blit(self.PIPE_T, (self.x, self.top))
        win.blit(self.PIPE_B, (self.x, self.bottom))

    def get_rects(self):
        top_rect = self.PIPE_T.get_rect(topleft=(self.x, self.top))
        bottom_rect = self.PIPE_B.get_rect(topleft=(self.x, self.bottom))
        return top_rect, bottom_rect

def check_collision(bird, pipes):
    bird_rect = bird.img.get_rect(topleft=(bird.x, bird.y))

    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True

    return False

class Base:
    VELOCITY = 4
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 = self.x1 - self.VELOCITY
        self.x2 = self.x2 - self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = SCORE.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    base.draw(win)

    for bird in birds:
        bird.draw(win)
    pg.display.update()

def main(gen, config):
    pg.init()
    win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pg.time.Clock()

    birds = []
    pipes = [Pipe(600)]
    base = Base(730)

    score = 0

    network = []
    ge = []

    for _, g in gen:
        networks = neat.nn.FeedForwardNetwork.create(g, config)
        network.append((networks))
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)


    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_T.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = network[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()
        remove = []
        add_pipe = False

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if check_collision(bird, pipes):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    network.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.PIPE_T.get_width() < 0:
                remove.append(pipe)
            pipe.move()

        if add_pipe:
            score = score + 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in remove:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= WIN_HEIGHT - 40 or bird.y < 0:
                birds.pop(x)
                network.pop(x)
                ge.pop(x)

        draw_window(win, birds, pipes, base, score)
        clock.tick(30)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)

