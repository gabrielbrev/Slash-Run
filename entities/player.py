from PPlay.sprite import *
from PPlay.window import *
from PPlay.keyboard import *

from utils import Vector

class Player(Sprite):
    # Y referencial is inverted
    GRAVITY = 6000
    TERMINAL_VELOCITY = 7000

    def __init__(self, window: Window, keyboard: Keyboard, image_file, frames=1):
        super().__init__(image_file, frames)
        self.window = window
        self.keyboard = keyboard

        self.set_total_duration(500)

        self.x = 200

        self.speed = Vector(400, 0)
        # X speed is constant, Y speed varies because of gravity

        self.on_air = True

    def jump(self):
        if not self.on_air:
            self.on_air = True
            self.speed.y = -1500

    def move_right(self):
        if self.x + self.width < self.window.width:
            self.x += self.speed.x * self.window.delta_time()

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed.x * self.window.delta_time()
        
    def update(self):
        super().update()

        if self.keyboard.key_pressed("W"):
            self.jump()

        if self.keyboard.key_pressed("A"):
            self.move_left()
            
        if self.keyboard.key_pressed("D"):
            self.move_right()

        if self.on_air:
            if self.speed.y < Player.TERMINAL_VELOCITY:
                self.speed.y += Player.GRAVITY * self.window.delta_time()
                self.speed.y = min(self.speed.y, Player.TERMINAL_VELOCITY)

            self.y += self.speed.y * self.window.delta_time()
        else:
            self.speed.y = 0

        self.on_air = True

        if self.y + self.height > self.window.height:
            self.y = self.window.height - self.height
            self.on_air = False

            
        