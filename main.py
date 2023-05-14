import time
import os
import random

import pygame as pg
import neat as nt

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMG = [pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird1.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird2.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","base.png")))
BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs","bg.png")))
