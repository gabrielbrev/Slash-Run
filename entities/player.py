from PPlay.gameobject import GameObject

from utils import Vector

from core.grid import Grid
from core.global_data import GlobalData as GD

from .entity import Entity
from .enemy import Enemy
from .obstacle import Obstacle

from scenes.scene_objects.bar import Bar

from time import time
from math import sqrt

class Player(Entity):
    # Y referencial is inverted
    GRAVITY = 7000
    TERMINAL_VELOCITY = 7000
    GROUND_FRICTION = 550

    def __init__(self, fg: Grid, bg: Grid, health_bar: Bar, energy_bar: Bar):
        super().__init__(200, -1000, fg.cell_size, fg.cell_size)

        self.fg = fg
        self.bg = bg
        self.curr_grid = fg

        self.speed = Vector(bg.speed.get_value(), 0)
        # X speed is constant, Y speed varies because of gravity

        self.switching = False

        self.attack_delay = 0.3
        self.last_attack_time = 0
        self.attacking = False

        self.invincible = False

        self.health = health_bar
        self.energy = energy_bar

        self.add_sprite("run_1", "assets/sprites/entities/kim/run_1.png", 6, 500)
        self.add_sprite("run_2", "assets/sprites/entities/kim/run_2.png", 6, 500)
        self.add_sprite("switch_1", "assets/sprites/entities/kim/switch_1.png", 7, 500, False)
        self.add_sprite("switch_2", "assets/sprites/entities/kim/switch_2.png", 7, 500, False)
        self.add_sprite("jump_1", "assets/sprites/entities/kim/jump_1.png", 1)
        self.add_sprite("jump_2", "assets/sprites/entities/kim/jump_2.png", 1)
        self.add_sprite("attack_1", "assets/sprites/entities/kim/attack_1.png", 6, 75, False)
        self.add_sprite("attack_2", "assets/sprites/entities/kim/attack_2.png", 6, 75, False)
        self.add_sprite("death_1", "assets/sprites/entities/kim/death_1.png", 1)
        self.add_sprite("death_2", "assets/sprites/entities/kim/death_2.png", 1)

        super().set_action("run_1")

        self.add_sound("run", "assets/sounds/sfx/kim_run.ogg", 100, True)
        self.add_sound("attack", "assets/sounds/sfx/kim_attack_1.ogg", 30)
        self.add_sound("attack", "assets/sounds/sfx/kim_attack_2.ogg", 30)
        self.add_sound("attack", "assets/sounds/sfx/kim_attack_3.ogg", 30)
        self.add_sound("special_attack", "assets/sounds/sfx/kim_special_attack.ogg", 70)
        self.add_sound("jump", "assets/sounds/sfx/kim_jump_1.ogg", 30)
        self.add_sound("jump", "assets/sounds/sfx/kim_jump_2.ogg", 30)
        self.add_sound("jump", "assets/sounds/sfx/kim_jump_3.ogg", 30)
        self.add_sound("jump", "assets/sounds/sfx/kim_jump_4.ogg", 30)
        self.add_sound("damage", "assets/sounds/sfx/kim_damage.ogg", 75)
        self.add_sound("death", "assets/sounds/sfx/kim_death.ogg", 25)

        self.play_sound("run")
        self.pause_sound("run")

        GD.set_player(self) 

    def set_action(self, key, force = False):
        curr_action = self.get_action()
        if curr_action != key and (not curr_action == "attack" or force):
            curr_feet_pos = self.y + self.height

            play = True
            reset = False
            match key:
                case "switch":
                    reset = True
                case "attack":
                    reset = True

            super().set_action(f"{key}_{1 if self.curr_grid == self.fg else 2}", reset=reset, play=play)
            self.sprite.set_position(self.x, self.y)
            self.width = self.sprite.width
            self.height = self.sprite.height
            self.y = curr_feet_pos - self.height

    def get_sprite(self, key):
        key += f"_{1 if self.curr_grid == self.fg else 2}"
        return super().get_sprite(key)

    def get_curr_grid(self):
        return self.curr_grid
    
    def is_switching(self):
        return self.switching

    def get_spawn_position(self):
        front_grid_spawn = self.fg.get_spawn_position()
        back_grid_spawn = self.bg.get_spawn_position()
        if front_grid_spawn and back_grid_spawn:
            if front_grid_spawn[0] > back_grid_spawn[0]:
                grid = self.fg
                x, y = front_grid_spawn
            else:
                grid = self.bg
                x, y = back_grid_spawn
        elif front_grid_spawn:
            x, y = front_grid_spawn
            grid = self.fg
        elif back_grid_spawn:
            x, y = back_grid_spawn
            grid = self.bg
        else:
            x = 200
            y = -1000
            grid = self.fg
        return {
            "x": x,
            "y": y,
            "grid": grid
        }
    
    def set_spawn_positon(self):
        spawn_data = self.get_spawn_position()
        self.x = spawn_data["x"]
        self.y = spawn_data["y"]
        if self.curr_grid != spawn_data["grid"]:
            self.switch_plane()

    def jump(self, height):
        if not self.on_air:
            self.on_air = True
            self.speed.y = -sqrt(2 * Player.GRAVITY * (height * self.curr_grid.cell_size))
            if not self.switching:
                self.set_action("jump", force=True)
            self.play_sound("jump")

    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height
            if self.alive:
                self.set_action("run")

    def move_right(self):
        if self.x + self.width < GD.get_window().width:
            self.x += 400 * GD.get_window().delta_time()

    def move_left(self):
        if self.x > 0:
            self.x -= 400 * GD.get_window().delta_time()

    def switch_plane(self):
        if self.curr_grid == self.bg:
            self.curr_grid = self.fg
        else:
            self.curr_grid = self.bg
        self.speed.x = self.curr_grid.speed.get_value()

    def jump_switch(self):
            if not (self.switching or self.on_air):
                self.invincible = True
                self.switching = True
                self.jump(4)
                self.set_action("switch")
                self.switch_plane()
 
    def attack(self):
        if time() - self.last_attack_time >= self.attack_delay:
            if not self.get_action() == "attack" and not self.switching:
                self.attacking = True
                self.last_attack_time = time()
                self.set_action("attack")
                self.play_sound("attack")

    def finish_attack(self):
        if not self.sprite.playing:
            if time() - self.last_attack_time >= self.attack_delay:
                self.attacking = False
                self.set_action("run", force=True)

    def special_attack(self):
        if self.energy.is_maxed():
            self.energy.set_value(0)
            for obj in GD.get_screen_objs("All"):
                if isinstance(obj, Enemy):
                    if obj.is_alive():
                        obj.kill()
                elif isinstance(obj, Obstacle):
                    if not obj.is_destroyed():
                        obj.destroy()

            # Checagem exclusiva para o boss pois é necessário trazer apenas os elementos dele
            boss_hands_damaged = False
            for obj in GD.get_screen_objs("SkullordHand"):
                if not obj.is_damaged():
                    # SERA IMPLEMENTADO SE SOBRAR TEMPO
                    # obj.set_action("idle")
                    # obj.damage()
                    pass
                else:
                    boss_hands_damaged = True
            if boss_hands_damaged:
                for obj in GD.get_screen_objs("SkullordHead"):
                    obj.can_summon = False
            self.play_sound("special_attack")
            return 1
        return 0

    def kill(self):
        if not GD.is_level_complete():
            self.alive = False
            self.health.set_value(0)
            if not GD.is_game_over():
                self.play_sound("death")
            GD.set_game_over(True)

    def increment_energy(self):
        self.energy.increment()

    def increment_health(self):
        self.health.increment

    def decrement_health(self):
        if not (self.invincible or self.switching):
            temp = self.health.get_value()
            self.health.decrement()
            if self.health.get_value() == 0:
                self.kill()
            elif self.health.get_value() < temp:
                self.blink(1)
                self.play_sound("damage")

    def handle_physics(self):
        if self.health.get_value() == 0:
            self.x += self.speed.x * GD.get_window().delta_time()
            self.speed.x -= Player.GROUND_FRICTION * GD.get_window().delta_time()
            self.speed.x = max(self.speed.x, 0)
        elif GD.is_level_complete():
            self.x += self.speed.x * GD.get_window().delta_time()

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
            self.kill()        

    def handle_ground(self, obj):
        if (self.x < obj.x # Verifica se a colisão está acontecendo com a borda esquerda do chão
            and not self.invincible
            and not self.switching
            and self.y + self.height * 4/5 > obj.y # Verifica se os pés estão abaixo do chão
            ):
            self.kill()
            self.speed.x = 0
        else:
            if self.switching:
                if self.speed.y >= 0:
                    self.switching = False
                    self.invincible = False
                    self.land(obj)
            else:
                self.land(obj)

    def handle_collisions(self):        
        for obj in GD.get_screen_objs("Ground", self.curr_grid.id):
            if obj.collided(self):
                self.handle_ground(obj)

        for obj in GD.get_screen_objs("InfiniteGround", self.curr_grid.id):
            if obj.collided(self):
                self.handle_ground(obj)

        for obj in GD.get_screen_objs("EnergyOrb", self.curr_grid.id):
            if obj.collided(self) and not obj.collected and not self.switching:
                obj.collect()
                self.increment_energy()

        for obj in GD.get_screen_objs("Attacker", self.curr_grid.id):
            if obj.is_alive() and obj.collided(self):
                if self.attacking:
                    obj.kill()
                    self.increment_energy()
                elif not obj.attacked:
                    obj.attack()
                    self.decrement_health()

        for obj in GD.get_screen_objs("Destroyer", self.curr_grid.id):
            if obj.is_alive() and obj.collided(self):
                if self.attacking:
                    obj.kill()
                    self.increment_energy()
                elif not obj.attacked:
                    obj.attack()
                    self.decrement_health()

        for obj in GD.get_screen_objs("Boulder", self.curr_grid.id):
            if obj.collided(self) and not obj.is_destroyed():
                if not obj.damaged_player:
                    obj.deal_damage()
                    self.decrement_health()

        for obj in GD.get_screen_objs("FireBall", self.curr_grid.id):
            if obj.collided(self) and not obj.is_destroyed():
                if not obj.damaged_player:
                    obj.deal_damage()
                    self.decrement_health()

        for obj in GD.get_screen_objs("Geyser", self.curr_grid.id):
            if obj.collided(self):
                if not obj.damaged_player and (obj.get_action() == "active" or obj.get_action() == "rise"):
                    obj.damage_player()
                    self.decrement_health()

        for obj in GD.get_screen_objs("Spike", self.curr_grid.id):
            if obj.collided(self):
                if not obj.damaged_player:
                    obj.damage_player()
                    self.decrement_health()

        for obj in GD.get_screen_objs("Trigger", self.curr_grid.id):
            if obj.collided(self):
                obj.activate()

        for obj in GD.get_screen_objs("EndTrigger", self.curr_grid.id):
            if obj.collided(self):
                obj.activate()

        for obj in GD.get_screen_objs("SkullordHand", self.curr_grid.id):
            if obj.collided(self):
                if obj.is_alive():
                    if self.attacking and obj.get_action() == "smash":
                        obj.damage()
                    elif not obj.attacked:
                        if obj.get_action() == "smash" and obj.is_moving() and not obj.is_damaged():
                            obj.attack()
                            self.decrement_health()

        for obj in GD.get_screen_objs("SkullordHead", self.curr_grid.id):
            if obj.collided(self):
                if obj.get_action() == "magic" and self.attacking:
                    obj.decrement_health()

    def update(self):
        self.handle_physics()

        if self.total_blinks:
            self.invincible = True
        else:
            self.invincible = False

        self.handle_collisions()

        if self.get_action() != "run":
            self.pause_sound("run")
        else:
            self.unpause_sound("run")

        if self.get_action() == "attack":
            if self.get_sprite("attack").get_curr_frame() > 2:
                self.attacking = False
            self.finish_attack()

        if not self.is_alive():
            self.set_action("death")

        super().update()