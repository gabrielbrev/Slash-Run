from core.global_data import GlobalData as GD

from .trigger import Trigger

class EndTrigger(Trigger):
    def __init__(self, x, cell_size, grid_id, on_editor = False):
        super().__init__(x, cell_size, grid_id, False, self.end_level, name="end")
        self.on_editor = on_editor
        self.add_sprite("default",f"assets/sprites/grid_objects/highlights/trigger{cell_size}.png", 1)
        self.set_action("default")

    def end_level(self):
        GD.set_level_complete(True)

    def draw(self):
        if self.on_editor:
            super().draw()
            text = "END"
            size = 30
            self.window.draw_text(text, self.x + 10, GD.get_window().height/2 - size/2, size, (255, 250, 250), "assets/fonts/Roboto-Regular.ttf", True)