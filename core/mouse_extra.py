from PPlay.mouse import Mouse

class MouseExtra(Mouse):
    _clicked_buttons = []

    def __init__(self):
        super().__init__()

    def is_button_clicked(self, button):
        if self.is_button_pressed(button):
            if button not in MouseExtra._clicked_buttons:
                MouseExtra._clicked_buttons.append(button)
                return True
            else:
                return False
        elif button in MouseExtra._clicked_buttons:
            MouseExtra._clicked_buttons.remove(button)
        return False