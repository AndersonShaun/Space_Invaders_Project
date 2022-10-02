import pygame as pg
from pygame.sprite import Sprite, Group
from PIL import Image


class Barrier(Sprite):
    color = 255, 0, 0
    black = 0, 0, 0
    im = Image.open('images/bunker.png').convert('RGB')

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.health = 8
        self.alpha_value = 255

        self.image = pg.image.load('images/bunker.png')
        self.rect = self.image.get_rect()

        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def hit(self):
        raw_str = pg.image.tostring(self.image, "RGBA", False)
        image = Image.frombytes("RGBA", self.image.get_size(), raw_str)
        image_copy = image.copy()
        image_copy.putalpha(self.alpha_value // 2)
        image.paste(image_copy, image)

        # Change transparency of barrier when hit
        self.image = pg.image.fromstring(image.tobytes(), self.image.get_size(), "RGBA")
        self.alpha_value //= 2

        self.update()

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.barriers = Group()
        self.ship_lasers = game.ship_lasers.lasers
        self.alien_lasers = game.alien_lasers.lasers
        self.create_barriers()

    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        for i in range(4):
            barrier = Barrier(game=self.game)
            barrier_x = i * 2 * width + 1.5 * width
            barrier_y = height
            barrier_top = 548
            barrier.rect.x = barrier_x
            barrier.rect.y = barrier_y
            barrier.rect.top = barrier_top
            self.barriers.add(barrier)

    def hit(self, barrier):
        barrier.health -= 1
        if barrier.health <= 0:
            barrier.kill()
        barrier.hit()
    
    def reset(self):
        self.barriers.empty()
        self.create_barriers()

    def update(self):
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()
