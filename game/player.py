import time
import logging


class Player:
    keyboard = None
    mouse = None

    def __init__(self, keyboard, mouse):
        self.keyboard = keyboard
        self.mouse = mouse

    def init(self):
        logging.warning('waiting 5 sec to activate window')
        time.sleep(5)

    def init_position(self):
        self.keyboard.press_n_times('end', 2)
        self.keyboard.press_n_times('home', 4)
        time.sleep(2)

    def start_fishing(self):
        logging.info('start fishing')
        self.mouse.move(100, 100)
        self.keyboard.press('1')
        time.sleep(3)

    def loot(self, coordinates):
        time.sleep(0.1)
        self.mouse.move(coordinates[0], coordinates[1])
        self.mouse.click('right')
        time.sleep(3)
