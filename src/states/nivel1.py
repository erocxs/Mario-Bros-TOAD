import pygame
from pathlib import Path
from src.utils.constantsmario import *
from src.components.player import Mario


class Level1State:
    def __init__(self):
        self.nivel = 1
        self.ESCALA = ESCALA #variable para escalar los tiles al tamaño que queramos
        self.TILE_X = TILE_X #ancho del bloque
        self.TILE_Y = TILE_Y#alto del bloque
        self.FILAS = 15
        self.COLUMNAS = 212
        self.offset_y = 0
        
        # 1. Definimos la ruta a assets subiendo dos niveles desde src/states
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        self.scroll_x=0
        self.listas_sprites = {
        "all_sprites": pygame.sprite.Group(),
        
    }
        self.num = biblioteca(self)
        self.TILES_SOLIDOS = [14, 15, 16, 21, 22, 27, 28, 40, 41]
        self.END_WORLD_SCROLL = [2985]
        self.GRAVEDAD = 1.0
        self.instanciar_objetos()

    def obtener_grafico(self, nombreArchivo):
        # Ajustado para usar la ruta dinámica
        IMAGE_PATH = self.ASSETS_DIR / "img" / nombreArchivo
        img = pygame.image.load(str(IMAGE_PATH)).convert_alpha()
        image = pygame.transform.scale(img, (img.get_width() * self.ESCALA, img.get_height()* self.ESCALA))
        image.set_colorkey((255, 255, 255))
        rect = image.get_rect()
        return (image, rect)


    def instanciar_objetos(self):
        """Instanciar/re-instanciar Mario, enemigos, etc..."""
        # Instanciar Mario:
        self.mario = Mario(self, 11,13)
       
        self.listas_sprites["all_sprites"].add(self.mario)
        
        
    def update(self, dt):
       
        self.listas_sprites["all_sprites"].update()
      
            
   


    def draw(self, surface, Nivel=NIVEL_1):
         surface.fill((100, 170, 180))
         
         TILE_X=32 #ancho del bloque
         TILE_Y=32 #alto del bloque 
    # Dividimos el ancho de la pantalla (1024) entre el ancho del bloque (32).
    # Esto evita procesar las 212 columnas si solo vemos 32.
         tiles_on_screen_x = surface.get_width() // self.TILE_X
         start_tile_x = int(self.scroll_x // self.TILE_X)
         self.offset_y = surface.get_height() - (self.FILAS * self.TILE_Y)
         
         for y in range(self.FILAS):
        # Solo recorremos las columnas que caben en la pantalla (+1 para el borde derecho).
            for x in range(tiles_on_screen_x + 2):  
                tile_index = y * self.COLUMNAS + (start_tile_x + x)
            # Verificación de seguridad: No intentar leer fuera de la lista.
                if tile_index >= len(Nivel):
                    continue  
            # Obtenemos el número del bloque (ID)
                tile = Nivel[tile_index]
            # Solo dibujamos si el ID no es "None" (como el cielo).
                if self.num[tile] is not None:
                     pantalla_x = x * self.TILE_X - (self.scroll_x % self.TILE_X)
                     pantalla_y = (y * self.TILE_Y) + self.offset_y
                     surface.blit(self.num[tile][0], (pantalla_x, pantalla_y))
                else:
                # Si el bloque es None (como el cielo), no hacemos nada y pasamos al siguiente
                        continue
         self.listas_sprites["all_sprites"].draw(surface)
         #self.listas_sprites["mario"].draw(surface)