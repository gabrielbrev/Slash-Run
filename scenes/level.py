from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from PPlay.sprite import Sprite

from core.grid import Grid
from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA
from core.keyboard_extra import KeyboardExtra
from core.sound_extra import SoundExtra
from core.data_manager import DataManager

from entities.player import Player
from entities.skullord import Skullord

from .scene_objects.bar import Bar
from .scene_objects.background import Background
from .scene_objects.transition import Transition
from .scene_objects.button import Button

from utils import FPSCounter
from utils import Multipliable

from time import time, sleep

class Level:
    def __init__(self, level_id) -> None:
        self.window = GD.get_window()

        self.keyboard = GD.get_keyboard()
        self.mouse = GD.get_mouse()

        self.level_id = level_id

        self.music = SoundExtra("assets/sounds/music/level_music.ogg", "music", 85)
        self.music.set_repeat(True)

        self.t = Transition(100)

        self.bg = Background(Multipliable(50))

        self.front_grid = Grid(2000, 13, 64, Multipliable(600))

        self.back_grid = Grid(2000, 26, 48, Multipliable(500))

        self.health_bar = Bar(5, "assets/sprites/scene_objects/level/health_bar.png", 6)
        self.health_bar.set_position(5, 5)

        self.energy_bar = Bar(0, "assets/sprites/scene_objects/level/energy_bar.png", 11)
        self.energy_bar.set_position(self.health_bar.x, self.health_bar.y + self.health_bar.height)

        self.player = Player(self.front_grid, self.back_grid, self.health_bar, self.energy_bar)

        self.special_attack_sprite = Sprite("assets/sprites/entities/kim/flash.png", 12)
        self.special_attack_sprite.set_total_duration(500)
        self.special_attack_sprite.set_loop(False)

        self.retry_button = Button(
            mouse=self.mouse, 
            image_file="assets/sprites/scene_objects/buttons/try_again.png",
            transition=self.t,
            hover_sound=SoundExtra("assets/sounds/sfx/button_hover.ogg", "sfx", 15, False)
        )
        self.retry_button.set_position(-self.retry_button.width, self.window.height/2 - self.retry_button.height - 10)

        self.quit_button = Button(
            mouse=self.mouse,
            image_file="assets/sprites/scene_objects/buttons/quit.png",
            transition=self.t,
            hover_sound=SoundExtra("assets/sounds/sfx/button_hover.ogg", "sfx", 15, False)
        )
        self.quit_button.set_position(self.window.width, self.window.height/2 + 10)

        self.shade = GameImage("assets/sprites/scene_objects/level/shade.png")

        self.menu_shown = False
        self.paused = False
        self.retry = False
        self.completion_delay = 4
        self.ended = False

        self.dm = DataManager()

        self.fps = FPSCounter(self.window, 0, 0, 30)

        if level_id == 3:
            self.loop = self.boss_loop

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
        self.window.draw_text("ESC to resume", 5, 5, 12, (235, 235, 235))
        self.quit_button.draw()
        self.retry_button.draw()

    def handle_level_end(self):
        if not self.ended:
            self.ended = True
            self.front_grid.speed.set_value(0)
            self.back_grid.speed.set_value(0)
            self.bg.speed.set_value(0)
            SoundExtra.fade_all(1500)
            if self.level_id == 3:
                self.boss.head.play_sound("death")

    def handle_input(self):
        if not GD.is_game_over() and not GD.is_level_complete():
            if self.keyboard.key_clicked("ESC"):
                if self.paused:
                    self.mouse.hide()
                    self.paused = False
                    self.menu_shown = False
                    self.quit_button.set_position(self.window.width, self.window.height/2 + 10)
                    self.retry_button.set_position(-self.retry_button.width, self.window.height/2 - self.retry_button.height - 10)
                    self.music.unpause()
                    self.player.unmute()
                    self.front_grid.unmute()
                    self.back_grid.unmute()
                    if self.level_id == 3:
                        self.boss.unmute()
                else:
                    self.mouse.unhide()
                    self.paused = True
                    self.music.pause()
                    self.player.mute()
                    self.front_grid.mute()
                    self.back_grid.mute()
                    if self.level_id == 3:
                        self.boss.mute()
            if not self.paused:
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
                    if self.player.special_attack():
                        self.special_attack_sprite.set_curr_frame(0)
                        self.special_attack_sprite.playing = True

        if not self.mouse.is_visible():
            self.mouse.set_position(self.window.width/2, self.window.height/2)

    def load_level(self):
        start_time = time()
        self.window.draw_text("Loading...", 5, self.window.height - 17, 12, (235, 235, 235))
        self.window.update()
        self.front_grid.load_level(f"levels/{self.level_id}/front.json")
        self.window.update() # Evitar que a tela pare de responder
        self.back_grid.load_level(f"levels/{self.level_id}/back.json")
        if self.level_id == 3:
            self.boss = Skullord(self.window.width - 300, 50, self.front_grid, self.back_grid)
            self.boss_music = SoundExtra("assets/sounds/music/boss_music.ogg", "music", 40)
            self.music_fade_time = time() + 4
            self.boss_init_time = self.music_fade_time + 2
            self.completion_delay = 5
            for i in range(10):
                self.player.increment_energy()
        
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
        self.music.play()
        while True:
            if GD.is_game_over() or self.paused:
                if self.music.is_playing():
                    self.music.pause()
                if not self.mouse.is_visible():
                    self.mouse.unhide()
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
                SoundExtra.stop_all()
                self.t.play_out(self.window)
                break
            elif self.retry_button.is_clicked():
                self.retry_button.clicked = False
                self.retry = True
                SoundExtra.stop_all()
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

            self.fps.update()
            self.fps.draw()

            self.t.update()
            self.t.draw()

            if self.special_attack_sprite.playing:
                self.special_attack_sprite.update()
                self.special_attack_sprite.draw()
        
        self.music.fadeout(750)
        if self.retry:
            self.__init__(self.level_id)
            self.mouse.hide()
            self.loop()
        

    def boss_loop(self):
        self.load_level()
        self.music.play()
        while True:
            if GD.is_game_over() or self.paused:
                if self.music.is_playing():
                    self.music.stop()
                if not self.mouse.is_visible():
                    self.mouse.unhide()
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
                SoundExtra.stop_all()
                self.t.play_out(self.window)
                break
            elif self.retry_button.is_clicked():
                self.retry_button.clicked = False
                self.retry = True
                SoundExtra.stop_all()
                self.t.play_out(self.window)
                break

            if not self.boss.is_active():
                if time() >= self.music_fade_time:
                    self.music.fadeout(600)
                    self.bg.darken(500)
                if time() >= self.boss_init_time:
                    self.music = self.boss_music
                    self.music.play()
                    self.boss.activate()

            self.window.update()
            if not self.paused:
                self.bg.update()
                self.player.update()
                self.back_grid.update()
                self.front_grid.update()
                self.health_bar.update()
                self.energy_bar.update()
                self.boss.update()
                if not GD.is_level_complete() and not self.boss.is_alive():
                    print("completou")
                    GD.set_level_complete(True)

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

            # self.fps.update()
            # self.fps.draw()

            self.t.update()
            self.t.draw()

            if self.special_attack_sprite.playing:
                self.special_attack_sprite.update()
                self.special_attack_sprite.draw()
        
        self.music.fadeout(750)
        if self.retry:
            self.__init__(self.level_id)
            self.mouse.hide()
            self.loop()
    