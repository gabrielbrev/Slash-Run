from PPlay.gameobject import GameObject

from .obstacle import Obstacle

from core.global_data import GlobalData as GD

from utils import Vector

class Boulder(Obstacle):
    # Y referencial is inverted
    GRAVITY = 7000
    TERMINAL_VELOCITY = 7000

    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(
            x=x, 
            y=y, 
            width=cell_size * 4, 
            height=cell_size * 4, 
            cell_size=cell_size, 
            grid_id=grid_id,
        )

        self.x -= 1.5 * self.cell_size
        self.y -= 3 * self.cell_size

        self.speed = Vector(-1, 0)

        self.add_sprite("roll", f"assets/sprites/entities/boulder/roll{cell_size * 4}.png", 72, 5500)
        self.set_action("roll")

        self.add_sound("roll", "assets/sounds/sfx/boulder_roll.ogg", 70, True)

    def reset(self):
        self.speed = Vector(-1, 0)
        self.damaged_player = False
        super().reset()

    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height + 1

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
        
        for obj in GD.get_screen_objs("Ground", self.grid_id):
            if self.collided(obj):
                self.land(obj)
        for obj in GD.get_screen_objs("InfiniteGround", self.grid_id):
            if self.collided(obj):
                self.land(obj)

        on_screen = GD.on_screen(self)
        if not self.is_sound_playing("roll") and on_screen:
            self.play_sound("roll")
        elif not on_screen:
            self.fade_sounds(200)

        super().update()
