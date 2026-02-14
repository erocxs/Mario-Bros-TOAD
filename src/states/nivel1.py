import pygame
from pathlib import Path
from src.utils.constants import *
from arcade_machine_sdk import GameBase, json

class Level1State:
    def __init__(self):
        # 1. Definimos la ruta a assets subiendo dos niveles desde src/states
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        self.scroll_x=0
        # 2. El diccionario de tu amiga (usando self.obtener_grafico)
        self.num = biblioteca(self)

    def obtener_grafico(self, nombreArchivo):
        # Ajustado para usar la ruta dinámica
        IMAGE_PATH = self.ASSETS_DIR / "img" / nombreArchivo
        img = pygame.image.load(str(IMAGE_PATH))
        image = pygame.transform.scale(img, (53, 53))
        image.set_colorkey((255, 255, 255))
        rect = image.get_rect()
        return (image, rect)

    def update(self, dt):
        keys= pygame.key.get_pressed() #toma que tecla se esta presionando 
        #K_RIGHT SERIA LA FLECHA HACIA LA DERECHA
        if keys[pygame.K_RIGHT]:
            self.scroll_x += 5
        #K_LEFT SERIA LA FLECHA HACIA LA IZQUIERDA  
        if keys[pygame.K_LEFT]:
            self.scroll_x -= 5

        # Limitar el scroll para no salirte del mapa (opcional pero recomendado)
        if self.scroll_x < 0: 
            self.scroll_x = 0
    
    # El límite derecho sería: (Columnas * AnchoTile) - AnchoPantalla
        limite_derecho = (212 * 53) - 1024 
        if self.scroll_x > limite_derecho:
            self.scroll_x = limite_derecho

    def draw(self, surface, Nivel=NIVEL_1):
         surface.fill((100, 170, 180))
         TILE_X=53 #ancho del bloque
         TILE_Y=53 #alto del bloque
         FILAS = 15
         COLUMNAS = 212 
    # Dividimos el ancho de la pantalla (1024) entre el ancho del bloque (32).
    # Esto evita procesar las 212 columnas si solo vemos 32.
         tiles_on_screen_x = surface.get_width() // TILE_X
    # Si te has movido 64 píxeles (scroll_x = 64) y cada bloque mide 32,
    # el start_tile_x será 2. Empezaremos a dibujar desde la columna 2.
         start_tile_x = int(self.scroll_x // TILE_X)
    # Como Pygame dibuja desde arriba (Y=0), restamos la altura del mapa (15 filas * 32px)
    # a la altura de la pantalla (768px) para que el suelo quede abajo.
         offset_y = surface.get_height() - (FILAS * TILE_Y)

    # EMPIEZA EL DIBUJO
         for y in range(FILAS):
        # Solo recorremos las columnas que caben en la pantalla (+1 para el borde derecho).
            for x in range(tiles_on_screen_x + 1):  
            # (y * 212) salta a la fila correcta.
            # (start_tile_x + x) se mueve a la columna correcta según la cámara.
                tile_index = y * COLUMNAS + (start_tile_x + x)

            # Verificación de seguridad: No intentar leer fuera de la lista.
                if tile_index >= len(Nivel):
                    continue  

            # Obtenemos el número del bloque (ID)
                tile = Nivel[tile_index]

            # Solo dibujamos si el ID no es "None" (como el cielo).
                if self.num[tile] is not None:
                # Usamos el módulo (%) para saber cuántos píxeles "sobran".
                # Esto permite que los bloques se deslicen suavemente píxel a píxel.
                     pantalla_x = x * TILE_X - (self.scroll_x % TILE_X)
                # Aplicamos la fila multiplicada por el tamaño + el offset del suelo.
                     pantalla_y = (y * TILE_Y) + offset_y
                
                # Dibujamos la imagen (posición [0] de tu diccionario) en la pantalla.
                     surface.blit(self.num[tile][0], (pantalla_x, pantalla_y))
                else:
    # Si el bloque es None (como el cielo), no hacemos nada y pasamos al siguiente
                        continue
        