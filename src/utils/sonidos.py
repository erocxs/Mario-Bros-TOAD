import pygame
from pathlib import Path


class Sonidos:
    def __init__(self):
        self.BASE_DIR=Path(__file__).resolve().parent.parent.parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        
    

    

    def reproducir(self, nombre_archivo, volumen=1.0):
        """Carga un sonido específico con el volumen indicado."""
        ruta = self.ASSETS_DIR / "sounds" / nombre_archivo
        sonido = pygame.mixer.Sound(str(ruta))
        sonido.set_volume(0.5)
        sonido.play()
        return sonido

    