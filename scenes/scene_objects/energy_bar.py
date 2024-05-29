from PPlay.sprite import Sprite

from entities.player import Player

class EnergyBar(Sprite):
    class EnergyBarException(Exception):
        def __init__(self, message="An error occurred."):
            self.message = message
            super().__init__(self.message)

    def __init__(self, player: Player):
        super().__init__("assets/scene_objects/game/energy_bar.png", 11)
        self.player = player
        self.energy = 5

    def set_energy(self, energy: int):
        if self.energy < self.total_frames and self.energy >= 0:
            self.energy = energy
            if self.curr_frame != energy:
                self.set_curr_frame(energy)
        else:
            raise EnergyBar.EnergyBarException("Invalid Energy Points")
        
    def update(self):
        self.set_energy(self.player.energy)
