class Settings:
    """A class to store all settings for Alien Invasion."""

    alien_points = {0: 10, 1: 20, 2: 40, 3: 100}

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)

        self.laser_width = 5
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 30

        self.aliens_shoot_every = 600       # about every 2 seconds at 60 fps
        self.ufo_spawn_every = 6000

        self.alien_0_points = 40
        self.alien_1_points = 20
        self.alien_2_points = 10
        self.alien_3_points = 100

        self.ship_limit = 3        # total ships allowed in game before game over

        self.fleet_drop_speed = 20
        self.fleet_direction = 1     # change to a Vector(1, 0) move to the right, and ...
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.alien_speed_factor = 0.1
        self.ship_speed_factor = 1
        self.laser_speed_factor = 1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale
