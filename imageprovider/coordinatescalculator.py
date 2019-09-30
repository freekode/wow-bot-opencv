import enum


class Anchor(enum.Enum):
    NW = 1
    NE = 2
    SW = 3
    SE = 4


class CoordinatesCalculator:
    screen_resolution = None
    window_resolution = None
    window_region = None
    header_height = None
    multiplier = None
    anchor = None

    def __init__(self, screen_resolution, window_resolution, multiplier=2, header_height=45):
        self.screen_resolution = (screen_resolution[0] / multiplier, screen_resolution[1] / multiplier)
        self.window_resolution = (window_resolution[0] / multiplier, window_resolution[1] / multiplier)
        self.header_height = header_height / multiplier
        self.multiplier = multiplier
        self.anchor = Anchor.NW
        self.window_region = self.get_window_coordinates()

    def get_window_coordinates(self):
        return (0,
                self.header_height,
                self.window_resolution[0],
                self.window_resolution[1] + self.header_height)

    def get_region_in_window_coordinates(self, x1, y1, x2, y2):
        return (self.window_region[0] + x1 / self.multiplier,
                self.window_region[1] + y1 / self.multiplier,
                self.window_region[0] + x2 / self.multiplier,
                self.window_region[1] + y2 / self.multiplier)

    def get_real_coordinates_from_region(self, x, y, x_region, y_region):
        return ((x / self.multiplier + x_region + self.window_region[0]),
                (y / self.multiplier + y_region + self.window_region[1]))
