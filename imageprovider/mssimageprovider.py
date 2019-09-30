import pyscreenshot
import numpy
import mss
import mss.tools
from .abstractimageprovider import AbstractImageProvider


class MssImageProvider(AbstractImageProvider):
    save_image = False

    def get_image_numpy_array(self, coordinates):
        bobber_image = self.get_image_mss(coordinates)
        return numpy.array(bobber_image)

    def get_image_mss(self, coordinates):
        with mss.mss() as sct:
            monitor = {
                'top': coordinates[1],
                'left': coordinates[0],
                'width': coordinates[2] - coordinates[0],
                'height': coordinates[3] - coordinates[1]}
            image = sct.grab(monitor)
            if self.save_image:
                output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
                mss.tools.to_png(image.rgb, image.size, output=output)

            return image
