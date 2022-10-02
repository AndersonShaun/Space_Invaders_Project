import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.3)

        ship_laser_sound = pg.mixer.Sound('sounds/ship_laser.wav')
        alien_laser_sound = pg.mixer.Sound('sounds/laser.wav')

        ufo_sound = pg.mixer.Sound('sounds/ufo.wav')
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')

        self.sounds =\
            {'ship_laser': ship_laser_sound, 'alien_laser': alien_laser_sound,
             'gameover': gameover_sound, 'ufo': ufo_sound}

        pg.mixer.Sound.set_volume(self.sounds['alien_laser'], 0.2)
        pg.mixer.Sound.set_volume(self.sounds['ship_laser'], 0.2)
        pg.mixer.Sound.set_volume(self.sounds['ufo'], 0.2)

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def shoot_laser(self, type):
        pg.mixer.Sound.play(self.sounds['alien_laser' if type == LaserType.ALIEN else 'ship_laser'])

    def ufo_hover_start(self):
        pg.mixer.Sound.play(self.sounds['ufo'], -1)

    def ufo_hover_stop(self):
        pg.mixer.Sound.stop(self.sounds['ufo'])

    def change_bg_music(self, track):
        self.stop_bg()
        pg.mixer.music.load('sounds/Background_music_2.wav' if track == 1 else 'sounds/Background_music_3.wav')
        self.play_bg()

    def reset_bg_music(self, game_over_flag):
        if game_over_flag:
            self.stop_bg()
            return
        self.stop_bg()
        pg.mixer.music.load('sounds/Background_music.wav')
        self.play_bg()

    def gameover(self):
        self.stop_bg() 
        pg.mixer.music.load('sounds/gameover.wav')
        self.play_bg()
        time.sleep(2.8)
        self.stop_bg()
        pg.mixer.music.load('sounds/Background_music.wav')
