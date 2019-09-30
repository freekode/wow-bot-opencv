import cv2 as cv
import imageprovider

methods = ['cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


class BobberFinder:
    templates = None
    threshold = None
    fishing_region = None
    image_provider = None
    coordinates_calculator = None

    def __init__(self,
                 template_filenames: [],
                 threshold: float,
                 fishing_region_size: (),
                 image_provider: imageprovider.MssImageProvider,
                 coordinates_calculator: imageprovider.CoordinatesCalculator):
        self.threshold = threshold
        self.image_provider = image_provider
        self.coordinates_calculator = coordinates_calculator

        self.templates = self.__get_templates(template_filenames)
        self.fishing_region = self.__get_fishing_region(fishing_region_size)

    def find_bobber_coordinates(self):
        fishing_region_image = self.image_provider.get_image_numpy_array(self.fishing_region)
        fishing_region_image = self.__prepare_image(fishing_region_image)

        bobber_region_coordinates = self.__find_bobber_coordinates(fishing_region_image)
        if bobber_region_coordinates is None:
            return None

        real_coordinates = self.coordinates_calculator.get_real_coordinates_from_region(
            bobber_region_coordinates[1][0], bobber_region_coordinates[1][1],
            self.fishing_region[0], self.fishing_region[1])
        return real_coordinates, bobber_region_coordinates[3]

    def find_bobber_coordinates_for_template(self, template):
        fishing_region_image = self.image_provider.get_image_numpy_array(self.fishing_region)
        fishing_region_image = self.__prepare_image(fishing_region_image)

        bobber_region_coordinates = self.__find_bobber_coordinates_for_template(fishing_region_image, template)
        if bobber_region_coordinates is None:
            return None

        real_coordinates = self.coordinates_calculator.get_real_coordinates_from_region(
            bobber_region_coordinates[1][0], bobber_region_coordinates[1][1],
            self.fishing_region[0], self.fishing_region[1])
        return real_coordinates, bobber_region_coordinates[3]

    def __find_bobber_coordinates(self, image):
        max_value_coordinates = (0, (0, 0), (0, 0), None)
        for template in self.templates:
            coordinates = self.__find_bobber_coordinates_for_template(image, template)
            if coordinates is not None and coordinates[0] > max_value_coordinates[0]:
                max_value_coordinates = coordinates

        if max_value_coordinates[0] == 0:
            return None
        return max_value_coordinates

    def __find_bobber_coordinates_for_template(self, image, template):
        result = cv.matchTemplate(image, template.image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val >= self.threshold:
            return (
                max_val,
                (max_loc[0], max_loc[1]),
                (max_loc[0] + template.width, max_loc[1] + template.height),
                template)
        return None

    def __prepare_image(self, fishing_region_image):
        return cv.cvtColor(fishing_region_image, cv.COLOR_BGR2GRAY)

    def __get_templates(self, filenames):
        return list(map(lambda filename: TemplateImage.create_template(filename), filenames))

    def __get_fishing_region(self, region_size):
        return self.coordinates_calculator.get_region_in_window_coordinates(
            region_size[0], region_size[1], region_size[2], region_size[3])


class TemplateImage:
    image = None
    width = None
    height = None

    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height

    @staticmethod
    def create_template(filename):
        image = cv.imread(filename, 0)
        w, h = image.shape[::-1]
        return TemplateImage(image, w, h)
