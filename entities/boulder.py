from PPlay.gameobject import GameObject

from .grid_entity import GridEntity

from grid_objects.ground import Ground

from core.global_data import GlobalData as GD

from common import Vector

class Boulder(GridEntity):
    # Y referencial is inverted
    GRAVITY = 7000
    TERMINAL_VELOCITY = 7000

    def __init__(self, x, y, cell_size, grid_id, fragile):
        self.SPECIAL_DATA = ["fragile"]
        super().__init__(
            x=x, 
            y=y, 
            width=cell_size * 4, 
            height=cell_size * 4, 
            cell_size=cell_size, 
            grid_id=grid_id
        )

        self.x -= 1.5 * self.cell_size
        self.y -= 3 * self.cell_size

        self.speed = Vector(-1, 0)
        self.fragile = fragile
        self.destroyed = False
        self.damaged_player = True

        self.add_sprite("roll", f"assets/sprites/boulder/roll{cell_size * 4}.png", 1, 1000)
        self.set_action("roll")

    def is_destroyed(self):
        return self.destroyed
    
    def destroy(self):
        self.destroyed = True

    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height + 1

    def attack(self):
        self.damaged_player = True

    def update(self):
        self.x += self.speed.x

        if self.on_air:
            if self.speed.y < Boulder.TERMINAL_VELOCITY:
                self.speed.y += Boulder.GRAVITY * GD.get_window().delta_time()
                self.speed.y = min(self.speed.y, Boulder.TERMINAL_VELOCITY)
            self.y += self.speed.y * GD.get_window().delta_time()
        else:
            self.speed.y = 0

        self.on_air = True
        
        for obj in GD.get_screen_objs():
            if obj.grid_id == self.grid_id and self.collided(obj):
                if isinstance(obj, Ground):
                    self.land(obj)
        
        super().update()
