import pygame as pg
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector
from timer import Timer


class Ship(Sprite):
    ship_images = [pg.transform.rotozoom(pg.image.load(f'images/ship_resize.png'), 0, 1.0)]
    ship_explosion_images =\
        [pg.transform.rotozoom(pg.image.load(f'images/ship_explode_{n}.png'), 0, 1.0) for n in range(8)]

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.sb = game.scoreboard
        self.ships_left = game.settings.ship_limit  
        self.image = pg.image.load('images/ship_resize.png')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.posn = self.center_ship()    # posn is the centerx, bottom of the rect, not left, top
        self.vel = Vector()

        self.lasers = game.ship_lasers

        self.shooting = False
        self.lasers_attempted = 0

        self.timer_normal = Timer(image_list=Ship.ship_images)
        self.timer_explosion = Timer(image_list=Ship.ship_explosion_images, delay=100, is_loop=False)
        self.timer = self.timer_normal    

        self.dying = self.dead = False

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)

    def reset(self):
        if self.game.game_is_over:
            self.ships_left = self.settings.ship_limit
        self.vel = Vector()
        self.posn = self.center_ship()
        self.dying = self.dead = False
        self.lasers.reset()
        self.timer = self.timer_normal
        self.timer_explosion.reset()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y

    def hit(self):
        if not self.dying:
            print('SHIP IS HIT !!!!!!!!!!!!!!!!!!!!!')
            self.dying = True 
            self.timer = self.timer_explosion
            self.vel = Vector()

    def really_dead(self):
        self.ships_left -= 1
        print(f'Ship is dead! Only {self.ships_left} ships left')
        self.sb.decrement_lives(self)
        self.game.reset() if self.ships_left > 0 else self.game.game_over()

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.really_dead()
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(game=self.game, x=self.rect.centerx, y=self.rect.top)
        self.lasers.update()
        self.draw()

    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
