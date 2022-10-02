import pygame as pg
from pygame.sprite import Sprite, Group, GroupSingle
from timer import Timer
from random import randint


class Alien(Sprite):

    alien_images_0 = [pg.image.load(f'images/alien_1_{n}.png') for n in range(2)]
    alien_images_1 = [pg.image.load(f'images/alien_2_{n}.png') for n in range(2)]
    alien_images_2 = [pg.image.load(f'images/alien_3_{n}.png') for n in range(2)]
    alien_images_3 = [pg.image.load(f'images/alien_4.png') for n in range(1)]

    alien_timers = {0: Timer(image_list=alien_images_0, delay=1000),
                    1: Timer(image_list=alien_images_1, delay=1000),
                    2: Timer(image_list=alien_images_2, delay=1000),
                    3: Timer(image_list=alien_images_3, delay=1000)}

    alien_explosion_images = [pg.image.load(f'images/explode{n}.png') for n in range(7)]
    ufo_explode_images = [pg.image.load(f'images/ufo_explode_{n}.png') for n in range(4)]

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/alien_1_0.png')
        self.rect = self.image.get_rect()
        self.points = game.settings.alien_points[type]

        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        
        self.dying = self.dead = False
                      
        self.timer_normal = Alien.alien_timers[type]              
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, is_loop=False)
        self.ufo_timer_explosion = Timer(image_list=Alien.ufo_explode_images, is_loop=False)
        self.timer = self.timer_normal                                    

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.type == 3:
            return self.rect.right >= screen_rect.right
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self, type):
        if not self.dying:
            self.dying = True
            if type == 3:
                self.timer = self.ufo_timer_explosion
                return
            self.timer = self.timer_explosion

    def update(self):
        if self.type == 3:
            if self.timer == self.ufo_timer_explosion and self.timer.is_expired():
                self.kill()
            settings = self.settings
            self.x += settings.alien_speed_factor * 2
            # print("This is unique for ufo")
            self.rect.x = self.x
            self.draw()
            return

        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Aliens:
    def __init__(self, game): 
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.ufo = GroupSingle()

        # self.ship_lasers = game.ship.lasers.lasers    # a laser Group

        self.ship_lasers = game.ship_lasers.lasers    # a laser Group
        self.aliens_lasers = game.alien_lasers

        self.barriers = game.barriers

        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.shoot_requests = 0
        self.ufo_spawn_requests = 0

        self.active_ufo = False
        self.ship = game.ship
        self.speed_check_1 = True
        self.speed_check_2 = True
        self.create_fleet()

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.6 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (6 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1.5 * alien_height))
        return number_rows

    def reset(self):
        self.aliens.empty()
        self.ufo.empty()
        self.sound.ufo_hover_stop()
        self.active_ufo = False
        self.create_fleet()
        self.aliens_lasers.reset()
        self.ufo_spawn_requests = 0
        self.shoot_requests = 0
        self.speed_check_1 = True
        self.speed_check_2 = True

    def create_alien(self, alien_number, row_number, alien_type):
        # if row_number > 5: raise ValueError('row number must be less than 6')
        if alien_type == 3:
            ufo = Alien(game=self.game, type=3)
            ufo.rect.x = ufo.x
            ufo.rect.y = ufo.rect.height + 1.2 * ufo.rect.height * 0
            self.ufo.add(ufo)
            return
        type = row_number // 2
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number 
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number, row_number // 2)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break

        for ufo in self.ufo.sprites():
            if ufo.check_edges():
                ufo.kill()
                self.sound.ufo_hover_stop()
                self.active_ufo = False
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

        for ufo in self.ufo.sprites():
            if ufo.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.speed_check_1 = True
            self.speed_check_2 = True
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def spawn_random_ufo(self):
        self.ufo_spawn_requests += 1
        if self.ufo_spawn_requests % self.settings.ufo_spawn_every != 0 or self.active_ufo:
            return

        self.active_ufo = True
        self.create_alien(0, 0, 3)
        self.sound.ufo_hover_start()

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit(alien.type)
                self.sb.increment_score(alien.type)

        collisions = pg.sprite.groupcollide(self.ufo, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit(3)
                self.active_ufo = True
                self.sound.ufo_hover_stop()
            self.sb.increment_score(3)

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

        # Check for colliding lasers
        pg.sprite.groupcollide(self.ship_lasers, self.aliens_lasers.lasers, True, True)

        collisions = pg.sprite.groupcollide(self.barriers.barriers, self.ship_lasers, False, True)
        if collisions:
            for barriers in collisions:
                self.barriers.hit(barriers)

        collisions = pg.sprite.groupcollide(self.barriers.barriers, self.aliens_lasers.lasers, False, True)
        if collisions:
            for barriers in collisions:
                self.barriers.hit(barriers)

    def speed_up_music(self):
        if len(self.aliens) <= 33 and self.speed_check_1:
            self.sound.change_bg_music(1)
            self.speed_check_1 = False

        if len(self.aliens) <= 16 and self.speed_check_2:
            self.sound.change_bg_music(2)
            self.speed_check_2 = False

    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        self.spawn_random_ufo()
        self.speed_up_music()

        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update()
        self.aliens_lasers.update()

        for ufo in self.ufo.sprites():
            if ufo.dead:
                self.sound.ufo_hover_stop()
                ufo.remove()
            ufo.update()

    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
