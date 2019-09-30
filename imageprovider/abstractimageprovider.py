from abc import ABC, abstractmethod


class AbstractImageProvider(ABC):
    @abstractmethod
    def get_image_numpy_array(self, coordinates):
        pass
