from .enemy import Enemy
from .fireball import FireBall

from grid_objects.trigger import Trigger

from utils import Vector

from core.global_data import GlobalData as GD

class Flyer(Enemy):
    GRAVITY = 30

    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(
            x=x, 
            y=y, 
            width=cell_size,
            height=cell_size,
            cell_size=cell_size,
            grid_id=grid_id
        )
        self.trigger_distance = cell_size * 8
        self.attack_trigger = Trigger(
            x=self.x + self.width/2 - self.trigger_distance,
            cell_size=cell_size,
            grid_id=grid_id,
            grid_attached=False,
            name="throw fireball",
            command=self.attack
        )
        self.fire_ball = FireBall(x, y + 20, 0, cell_size, grid_id)
        self.speed = Vector(0, -30)

        self.add_sprite("idle", f"assets/sprites/entities/monsters/flyer/idle{cell_size}.png", 8, 500)
        self.set_action("idle")

        self.set_sprite_anchor((self.width - self.sprite.width)/2, self.height - self.sprite.height)

    def attack(self):
        if not self.attacked and self.alive:
            self.attacked = True
            self.speed.y = -30 * self.cell_size / 64

            player = GD.get_player()
            self.grid_speed = GD.get_grid(self.grid_id).speed.get_value()

            player_top_right = Vector(player.x + player.width/2 - 20, player.y + 20)
            # O número 20 é um ajuste fino para especificar o ponto de contato do ataque
            self_bottom_center = Vector(self.x + self.width/2, self.y + self.height + 20)
            speed = abs((player_top_right.y - self_bottom_center.y) * self.grid_speed / (self_bottom_center.x - player_top_right.x))
            speed = max(speed, 100)
            self.fire_ball.set_speed(speed)

    def update(self):
        if self.y < self.og_pos.y:
            self.speed.y += Flyer.GRAVITY * GD.get_window().delta_time()
        else:
            self.speed.y -= Flyer.GRAVITY * GD.get_window().delta_time()
        self.y += self.speed.y * GD.get_window().delta_time()

        super().update()

        if self.attacked:
            self.fire_ball.update()
        self.fire_ball.x = self.x
        self.attack_trigger.x = self.x + self.width/2 - self.trigger_distance
        self.attack_trigger.update()

        GD.on_screen(self.attack_trigger, append_to_list=True)

    def draw(self):
        super().draw()
        if self.attacked:
            self.fire_ball.draw()