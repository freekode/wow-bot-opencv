import time
import keyboard as python_keyboard


class Keyboard:
    def press_n_times(self, key, times):
        for x in range(0, times - 1):
            self.press(key)
            time.sleep(0.1)

    def press(self, key):
        python_keyboard.send(key)
