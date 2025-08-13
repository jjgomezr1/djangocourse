from abc import ABC, abstractmethod
from django.http import HttpRequest

class IStorage(ABC):
    @abstractmethod
    def save(self, file, filename: str) -> str:
        """Guarda un archivo y devuelve la ruta o URL"""
        pass