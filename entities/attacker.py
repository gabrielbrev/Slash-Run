from PPlay.gameobject import GameObject

from utils import Vector

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

        self.add_sprite("idle", f"assets/sprites/entities/monsters/attacker/idle{cell_size}.png", 2, 1000)
        self.add_sprite("attack", f"assets/sprites/entities/monsters/attacker/attack{cell_size}.png", 9, 450, False)

        self.set_action("idle")

        self.set_sprite_anchor(self.width - self.sprite.width, self.height - self.sprite.height)

        self.add_sound("attack", "assets/sounds/sfx/attacker_attack.ogg", 40)

    def land(self, obj: GameObject):
        if self.on_air:
            self.on_air = False
            self.y = obj.y - self.height + 1

    def attack(self):
        if not self.get_action() == "attack" and not self.attacked:
            self.set_action("attack", reset=True)
            self.play_sound("attack")
        super().attack()

    def update(self):
        if self.on_air:
            if self.speed.y < Attacker.TERMINAL_VELOCITY:
                self.speed.y += Attacker.GRAVITY * GD.get_window().delta_time()
                self.speed.y = min(self.speed.y, Attacker.TERMINAL_VELOCITY)
            self.y += self.speed.y * GD.get_window().delta_time()
        else:
            self.speed.y = 0

        self.on_air = True
        
        for obj in GD.get_screen_objs("Ground", self.grid_id):
            if self.collided(obj):
                self.land(obj)

        if self.get_action() == "attack":
            s = self.get_sprite("attack")
            if s.get_curr_frame() == s.get_final_frame() - 1:
                self.set_action("idle")
        
        super().update()
