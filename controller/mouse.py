import time
import autopy

button_mapping = {
    'left': autopy.mouse.Button.LEFT,
    'middle': autopy.mouse.Button.MIDDLE,
    'right': autopy.mouse.Button.RIGHT
}


class Mouse:
    def move(self, x, y):
        autopy.mouse.move(x, y)

    def click(self, button):
        autopy.mouse.click(button_mapping[button])
