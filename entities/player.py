from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from common import Vector

from grid_objects.ground import Ground
from grid_objects.energy_orb import EnergyOrb

from core.grid import Grid
from core.global_data import GlobalData as GD

from .attacker import Attacker
from .entity import Entity
from .enemy import Enemy
from .boulder import Boulder

from time import time
from math import sqrt

class Player(Entity):
    # Y referencial is inverted
    GRAVITY = 7000
    TERMINAL_VELOCITY = 7000

    MAX_ENERGY = 10
    MAX_HEALTH = 5

    def __init__(self, fg: Grid, bg: Grid):
        super().__init__(200, -1000, fg.cell_size, fg.cell_size)

        self.fg = fg
        self.bg = bg
        self.curr_grid = fg

        self.speed = Vector(400, 0)
        # X speed is constant, Y speed varies because of gravity

        self.switching = False

        self.attack_delay = 0.3
        self.last_attack_time = 0

        self.invincible = False

        self.hp = Player.MAX_HEALTH
        self.energy = 0

        self.add_sprite("run_1", "assets/sprites/kim/run_1.png", 6, 500)
        
        self.add_sprite("run_2", "assets/sprites/kim/run_2.png", 6, 600)

        self.add_sprite("switch_1", "assets/sprites/kim/jump.png", 9)
        self.get_sprite("switch_1").set_sequence_time(4, 9, 75, False)

        self.add_sprite("switch_2", "assets/sprites/kim/jump.png", 9)
        self.get_sprite("switch_2").set_sequence_time(0, 5, 75, False)

        self.add_sprite("jump_1", "assets/sprites/kim/jump.png", 9)
        self.get_sprite("jump_1").set_curr_frame(0)
        self.get_sprite("jump_1").playing = False

        self.add_sprite("jump_2", "assets/sprites/kim/jump.png", 9)
        self.get_sprite("jump_2").set_curr_frame(4)
        self.get_sprite("jump_2").playing = False

        self.add_sprite("attack_1", "assets/sprites/kim/attack_1.png", 4)
        self.get_sprite("attack_1").set_sequence_time(0, 4, 50, False)

        self.add_sprite("attack_2", "assets/sprites/kim/attack_2.png", 4)
        self.get_sprite("attack_2").set_sequence_time(0, 4, 50, False)

        super().set_action("run_1")

    def set_action(self, key, force = False):
        if not self.get_action() == "attack" or force:
            curr_feet_pos = self.y + self.height

            key = f"{key}_{1 if self.curr_grid == self.fg else 2}"
            super().set_action(key)
            self.sprite.set_position(self.x, self.y)
            match key:
                case "switch_1":
                    self.sprite.playing = True
                    self.sprite.set_curr_frame(4)
                case "switch_2":
                    self.sprite.playing = True
                    self.sprite.set_curr_frame(0)

                case "attack_1":
                    self.sprite.playing = True
                    self.sprite.set_curr_frame(0)
                case "attack_2":
                    self.sprite.playing = True
                    self.sprite.set_curr_frame(0)

            self.width = self.sprite.width
            self.height = self.sprite.height
            self.y = curr_feet_pos - self.height

    def jump(self, height):
        if not self.on_air:
            self.on_air = True
            self.speed.y = -sqrt(2 * Player.GRAVITY * (height * self.curr_grid.cell_size))
            self.set_action("jump")

    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height + 1
            self.set_action("run")

    def move_right(self):
        if self.x + self.width < GD.get_window().width:
            self.x += self.speed.x * GD.get_window().delta_time()

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed.x * GD.get_window().delta_time()

    def switch_plane(self):
        if not (self.switching or self.on_air):
            self.switching = True
            self.jump(4)
            
            if self.curr_grid == self.bg:
                self.curr_grid = self.fg
            else:
                self.curr_grid = self.bg

            self.set_action("switch")
 
    def attack(self):
        if time() - self.last_attack_time >= self.attack_delay:
            if not self.get_action() == "attack" and not self.switching:
                self.last_attack_time = time()
                self.set_action("attack")

    def finish_attack(self):
        if not self.sprite.playing:
            if time() - self.last_attack_time >= self.attack_delay:
                self.set_action("run", force=True)

    def special_attack(self):
        if self.energy == Player.MAX_ENERGY:
            self.energy = 0
            for obj in GD.objs_on_screen:
                if isinstance(obj, Enemy):
                    if obj.is_alive():
                        obj.kill()

    def kill(self):
        self.bg.speed.set_value(0)
        self.fg.speed.set_value(0)
        GD.game_over = True

    def increment_energy(self):
        if self.energy < Player.MAX_ENERGY:
            self.energy += 1

    def increment_health(self):
        if self.hp < Player.MAX_HEALTH:
            self.hp += 1

    def decrement_health(self):
        if not self.invincible:
            if self.hp > 0:
                self.hp -= 1
            if self.hp == 0:
                self.kill()

    def update(self):
        if self.on_air:
            if not self.switching:
                self.set_action("jump")
            if self.speed.y < Player.TERMINAL_VELOCITY:
                self.speed.y += Player.GRAVITY * GD.get_window().delta_time()
                self.speed.y = min(self.speed.y, Player.TERMINAL_VELOCITY)

            self.y += self.speed.y * GD.get_window().delta_time()
        else:
            self.speed.y = 0

        self.on_air = True

        if self.y + self.height > GD.get_window().height:
            if self.invincible:
                floor = GameObject()
                floor.y = GD.get_window().height
                self.land(floor)
                self.switching = False
            else:
                self.kill()

        for obj in GD.get_screen_objs():
            if self.curr_grid.id == obj.grid_id and self.collided(obj):
                if isinstance(obj, Ground):
                    if (self.x < obj.x # Verifica se a colisão está acontecendo com a borda esquerda do chão
                        and not self.invincible 
                        and not self.switching
                        and self.y + self.height * 4/5 > obj.y # Verifica se os pés estão abaixo do chão
                        ):
                        self.kill()
                    else:
                        if self.switching:
                            if self.speed.y >= 0:
                                self.switching = False
                                self.land(obj)
                        else:
                            self.land(obj)
                elif isinstance(obj, EnergyOrb):
                    if not obj.collected:
                        obj.collect()
                        self.increment_energy()
                elif isinstance(obj, Attacker):
                    if obj.is_alive():
                        if self.get_action() == "attack":
                            obj.kill()
                            self.increment_energy()
                        elif not obj.attacked:
                            obj.attack()
                            self.decrement_health()
                elif isinstance(obj, Boulder):
                    if not obj.is_destroyed():
                        if self.get_action() == "attack":
                            obj.destroy()
                        elif not obj.damaged_player:
                            obj.attack()
                            self.decrement_health()

        if self.get_action() == "attack":
            self.finish_attack()

        super().update()
            
        