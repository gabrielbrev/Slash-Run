from core.grid import Grid
from core.grid_editor import GridEditor
from core.global_data import GlobalData as GD

from .scene_objects.transition import Transition
from .scene_objects.background import Background

from utils import Multipliable

from core.keyboard_extra import KeyboardExtra
from core.mouse_extra import MouseExtra

class LevelEditor:
    def __init__(self) -> None:
        self.window = GD.get_window()

        self.keyboard = KeyboardExtra()
        self.mouse = MouseExtra()
        self.t = Transition(100)
        
        scroll_multipliers = [num/10 for num in range(10, 51, 5)]

        self.bg = Background("assets/backgrounds/level_bg.jpeg", Multipliable(50, scroll_multipliers))

        self.front_grid = Grid(2000, 13, 64, Multipliable(600, scroll_multipliers), True)
        self.front_grid.load_level(f"levels/0/front.json")
        self.front_grid.move_left()
        self.front_grid.move_right()

        self.back_grid = Grid(2000, 26, 48, Multipliable(500, scroll_multipliers), True)
        self.back_grid.load_level(f"levels/0/back.json")
        self.back_grid.move_left()
        self.back_grid.move_right()

        # Diferenca de velocidades deve ser 5:50:60

        self.scroll_multiplier = Multipliable(1, scroll_multipliers)

        self.editor = GridEditor(self.mouse, self.front_grid, self.back_grid)

    def handle_keys(self):
        # Toma conta da rolagem da tela
            if self.keyboard.key_pressed("RIGHT"):
                self.back_grid.move_left()
                self.front_grid.move_left()
                if self.back_grid.delta_x and self.front_grid.delta_x:
                    self.bg.move_left()
            if self.keyboard.key_pressed("LEFT"):
                self.back_grid.move_right()
                self.front_grid.move_right()
                if self.back_grid.delta_x and self.front_grid.delta_x:
                    self.bg.move_right()
            if self.keyboard.key_clicked("UP"):
                self.bg.raise_speed()
                self.front_grid.raise_speed()
                self.back_grid.raise_speed()
                self.scroll_multiplier.raise_multiplier()
            if self.keyboard.key_clicked("DOWN"):
                self.bg.lower_speed()
                self.front_grid.lower_speed()
                self.back_grid.lower_speed()
                self.scroll_multiplier.lower_multiplier()

            if self.keyboard.key_pressed("LEFT_CONTROL"):
                if self.keyboard.key_pressed("LEFT_SHIFT"):
                    if self.keyboard.key_clicked("Z"):
                        self.editor.redo()
                else:
                    if self.keyboard.key_clicked("Z"):
                        self.editor.undo()
                    if self.keyboard.key_clicked("S"):
                        self.editor.save_changes(f"levels/0")
            
            if self.keyboard.key_clicked("G"):
                self.editor.switch_grid()
            if self.keyboard.key_clicked("D"):
                self.editor.delete_hovered_object()

            if self.keyboard.key_clicked("P"):
                self.editor.cycle_object()
            if self.keyboard.key_clicked("O"):
                self.editor.cycle_object(backwards=True)
    
    def handle_mouse(self):
        if self.mouse.is_button_clicked(self.mouse.BUTTON_LEFT):
            self.editor.place_object()

    def loop(self):
        self.t.play_in()
        while True:
            # Nao esta na funcao handle keys pois quebra o loop
            if self.keyboard.key_clicked("ESCAPE"):
                self.t.play_out(self.window)
                break

            self.handle_keys()
            self.handle_mouse()

            self.window.update()
            self.editor.update()

            self.bg.draw()
            self.back_grid.draw()
            self.front_grid.draw()
            self.editor.draw()
            self.window.draw_text(
                f'''Speed: {self.scroll_multiplier.get_value()}x    Hovering: {self.editor.get_hovered_object_name()}    New Object: {self.editor.get_new_object_name()}    Saved: {self.editor.is_saved()}''',
                x=0, y=0, color=(255, 255, 255)
            )
            self.window.draw_text(self.editor.get_message(), x=0, y=15, bold=True, color=(255, 255, 255))

            self.t.update()
            self.t.draw()
            