import pygame
import pygame.mixer

from core.global_data import GlobalData as GD

pygame.init()
pygame.mixer.init()

pygame.mixer.set_num_channels(32)

class SoundExtra:

    instances = []

    @staticmethod
    def stop_all():
        pygame.mixer.stop()
        for s in SoundExtra.instances:
            s.channel = None

    @staticmethod
    def fade_all(time_ms):
        for s in SoundExtra.instances:
            s.fadeout(time_ms)

    def __init__(self, sound_file, sound_type, volume = 100, loop = True):
        if sound_type not in ["music", "sfx"]:
            raise ValueError("sound_type must be 'music' or 'sfx'")
        self.type = sound_type
        self.loop = loop
        self.sound_file = sound_file
        self.volume = volume
        self.sound = pygame.mixer.Sound(sound_file)
        self.set_volume(self.volume)
        self.channel = None
        self.playing = False
        SoundExtra.instances.append(self)

    def set_volume(self, value):
        if value > 100:
            value = 100
        if value < 0:
            value = 0

        self.volume = value

        match self.type:
            case "music":
                volume = (value / 100) * (GD.get_music_volume() / 100)
            case "sfx":
                volume = (value / 100) * (GD.get_sfx_volume() / 100)

        self.sound.set_volume(volume)
        # O volume setado no final é o volume da instância multiplicado pelo volume global, que é definido em runtime pelo jogador

    def increase_volume(self, value):
        self.set_volume(self.volume * 100 + value)

    def decrease_volume(self, value):
        self.set_volume(self.volume * 100 - value)

    def update_volume(self):
        match self.type:
            case "music":
                volume = (self.volume / 100) * (GD.get_music_volume() / 100)
            case "sfx":
                volume = (self.volume / 100) * (GD.get_sfx_volume() / 100)

        self.sound.set_volume(volume)

    def is_playing(self):
        if self.playing:
            if self.channel:
                self.playing = self.channel.get_busy()
                return self.playing
            self.playing = False
        return False

    def pause(self):
        if self.channel:
            self.channel.pause()
        self.playing = False

    def unpause(self):
        if self.channel:
            self.channel.unpause()
        self.playing = True

    def play(self):
        if self.loop:
            self.channel = self.sound.play(-1)
        else:
            self.channel = self.sound.play()
        self.playing = True

    def stop(self):
        if self.channel:
            self.channel.stop()
        self.playing = False

    def set_repeat(self, repeat):
        self.loop = repeat

    def fadeout(self, time_ms):
        if self.channel:
            self.channel.fadeout(time_ms)
        self.playing = False
