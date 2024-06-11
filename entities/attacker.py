from PPlay.gameobject import GameObject

from common import Vector

from core.global_data import GlobalData as GD

from grid_objects.ground import Ground

from .enemy import Enemy

class Attacker(Enemy):
    # Y referencial is inverted
    GRAVITY = 7000
    TERMINAL_VELOCITY = 7000

    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(
            x=x - cell_size * 1/4, 
            y=y - cell_size * 1/2, 
            width=cell_size * 3/2, 
            height=cell_size * 3/2, 
            cell_size=cell_size, 
            grid_id=grid_id
        )

        self.speed = Vector(0, 0)

        self.add_sprite("idle", f"assets/sprites/monsters/attacker/idle{cell_size}.jpeg", 1, 500)

        self.add_sprite("attack", f"assets/sprites/monsters/attacker/attack{cell_size}.jpeg", 1, 500)

        self.set_action("idle")

    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height + 1

    def attack(self):
        if not self.get_action() == "attack" and not self.attacked:
            self.set_action("attack")
            self.attacked = True

    def update(self):
        if self.on_air:
            if self.speed.y < Attacker.TERMINAL_VELOCITY:
                self.speed.y += Attacker.GRAVITY * GD.get_window().delta_time()
                self.speed.y = min(self.speed.y, Attacker.TERMINAL_VELOCITY)
            self.y += self.speed.y * GD.get_window().delta_time()
        else:
            self.speed.y = 0

        self.on_air = True
        
        for obj in GD.get_screen_objs():
            if obj.grid_id == self.grid_id and self.collided(obj):
                if isinstance(obj, Ground):
                    self.land(obj)
        
        super().update()
