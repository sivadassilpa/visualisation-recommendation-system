from abc import ABC, abstractmethod

class VisualizationFactory(ABC):
    @abstractmethod
    def create_visualization(self):
        pass
