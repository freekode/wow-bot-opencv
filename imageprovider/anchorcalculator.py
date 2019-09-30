from abc import ABC, abstractmethod


class AnchorCalculator(ABC):
    @abstractmethod
    def calculate(self):
        pass

