import pyscreenshot
import matplotlib.pyplot as plt
import imageprovider
import processor
import time
import controller
import game
import logging

screen_resolution = 3840, 2400
window_resolution = 2048, 1280
fishing_region_size = 500, 300, 500 + 1048, 300 + 600
templates = ['templates/template.png', 'templates/template1.png',
             'templates/template2.png', 'templates/template3.png',
             'templates/template4.png', 'templates/template5.png',
             'templates/template6.png']
threshold = 0.70
fishing_time_sec = 30


def main():
    logging.basicConfig(level=logging.INFO)

    keyboard = controller.Keyboard()
    mouse = controller.Mouse()
    player = game.Player(keyboard, mouse)
    bobber_finder = get_bobber_finder()

    player.init()

    for i in range(20):
        print('attempt ' + str(i))
        fishing(player, bobber_finder)


def fishing(player, bobber_finder):
    bobber_coordinates = get_initial_bobber(bobber_finder, player)
    if bobber_coordinates is None:
        logging.warning('cant find bobber for first time')
        return

    start_time = time.time()

    while True:
        if (time.time() - start_time) >= fishing_time_sec:
            logging.info('didnt catch it')
            break

        new_bobber_coordinates = bobber_finder.find_bobber_coordinates_for_template(bobber_coordinates[1])
        if new_bobber_coordinates is None:
            logging.info('take it! ' + str(bobber_coordinates))
            player.loot(bobber_coordinates[0])
            return

        print('bobber ' + str(new_bobber_coordinates))
        time.sleep(0.25)


def get_initial_bobber(bobber_finder, player):
    player.start_fishing()
    bobber_coordinates = bobber_finder.find_bobber_coordinates()
    if bobber_coordinates is not None:
        return bobber_coordinates
    return None


def get_bobber_finder():
    calculator = imageprovider.CoordinatesCalculator(screen_resolution, window_resolution)
    image_provider = imageprovider.MssImageProvider()
    return processor.BobberFinder(templates, threshold, fishing_region_size, image_provider, calculator)


if __name__ == '__main__':
    main()
