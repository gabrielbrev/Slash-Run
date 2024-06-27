from PPlay.gameobject import GameObject

from utils import Vector

from core.global_data import GlobalData as GD

from grid_objects.ground import Ground
from grid_objects.trigger import Trigger

from .enemy import Enemy

from math import sqrt

class Destroyer(Enemy):
    # Y referencial is inverted
    GRAVITY = 7000
    TERMINAL_VELOCITY = 7000

    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(
            x=x - cell_size * 1/2, 
            y=y - cell_size, 
            width=cell_size * 2, 
            height=cell_size * 2, 
            cell_size=cell_size, 
            grid_id=grid_id
        )

        self.speed = Vector(0, 0)
        self.jumped = False
        self.trigger_distance = 6 * cell_size
        self.jump_trigger = Trigger(
            x=self.x + self.width/2 - self.trigger_distance,
            cell_size=cell_size,
            grid_id=grid_id,
            grid_attached=False,
            name="destroy",
            command=self.jump,
            args=(6,)
        )

        self.add_sprite("idle", f"assets/entities/monsters/destroyer/idle{cell_size * 2}.png", 1, 500)
        self.add_sprite("jump", f"assets/entities/monsters/destroyer/jump{cell_size * 2}.png", 1, 500)
        self.add_sprite("attack", f"assets/entities/monsters/destroyer/attack{cell_size * 2}.png", 4, 150, False)
        self.set_action("idle")

        self.set_sprite_anchor(self.width - self.sprite.width, self.height - self.sprite.height)


    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height + 1   
            if self.jumped and self.get_action() != "attack":
                self.set_action("attack")

    def jump(self, height):
        self.speed.x = -1
        if not self.on_air:
            self.on_air = True
            self.jumped = True
            self.speed.y = -sqrt(2 * Destroyer.GRAVITY * (height * self.cell_size))
            self.set_action("jump")

    def update(self):
        self.x += self.speed.x * GD.get_window().delta_time()
        if self.on_air:
            if self.speed.y < Destroyer.TERMINAL_VELOCITY:
                self.speed.y += Destroyer.GRAVITY * GD.get_window().delta_time()
                self.speed.y = min(self.speed.y, Destroyer.TERMINAL_VELOCITY)
            self.y += self.speed.y * GD.get_window().delta_time()
        else:
            self.speed.y = 0

        self.on_air = True
        
        for obj in GD.get_screen_objs("Ground", self.grid_id):
            if obj.collided(self):
                self.land(obj)
                if self.jumped and self.is_alive():
                    obj.collapse()

        self.jump_trigger.x = self.x + self.width/2 - self.trigger_distance
        self.jump_trigger.update()
        
        super().update()

        GD.on_screen(self.jump_trigger, append_to_list=True)
