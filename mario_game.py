import pygame
from pathlib import Path
from src.utils.constants import NIVEL_1
from arcade_machine_sdk import GameBase, json



class Game(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.num={
        1: None,
        2: self.obtener_grafico("smb-nube-2.png"),
        3: self.obtener_grafico("smb-nube-3.png"),
        4: self.obtener_grafico("smb-nube-4.png"),
        5: self.obtener_grafico("smb-mastil-bola.png"),
        6: self.obtener_grafico("smb-nube-6.png"),
        7: self.obtener_grafico("smb-nube-7.png"),
        8: self.obtener_grafico("smb-nube-8.png"),
        9: self.obtener_grafico("smb-mastil-bandera2.png"),
        10: self.obtener_grafico("smb-mastil-bandera1.png"),
        11: None,
        12: None,
        13: self.obtener_grafico("smb-mastil-1.png"),
        14: self.obtener_grafico("smb-interrogacion.png"),
        15: self.obtener_grafico("smb-block-ladrillo.png"),
        16: self.obtener_grafico("smb-block-piramide.png"),
        17: self.obtener_grafico("smb-mastil-2.png"),
        18: None,
        19: None,
        20: self.obtener_grafico("smb-castillo-20.png"),
        21: self.obtener_grafico("smb-tuberia-arriba-iz.png"),
        22: self.obtener_grafico("smb-tuberia-arriba-de.png"),
        23: self.obtener_grafico("smb-castillo-ventana-de.png"),
        24: self.obtener_grafico("smb-castillo-block-ladrillos.png"),
        25: self.obtener_grafico("smb-castillo-ventana-iz.png"),
        26: self.obtener_grafico("smb-hierba-26.png"),
        27: self.obtener_grafico("smb-tuberia-abajo-iz.png"),
        28: self.obtener_grafico("smb-tuberia-abajo-de.png"),
        29: self.obtener_grafico("smb-castillo-29.png"),
        30: self.obtener_grafico("smb-monticulo-iz.png"),
        31: self.obtener_grafico("smb-monticulo-centro.png"),
        32: self.obtener_grafico("smb-monticulo-de.png"),
        33: self.obtener_grafico("smb-castillo-33.png"),
        34: self.obtener_grafico("smb-monticulo-34.png"),
        35: self.obtener_grafico("smb-monticulo-35.png"),
        36: self.obtener_grafico("smb-hierba-36.png"),
        37: self.obtener_grafico("smb-hierba-37.png"),
        38: self.obtener_grafico("smb-hierba-38.png"),
        39: self.obtener_grafico("smb-castillo-39.png"),
        40: self.obtener_grafico("smb-suelo.png"),
        41: self.obtener_grafico("smb-block-desactivado.png"),
    }
    
    def obtener_grafico(self, nombreArchivo):
            GAME_DIR = Path(__file__).resolve().parent
            ASSETS_DIR = GAME_DIR / "assets"
            IMAGE_PATH = ASSETS_DIR / "img" / nombreArchivo
            img = pygame.image.load(str(IMAGE_PATH))
            escalaX= 53
            escalaY = 53
            image = pygame.transform.scale(img, (escalaX, escalaY))
            image.set_colorkey((255,255,255))
            rect = image.get_rect()
            return (image, rect)
    
    
     
    def handle_events(self, events: list[pygame.event.Event]):
       pass
   
    def update(self, dt: float):
        pass
        
    def render(self):
        # Primero pintamos el fondo para limpiar la pantalla
        surface=self.surface
        surface.fill((100, 170, 180)) # Color azul cielo de Mario
        FILAS= 15
        COLUMNAS=212
        for y in range(FILAS):
            for x in range(COLUMNAS):
                index=y*COLUMNAS+x
                tile=NIVEL_1[index]
                if tile in self.num and self.num[tile] is not None:
                    # Ahora sí, podemos usar [0] con seguridad
                    imagen = self.num[tile][0]
                    surface.blit(imagen, (x * 53, y * 53))
                else:
                    # Si es None, simplemente no hacemos nada y pasamos al siguiente
                    continue
        
        