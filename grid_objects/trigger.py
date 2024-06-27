from .grid_object import GridObject

from core.global_data import GlobalData as GD

class Trigger(GridObject):
    def __init__(self, x, cell_size, grid_id, grid_attached, command, args = (), name = ""):
        super().__init__(x, 0, cell_size, grid_id, False)
        self.window = GD.get_window()
        self.width = cell_size
        self.height = self.window.height
        self.name = name
        self.func = command
        self.args = args
        self.triggered = False
        if not grid_attached:
            self.grid_id = -1

    def activate(self):
        if not self.triggered:
            self.func(*self.args)
        self.triggered = True

    def update(self):
        GD.add_screen_obj(self)
        super().update()