from PPlay.gameobject import GameObject

from utils import Vector

from core.global_data import GlobalData as GD

class MoveAnimation:
    LINEAR = 0
    EASE_IN_EXPO = 1
    EASE_IN_OUT_QUAD = 2
    EASE_OUT_QUAD = 3
    EASE_IN_CUBIC = 4
    EASE_OUT_CUBIC = 5
    EASE_IN_OUT_CUBIC = 6
    EASE_OUT_EXPO = 7
    EASE_IN_OUT_EXPO = 8
    EASE_IN_BACK = 9
    EASE_OUT_BACK = 10
    EASE_IN_OUT_BACK = 11

    def __init__(self, obj: GameObject, x, y) -> None:
        self.obj = obj
        self.curr_pos = Vector(x, y)
        self.delta_pos = Vector()
        self.destination = Vector(x, y)
        self.elapsed_time = 0
        self.duration = 0
        self.animation = self.linear
        self.playing = False
        self.overshoot = 1.70158
        self.move_buffer = []

    def is_playing(self):
        return self.playing

    def move_to(self, x, y, duration_s, animation, overshoot=1.70158, buffer=False):
        if self.playing and buffer:
            params_dict = {
                "x": x,
                "y": y,
                "duration_s": duration_s,
                "animation": animation,
                "overshoot": overshoot
            }
            self.move_buffer.append(params_dict)
        else:
            self.duration = duration_s
            self.overshoot = overshoot
            self.curr_pos.x = self.obj.x
            self.curr_pos.y = self.obj.y
            self.delta_pos.x = x - self.obj.x
            self.delta_pos.y = y - self.obj.y
            self.destination.x = x
            self.destination.y = y
            self.elapsed_time = 0
            self.playing = True
            match animation:
                case 0:
                    self.animation = self.linear
                case 1:
                    self.animation = self.ease_in_expo
                case 2:
                    self.animation = self.ease_in_out_quad
                case 3:
                    self.animation = self.ease_out_quad
                case 4:
                    self.animation = self.ease_in_cubic
                case 5:
                    self.animation = self.ease_out_cubic
                case 6:
                    self.animation = self.ease_in_out_cubic
                case 7:
                    self.animation = self.ease_out_expo
                case 8:
                    self.animation = self.ease_in_out_expo
                case 9:
                    self.animation = self.ease_in_back
                case 10:
                    self.animation = self.ease_out_back
                case 11:
                    self.animation = self.ease_in_out_back

    def linear(self, time, start: Vector, change: Vector, duration):
        x = change.x * time/duration + start.x
        y = change.y * time/duration + start.y
        return x, y

    def ease_in_out_quad(self, time, start: Vector, change: Vector, duration):
        time /= duration/2
        if time < 1:
            x = change.x/2 * time * time + start.x
            y = change.y/2 * time * time + start.y
            return x, y
        time -= 1
        x = -change.x/2 * (time*(time-2) - 1) + start.x
        y = -change.y/2 * (time*(time-2) - 1) + start.y
        return x, y
    
    def ease_out_quad(self, time, start: Vector, change: Vector, duration):
        time /= duration
        x = -change.x * time * (time-2) + start.x
        y = -change.y * time * (time-2) + start.y
        return x, y

    def ease_in_cubic(self, time, start: Vector, change: Vector, duration):
        time /= duration
        x = change.x * time * time * time + start.x
        y = change.y * time * time * time + start.y
        return x, y

    def ease_out_cubic(self, time, start: Vector, change: Vector, duration):
        time /= duration
        time -= 1
        x = change.x * (time * time * time + 1) + start.x
        y = change.y * (time * time * time + 1) + start.y
        return x, y

    def ease_in_out_cubic(self, time, start: Vector, change: Vector, duration):
        time /= duration/2
        if time < 1:
            x = change.x/2 * time * time * time + start.x
            y = change.y/2 * time * time * time + start.y
            return x, y
        time -= 2
        x = change.x/2 * (time * time * time + 2) + start.x
        y = change.y/2 * (time * time * time + 2) + start.y
        return x, y
    
    def ease_in_expo(self, time, start: Vector, change: Vector, duration):
        x = change.x * 2**(10 * (time/duration - 1)) + start.x
        y = change.y * 2**(10 * (time/duration - 1)) + start.y
        return x, y
    
    def ease_out_expo(self, time, start: Vector, change: Vector, duration):
        x = change.x * (-2**(-10 * time/duration) + 1) + start.x
        y = change.y * (-2**(-10 * time/duration) + 1) + start.y
        return x, y
    
    def ease_in_out_expo(self, time, start: Vector, change: Vector, duration):
        time /= duration/2
        if time < 1:
            x = change.x/2 * 2**(10 * (time - 1)) + start.x
            y = change.y/2 * 2**(10 * (time - 1)) + start.y
            return x, y
        time -= 1
        x = change.x/2 * (-2**(-10 * time) + 2) + start.x
        y = change.y/2 * (-2**(-10 * time) + 2) + start.y
        return x, y
    
    def ease_in_back(self, time, start: Vector, change: Vector, duration):
        s = self.overshoot
        time /= duration
        x = change.x * time * time * ((s + 1) * time - s) + start.x
        y = change.y * time * time * ((s + 1) * time - s) + start.y
        return x, y

    def ease_out_back(self, time, start: Vector, change: Vector, duration):
        s = self.overshoot
        time /= duration
        time -= 1
        x = change.x * (time * time * ((s + 1) * time + s) + 1) + start.x
        y = change.y * (time * time * ((s + 1) * time + s) + 1) + start.y
        return x, y

    def ease_in_out_back(self, time, start: Vector, change: Vector, duration):    
        s = self.overshoot
        time /= duration/2
        if time < 1:
            s *= 1.525
            x = change.x/2 * time * time * ((s + 1) * time - s) + start.x
            y = change.y/2 * time * time * ((s + 1) * time - s) + start.y
            return x, y
        time -= 2
        s *= 1.525
        x = change.x/2 * (time * time * ((s + 1) * time + s) + 2) + start.x
        y = change.y/2 * (time * time * ((s + 1) * time + s) + 2) + start.y
        return x, y

    def execute_buffer(self):
        if len(self.move_buffer):
            params = self.move_buffer.pop(0)
            self.move_to(params["x"], params["y"], params["duration_s"], params["animation"], params["overshoot"])

    def update(self):
        if self.playing:
            if self.elapsed_time < self.duration:
                self.elapsed_time += GD.get_window().delta_time()
                self.obj.x, self.obj.y = self.animation(self.elapsed_time, self.curr_pos, self.delta_pos, self.duration)
            else:
                self.obj.x = self.destination.x
                self.obj.y = self.destination.y
                self.playing = False
        else:
            self.execute_buffer()
