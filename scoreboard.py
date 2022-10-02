import pygame as pg


class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
        self.high_score = game.get_high_scores()
        self.all_time_high_score = self.high_score
        self.lives = game.settings.ship_limit
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_text = self.font.render('Score: ', True, self.text_color)

        self.lives_image = None
        self.lives_rect = None
        self.score_image = None 
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.prep_hud()

    def increment_score(self, alien_type):
        self.score += self.settings.alien_points[alien_type]
        self.update()
        self.prep_hud()

    def decrement_lives(self, ship):
        self.lives = ship.ships_left
        self.prep_hud()

    def prep_hud(self):
        score_str = str(self.score)

        self.score_image = self.font.render('Score: ' + score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

        # Display the high score at the top center of the screen
        high_score_str = str(self.high_score)
        self.high_score_image =\
            self.font.render('High Score: ' + high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - (self.screen_rect.width / 2)
        self.high_score_rect.top = 20

        # Display the lives at the top center of the screen
        lives_str = str(self.lives)
        self.lives_image = self.font.render('Lives: ' + lives_str, True, self.text_color, self.settings.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.screen_rect.left + 20
        self.lives_rect.top = 20

    def reset(self): 
        self.score = 0
        self.lives = self.settings.ship_limit
        self.high_score = self.high_score
        self.prep_hud()
        self.update()

    def update(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.draw()

    def draw(self):
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.lives_image, self.lives_rect)
