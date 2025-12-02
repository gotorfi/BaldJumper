#DATA ABOUT MAP
from const import *
import os
import pygame
map = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,53,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,8,0,0,0,8,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,8,0,55,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,55,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,55,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,4,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,2,2,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,2,2,2,0,0,0,0,0,0,0,0,0,4,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0],
[3,3,1,1,1,1,1,1,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,2,2,1,0,0,0,0,0,0,0,0,0,0],
[3,3,3,3,1,1,1,1,1,1,1,1,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0],
[3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
[3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,2,2,1,1,1,1,1,1,1,1,3,3,0,0,0,0,0,0,0,0,0,0],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,2,0,0,54,0,0,2,1,1,1,1,1,1,1,1,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,2,2,2,2,2,1,1,1,1,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]





class Map:
    def __init__(self, screen):
        print(screen)
        self.squares = map
        self._create()
        self.screen = screen

        self.assets = {
            1: pygame.image.load(os.path.join("ASSET/OBJ/dirt.png")).convert_alpha(),
            2: pygame.image.load(os.path.join("ASSET/OBJ/grass.png")).convert_alpha(),
            3: pygame.image.load(os.path.join("ASSET/OBJ/stone.png")).convert_alpha(),
            4: pygame.image.load(os.path.join("ASSET/OBJ/platform.png")).convert_alpha(),
            8: pygame.image.load(os.path.join("ASSET/OBJ/saw.png")).convert_alpha(),
            7: pygame.image.load(os.path.join("ASSET/OBJ/spike.png")).convert_alpha(),
            8: pygame.image.load(os.path.join("ASSET/OBJ/saw.png")).convert_alpha(),
            55: pygame.image.load(os.path.join("ASSET/OBJ/star.png")).convert_alpha(),
            54: pygame.image.load(os.path.join("ASSET/OBJ/startflag1.png")).convert_alpha(),
            53: pygame.image.load(os.path.join("ASSET/OBJ/startflag1.png")).convert_alpha()
        }
        self._scaled_cache = {}
        self._last_size = None

        self.draw(screen)

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col, map[row][col])
    def restore(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col, 0)
    def _IsValid(self):
        stars = 0
        flags = 0
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.value == 55:
                    stars += 1
                if square.value == 53 or square.value == 54:
                    flags += 1
        if stars == 3 and flags == 2:
            return True
        return False
    def draw(self, screen, GridSizee=-1):
        map = self.squares

        size = GridSize if GridSizee == -1 else GridSizee
        size = max(1, int(size))

        if self._last_size != size:
            self._scaled_cache = {}
            for val, surf in self.assets.items():
                self._scaled_cache[val] = pygame.transform.smoothscale(surf, (size, size))
            self._last_size = size


        target = max(WIDTH, HEIGHT)
        img = pygame.image.load("ASSET/BG/mainbg.png")
        scaled = pygame.transform.smoothscale(img, (target, int(target / 1.5)))
        self.screen.blit(scaled, (0, 0))


        for row in map:
            for square in row:
                v = square.value
                if v != 0 and v != 9:
                    tile_img = self._scaled_cache.get(v)
                    if tile_img:
                        screen.blit(tile_img, (square.col * size, square.row * size))
    def load_from_list(self, grid):
        if not hasattr(self, "squares") or not self.squares:
            return

        for r, row in enumerate(grid):
            if r >= len(self.squares):
                break
            for c, val in enumerate(row):
                if c >= len(self.squares[r]):
                    break
                self.squares[r][c].value = val                    


class Square:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

class AnimatedSquare(Square):
    def __init__(self, row, col, frames, speed):
        super().__init__(row, col)
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.speed:
            self.counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
