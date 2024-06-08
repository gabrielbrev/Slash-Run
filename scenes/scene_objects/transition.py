from PPlay.sprite import Sprite
from PPlay.window import Window

from time import time

class Transition:
    def __init__(self, duration):
        self.init_time = 0

        self.t_in = Sprite("assets/scene_objects/transition_in.png", 10)
        self.t_in.set_total_duration(duration)
        self.t_in.set_loop(False)
        self.t_in.playing = False

        self.t_out = Sprite("assets/scene_objects/transition_out.png", 10)
        self.t_out.set_total_duration(duration)
        self.t_out.set_loop(False)
        self.t_out.playing = False

        self.curr_t = None
        
        self.started = False
        self.played = False


    def is_playing(self):
        return not self.played

    def _play(self, t: Sprite):
        self.init_time = time()
        self.curr_t = t
        self.curr_t.set_curr_frame(0)
        self.curr_t.playing = False
        self.played = False
        self.started = False

    def play_in(self):
        self._play(self.t_in)

    def play_out(self, window: Window):
        self._play(self.t_out)
        while self.is_playing():
            window.update()
            self.update()
            self.draw()

    def update(self):
        if self.curr_t:
            if not self.curr_t.playing:
                if not self.started:
                    self.started = True
                    self.curr_t.playing = True

            self.curr_t.update()

            if self.curr_t.get_curr_frame() == self.curr_t.get_final_frame() - 1:
                self.curr_t.playing = False
                self.played = True

    def draw(self):
        if self.curr_t and not self.played:
            self.curr_t.draw()

        
