from .obstacle import Obstacle

from grid_objects.ground import Ground

from core.global_data import GlobalData as GD

from random import randint

class FireBall(Obstacle):
    def __init__(self, x, y, speed, cell_size, grid_id):
        super().__init__(
            x=x - cell_size/4,
            y=y + cell_size/4, 
            width=cell_size * 3/4, 
            height=cell_size * 3/4, 
            cell_size=cell_size, 
            grid_id=grid_id,
        )
        self.speed = speed
        self.hit_the_ground = False
        self.played_sound = False

        self.add_sprite("shoot", f"assets/sprites/entities/fireball/shoot{int(cell_size * 3/4)}.png", 3, 200, False)
        self.add_sprite("fly", f"assets/sprites/entities/fireball/fly{int(cell_size * 3/4)}.png", 3, 200)
        self.add_sprite("death", f"assets/sprites/entities/fireball/death{int(cell_size * 3/4)}.png", 3, 200, False)
        
        self.set_action("shoot")

        self.set_sprite_anchor((self.width - self.sprite.width)/2, self.height - self.sprite.height)

        self.add_sound("shoot", "assets/sounds/sfx/fireball.ogg", 30)

    def set_speed(self, speed):
        self.speed = speed

    def destroy(self, stop_moving = True):
        self.hit_the_ground = stop_moving
        self.set_action("death", reset=True)
        self.fade_sounds(200)

    def update_animation(self):
        if self.get_action() == "shoot":
            s = self.get_sprite("shoot")
            if s.get_curr_frame() == s.get_final_frame() - 1:
                self.set_action("fly")

    def update(self):
        if not self.hit_the_ground:
            self.y += self.speed * GD.get_window().delta_time()

            if not self.played_sound:
                self.played_sound = True
                self.play_sound("shoot")

            for obj in GD.get_screen_objs("Ground", self.grid_id):
                if obj.collided(self):
                    self.destroy()
            for obj in GD.get_screen_objs("InfiniteGround", self.grid_id):
                if obj.collided(self):
                    self.destroy()

            self.update_animation()
        if self.get_action() == "death" and self.sprite.get_curr_frame() == self.sprite.get_final_frame() - 1:
            self.destroyed = True

        GD.add_screen_obj(self)
        super().update()        

            