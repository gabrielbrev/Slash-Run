from PPlay.sprite import Sprite

from .fixed_entity import FixedEntity
from .boulder import Boulder
from .skullord_head import SkullordHead

from grid_objects.energy_orb import EnergyOrb
from grid_objects.spike import Spike
from grid_objects.geyser import Geyser

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA
from core.grid import Grid

from utils import difficulty_multiplier

from time import time
import random


class SkullordHand(FixedEntity):
    GRAVITY = 50

    def __init__(self, x, y, head: SkullordHead, grid: Grid):
        self.player = GD.get_player()
        self.grid = grid
        self.grid_id = grid.id
        if self.grid_id == self.player.fg.id:
            s = Sprite("assets/sprites/entities/skullord/hand/left/idle.png")
            width = 152
        else:
            s = Sprite("assets/sprites/entities/skullord/hand/right/idle.png")
            width = s.width 
        height = s.height
        super().__init__(x, y, width, height)

        if self.grid_id == self.player.fg.id:
            self.set_sprite_anchor(width - s.width, 6)
        else:
            self.set_sprite_anchor(0, 16)

        self.head = head

        self.ground_y = grid.get_inf_ground_y()
        self.idle_y = self.ground_y - self.grid.cell_size * 4.5 - self.height

        self.y_speed = -20

        self.action_change_time = time()
        self.action_cooldown = random.randint(30, 40) / 10
        
        if self.grid_id == self.player.fg.id:
            self.add_sprite("idle", "assets/sprites/entities/skullord/hand/left/idle.png", 1)
            self.add_sprite("smash", "assets/sprites/entities/skullord/hand/left/smash.png", 1)
            self.add_sprite("inactive", "assets/sprites/entities/skullord/hand/left/idle.png", 1)
            self.add_sprite("activating", "assets/sprites/entities/skullord/hand/left/idle.png", 1)
            self.add_sprite("rise", "assets/sprites/entities/skullord/hand/left/smash.png", 1)
            self.set_action("inactive")
        else:
            self.add_sprite("idle", "assets/sprites/entities/skullord/hand/right/idle.png", 1)
            self.add_sprite("smash", "assets/sprites/entities/skullord/hand/right/smash.png", 1)
            self.add_sprite("inactive", "assets/sprites/entities/skullord/hand/right/idle.png", 1)
            self.add_sprite("activating", "assets/sprites/entities/skullord/hand/right/idle.png", 1)
            self.add_sprite("rise", "assets/sprites/entities/skullord/hand/right/smash.png", 1)
            self.set_action("inactive")

        self.add_sound("smash", "assets/sounds/sfx/skullord_attack_1.ogg")
        self.add_sound("smash", "assets/sounds/sfx/skullord_attack_2.ogg")
        self.add_sound("smash", "assets/sounds/sfx/skullord_attack_3.ogg")
        self.add_sound("smash", "assets/sounds/sfx/skullord_attack_4.ogg")
        self.add_sound("smash", "assets/sounds/sfx/skullord_attack_5.ogg")
        self.add_sound("smash", "assets/sounds/sfx/skullord_attack_6.ogg")
        self.add_sound("damage", "assets/sounds/sfx/enemy_damage_hard.ogg", 20)

        self.attacked = False

        self.hit_ground = False

        self.follow_speed = 270
        self.tracking_player = False

        self.arsenal = [
            [EnergyOrb(self.window.width + self.grid.cell_size * i + 100, self.ground_y - self.grid.cell_size, self.grid.cell_size, self.grid.id) for i in range(2)],
            [Boulder(self.window.width + 100, self.ground_y - self.grid.cell_size * 4, self.grid.cell_size, self.grid.id)], 
            [Spike(self.window.width + 100, self.ground_y - self.grid.cell_size, self.grid.cell_size, self.grid.id)],
            [Geyser(self.window.width + self.grid.cell_size * 2.35 * i + 100, self.ground_y - self.grid.cell_size, self.grid.cell_size, self.grid.id) for i in range(4)]
        ]
        self.summoned_objs = []
        self.summon_cooldown = random.randint(50, 100) / 10
        self.summon_time = time()
        self.can_summon = True

        self.alive = True

        self.damaged = False
        self.damage_time = 0
        self.damage_duration = 15

        self.head_health = 5

        GD.add_screen_obj(self)
    
    def attack(self):
        self.attacked = True

    def kill(self):
        self.alive = False

    def is_damaged(self):
        return self.damaged

    def damage(self):
        if not (self.damaged or self.is_moving()):
            self.blink(0.7)
            self.play_sound("damage")
            self.damaged = True
            self.damage_time = time()
            self.move_to(self.window.width, self.y - 50, 1, MA.EASE_IN_OUT_CUBIC)

    def deactivate(self):
        self.set_action("inactive")
        self.move_to(self.og_pos.x, self.og_pos.y, 0.5, MA.EASE_IN_OUT_CUBIC)

    def activate(self):
        self.set_action("activating")
        self.move_to(self.player.x + self.player.width/2 - self.width/2, self.idle_y, 0.5, MA.EASE_IN_OUT_CUBIC)
        self.action_cooldown /= random.randint(1, 4)
        self.action_change_time = time()

    def idle(self):
        self.set_action("rise")
        self.move_to(self.x, self.idle_y, 1, MA.EASE_OUT_QUAD)

    def smash(self):
        self.attacked = False
        self.lost_health = False
        self.hit_ground = False # 
        self.set_action("smash")
        self.move_to(self.x, self.ground_y - self.height + 2, 0.65, MA.EASE_IN_BACK, 5)

    def move_right(self):
        self.x += self.follow_speed * self.window.delta_time()
    
    def move_left(self):
        self.x -= self.follow_speed * self.window.delta_time()

    def snap_to_player(self):
        self.x = self.player.x + self.player.width/2 - self.width/2

    def summon_obj(self):
        if self.can_summon and not GD.is_game_over():
            indexes = [0, 1, 2, 3]
            weights = [18, 40, 22, 20]
            index = random.choices(indexes, weights=weights, k=1)[0]
            self.summoned_objs = self.arsenal[index]
            for obj in self.summoned_objs:
                obj.reset()
            
    def update_summoned_objs(self):
        if len(self.summoned_objs):
            for obj in self.summoned_objs:
                obj.x -= self.grid.speed.get_value() * self.window.delta_time()
                obj.update()
                if GD.off_screen(obj) < 0:
                    obj.fade_sounds(500)
                elif hasattr(obj, "destroyed"):
                    if obj.is_destroyed():
                        obj.x = -500

            if GD.off_screen(self.summoned_objs[-1]) < 0:
                self.summoned_objs = []
        else:
            curr_time = time()
            if curr_time - self.summon_time >= self.summon_cooldown:
                self.summon_time = curr_time
                self.summon_cooldown = random.randint(15, 55) / 10 / difficulty_multiplier(self.head_health, 5)
                if random.randint(0, 2):
                    if self.alive:
                        self.summon_obj()


    def handle_actions(self):
        if not self.damaged:
            curr_time = time()
            if self.get_action() == "idle":
                player_center_x = self.player.x + self.player.width/2
                hand_center_x = self.x + self.width/2
                if self.tracking_player:
                    if curr_time - self.action_change_time >= self.action_cooldown:
                        self.action_change_time = curr_time
                        self.action_cooldown = random.randint(5, 15) / 10
                        self.smash()

                    if hand_center_x - player_center_x > 1:
                        self.move_left()
                    elif hand_center_x - player_center_x < -1:
                        self.move_right()
                    else:
                        self.snap_to_player()
                        
                else:
                    self.deactivate()

            elif self.get_action() == "smash":
                if not self.move_animation.is_playing():
                    if curr_time - self.action_change_time >= self.action_cooldown:
                        self.action_change_time = curr_time
                        self.action_cooldown = random.randint(25, 30) / 10 / difficulty_multiplier(self.head_health, 5)
                        self.idle()

            elif self.get_action() == "rise":
                if not self.is_moving():
                    self.set_action("idle")

            elif self.get_action() == "inactive":
                if self.tracking_player:
                    if not self.is_moving():
                        self.activate()
                else:
                    if self.y >= self.og_pos.y:
                        self.y_speed -= SkullordHand.GRAVITY * self.window.delta_time()
                    else:
                        self.y_speed += SkullordHand.GRAVITY * self.window.delta_time()
                    self.y += self.y_speed * self.window.delta_time()

            elif self.get_action() == "activating":
                if not self.is_moving():
                    self.set_action("idle")

    def mute(self):
        super().mute()
        for obj_list in self.arsenal:
            for obj in obj_list:
                obj.mute()

    def unmute(self):
        super().unmute()
        for obj_list in self.arsenal:
            for obj in obj_list:
                obj.unmute()

    def update(self):
        if self.alive:
            self.tracking_player = self.player.curr_grid.id == self.grid.id and not self.player.switching

        self.damage_duration = 15 / difficulty_multiplier(self.head_health, 5)
        self.update_summoned_objs()

        if not self.hit_ground:
            for obj in GD.get_screen_objs("InfiniteGround", self.grid_id):
                if self.collided(obj):
                    self.hit_ground = True
                    self.play_sound("smash")
                    break

        super().update()

    def draw(self):
        for obj in self.summoned_objs:
            if GD.on_screen(obj, append_to_list=True):
                obj.draw()
        if self.alive:
            super().draw()