from PPlay.keyboard import Keyboard

class KeyboardExtra(Keyboard):
    _clicked_keys = []

    def __init__(self) -> None:
        super().__init__()

    def key_clicked(self, key):
        if self.key_pressed(key):
            if key not in KeyboardExtra._clicked_keys:
                KeyboardExtra._clicked_keys.append(key)
                return True
            else:
                return False
        elif key in KeyboardExtra._clicked_keys:
            KeyboardExtra._clicked_keys.remove(key)
        return False