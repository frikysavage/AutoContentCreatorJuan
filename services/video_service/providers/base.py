from abc import ABC, abstractmethod
from typing import List, Dict

class VideoProvider(ABC):
    @abstractmethod
    def generate_clips(self, guion: str, personajes: List[Dict], ficha_personaje: Dict, formato: str) -> List[str]:
        """
        Generates video clips given a script and character configuration.
        Returns a list of URLs or paths to the generated clips in order.
        """
        pass
