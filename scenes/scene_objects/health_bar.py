from PPlay.sprite import Sprite

from entities.player import Player

class HealthBar(Sprite):
    class HealthBarException(Exception):
        def __init__(self, message="An error occurred."):
            self.message = message
            super().__init__(self.message)

    def __init__(self, player: Player):
        super().__init__("assets/scene_objects/game/health_bar.png", 6)
        self.player = player
        self.hp = 5

    def set_hp(self, hp: int):
        if self.hp < self.total_frames and self.hp >= 0:
            self.hp = hp
            if self.curr_frame != hp:
                self.set_curr_frame(hp)
        else:
            raise HealthBar.HealthBarException("Invalid HP")
        
    def update(self):
        self.set_hp(self.player.hp)
