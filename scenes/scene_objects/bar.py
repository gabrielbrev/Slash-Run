from PPlay.sprite import Sprite

class Bar(Sprite):
    def __init__(self, initial_value, image_file, frames):
        super().__init__(image_file, frames)
        self.value = initial_value
        self.playing = False

    def set_value(self, value):
        if 0 <= value < self.total_frames:
            self.value = value

    def get_value(self):
        return self.value
    
    def is_maxed(self):
        return self.value == self.total_frames - 1

    def increment(self):
        if self.value < self.total_frames:
            self.value += 1
    
    def decrement(self):
        if self.value > 0:
            self.value -= 1

    def update(self):
        super().update()
        if self.value != self.get_curr_frame():
            self.set_curr_frame(self.value)