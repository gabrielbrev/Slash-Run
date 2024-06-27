from .grid_object import GridObject

from time import time

class Geyser(GridObject):
    def __init__(self, x, y, cell_size, grid_id):
        self.SPECIAL_DATA = ["active_duration", "cooldown"]
        super().__init__(x, y - 3 * cell_size, cell_size, grid_id, False)
        self.active_duration = 1
        self.cooldown = 0.5
        self.activation_time = 0
        self.deactivation_time = 0

        self.damaged_player = False

        self.add_sprite("inactive", f"assets/grid_objects/geyser/inactive{cell_size}.png", 1)
        self.add_sprite("active", f"assets/grid_objects/geyser/active{cell_size}.png", 3, 200)
        self.add_sprite("rise", f"assets/grid_objects/geyser/rise{cell_size}.png", 6, 150, False)
        self.add_sprite("fall", f"assets/grid_objects/geyser/fall{cell_size}.png", 11, 275, False)

        self.set_action("inactive")

    def damage_player(self):
        self.damaged_player = True

    def update(self):
        curr_time = time()

        # Começa a contar a partir do primeiro update (quando entra na area de update)
        if not self.activation_time:
            self.activation_time = curr_time
            self.deactivation_time = curr_time

        match self.get_action():
            case "inactive":
                if curr_time - self.deactivation_time >= self.cooldown:
                    self.set_action("rise", reset=True)
            case "active":
                if curr_time - self.activation_time >= self.active_duration:
                    self.set_action("fall", reset=True)
            case "rise":
                s = self.get_sprite("rise")
                if s.get_curr_frame() == s.get_final_frame() - 1:
                    self.activation_time = curr_time
                    self.set_action("active")
            case "fall":
                s = self.get_sprite("fall")
                if s.get_curr_frame() == s.get_final_frame() - 1:
                    self.deactivation_time = curr_time
                    self.set_action("inactive")

        super().update()
            