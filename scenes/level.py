from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from PPlay.sprite import Sprite

from core.grid import Grid
from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA
from core.keyboard_extra import KeyboardExtra
from core.data_manager import DataManager

from entities.player import Player
from entities.skullord import Skullord

from .scene_objects.bar import Bar
from .scene_objects.background import Background
from .scene_objects.transition import Transition
from .scene_objects.button import Button

from utils import FPSCounter
from utils import Multipliable

from time import time

class Level:
    def __init__(self, level_id) -> None:
        self.window = GD.get_window()

        self.keyboard = KeyboardExtra()
        self.mouse = Mouse()

        self.level_id = level_id

        self.t = Transition(100)

        self.bg = Background("assets/backgrounds/level_bg.jpeg", Multipliable(50))

        self.front_grid = Grid(2000, 13, 64, Multipliable(600))

        self.back_grid = Grid(2000, 26, 48, Multipliable(500))

        self.health_bar = Bar(5, "assets/scene_objects/level/health_bar.png", 6)
        self.health_bar.set_position(5, 5)

        self.energy_bar = Bar(0, "assets/scene_objects/level/energy_bar.png", 11)
        self.energy_bar.set_position(self.health_bar.x, self.health_bar.y + self.health_bar.height)

        self.player = Player(self.front_grid, self.back_grid, self.health_bar, self.energy_bar)

        self.special_attack_sprite = Sprite("assets/entities/kim/flash.png", 12)
        self.special_attack_sprite.set_total_duration(100)
        self.special_attack_sprite.set_loop(False)

        self.retry_button = Button(self.mouse, "assets/scene_objects/buttons/try_again.png")
        self.retry_button.set_position(-self.retry_button.width, self.window.height/2 - self.retry_button.height - 10)

        self.quit_button = Button(self.mouse, "assets/scene_objects/buttons/quit.png")
        self.quit_button.set_position(self.window.width, self.window.height/2 + 10)

        self.shade = GameImage("assets/scene_objects/level/shade.png")

        self.menu_shown = False
        self.paused = False
        self.retry = False
        self.completion_delay = 4
        self.ended = False

        self.dm = DataManager()

        self.fps = FPSCounter(self.window, 0, 0, 30)

        if level_id == 3:
            self.draw_segment = self.bossfight_draw_segment
        else:
            self.draw_segment = self.normal_draw_segment

    def go_to_spawn_position(self):
        MARGIN = 200
        spawn_data = self.player.get_spawn_position()
        x = spawn_data["x"]
        grid = spawn_data["grid"]
    
        delta_x = x - MARGIN
        delta_x_to_speed_ratio = delta_x / grid.speed.get_value()
        self.front_grid.update_x_position(-(self.front_grid.speed.get_value() * delta_x_to_speed_ratio))
        self.back_grid.update_x_position(-(self.back_grid.speed.get_value() * delta_x_to_speed_ratio))

    def show_menu(self):
        if not self.menu_shown:
            self.quit_button.move_to(self.window.width/2 - self.quit_button.width/2, self.window.height/2 + 10, 0.75, MA.EASE_IN_OUT_EXPO)
            self.retry_button.move_to(self.window.width/2 - self.retry_button.width/2, self.window.height/2 - self.retry_button.height - 10, 0.75, MA.EASE_IN_OUT_EXPO)
            self.menu_shown = True

        self.quit_button.update()
        self.retry_button.update()

        self.shade.draw()
        self.quit_button.draw()
        self.retry_button.draw()

    def handle_level_end(self):
        if not self.ended:
            self.ended = True
            self.front_grid.speed.set_value(0)
            self.back_grid.speed.set_value(0)
            self.bg.speed.set_value(0)

    def handle_input(self):
        if not GD.is_game_over() and not GD.is_level_complete():
            if self.keyboard.key_clicked("ESC"):
                if self.paused:
                    self.paused = False
                    self.menu_shown = False
                    self.quit_button.set_position(self.window.width, self.window.height/2 + 10)
                    self.retry_button.set_position(-self.retry_button.width, self.window.height/2 - self.retry_button.height - 10)
                else:
                    self.paused = True
            if self.keyboard.key_pressed("SPACE"):
                    self.player.jump(3)
            if self.keyboard.key_pressed("A"):
                self.player.move_left()  
            if self.keyboard.key_pressed("D"):
                self.player.move_right()
            if self.keyboard.key_pressed("LEFT_SHIFT"):
                self.player.jump_switch()
            if self.mouse.is_button_pressed(1):
                self.player.attack()
            if self.mouse.is_button_pressed(3):
                temp = self.player.special_attack()
                if temp:
                    self.special_attack_sprite.set_curr_frame(0)
                    self.special_attack_sprite.playing = True
                    self.player.special_attack()

    def normal_draw_segment(self):
        self.bg.draw()
        if self.player.get_curr_grid() == self.back_grid and not self.player.is_switching():
            self.player.draw()
            self.back_grid.draw()
            self.front_grid.draw()
        else:
            self.back_grid.draw()
            self.player.draw()
            self.front_grid.draw()
        self.health_bar.draw()
        self.energy_bar.draw()

    def bossfight_draw_segment(self):
        self.bg.draw()
        if self.player.get_curr_grid() == self.back_grid and not self.player.is_switching():
            self.player.draw()
            self.back_grid.draw()
            self.boss.right_hand.draw()
            self.boss.head.draw()
            self.front_grid.draw()
            self.boss.left_hand.draw()
        else:
            self.back_grid.draw()
            self.boss.right_hand.draw()
            self.boss.head.draw()
            self.player.draw()
            self.front_grid.draw()
            self.boss.left_hand.draw()
        self.health_bar.draw()
        self.energy_bar.draw()

    def load_level(self):
        start_time = time()
        self.front_grid.load_level(f"levels/{self.level_id}/front.json")
        self.back_grid.load_level(f"levels/{self.level_id}/back.json")
        if self.level_id == 3:
            self.boss = Skullord(self.window.width - 300, 50, self.front_grid, self.back_grid)
        
        GD.set_level_being_played(self.level_id)
        GD.set_level_complete(False)
        GD.set_game_over(False)
        self.retry = False
        self.t.play_in()
        self.go_to_spawn_position()
        self.player.set_spawn_positon()
        self.special_attack_sprite.playing = False
        self.special_attack_sprite.set_curr_frame(0)
        self.window.update() # Feito para resetar o delta time
        print(f"Level loaded in {(time() - start_time):.2f} seconds\n")

    def loop(self):
        self.load_level()

        while True:
            if GD.is_game_over() or self.paused:
                self.show_menu()

            if GD.is_level_complete():
                self.handle_level_end()
                if  time() - GD.get_level_completion_time() > self.completion_delay:
                    self.t.play_out(self.window)
                    self.dm.update_current_level(self.level_id)
                    break

            self.handle_input()

            if self.quit_button.is_clicked():
                self.quit_button.clicked = False
                self.t.play_out(self.window)
                break
            elif self.retry_button.is_clicked():
                self.retry_button.clicked = False
                self.retry = True
                self.t.play_out(self.window)
                break

            self.window.update()
            if not self.paused:
                self.bg.update()
                self.player.update()
                self.back_grid.update()
                self.front_grid.update()
                self.health_bar.update()
                self.energy_bar.update()
                if self.level_id == 3:
                    self.boss.update()
                    if not GD.is_level_complete() and not self.boss.is_alive():
                        GD.set_level_complete(True)

            self.draw_segment()

            self.fps.update()
            self.fps.draw()

            self.t.update()
            self.t.draw()

            if self.special_attack_sprite.playing:
                self.special_attack_sprite.update()
                # self.special_attack_sprite.draw()
        
        if self.retry:
            self.__init__(self.level_id)
            self.loop()
    