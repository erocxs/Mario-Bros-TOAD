import pygame
from pathlib import Path
from src.utils.constantsmario import *
from src.components.player import Mario
from src.components.enemies import Goomba


class Level1State:
    def __init__(self, game_reference, hud_reference=None):
        self.game = game_reference 
        self.hud = hud_reference
        if self.hud is not None:
            self.hud.set_world("1-1")
            self.nivel = 1
        self.ESCALA = ESCALA #variable para escalar los tiles al tamaño que queramos
        self.TILE_X = TILE_X #ancho del bloque
        self.TILE_Y = TILE_Y#alto del bloque
        self.FILAS = 15
        self.COLUMNAS = 212
        self.offset_y = 0 
        self.INI_POS_MARIO = (11, 13)

        # 1. Definimos la ruta a assets subiendo dos niveles desde src/states
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        #self.scroll_x=0
        self.listas_sprites = {
        "all_sprites": pygame.sprite.Group(),
            "mario": pygame.sprite.Group(),
            "enemigos": pygame.sprite.Group(),
            "bandera": pygame.sprite.Group(),
            "escenario": pygame.sprite.Group(),
            "textos": pygame.sprite.Group(),
    }
        self.pos_goombas = [
            (24, 13),
            (50, 13), (52, 13),
            (83, 1), (85, 1),
            (98, 13), (100, 13),
            (112, 13), (114, 13),
            (124, 13), (126, 13),
            (130, 13), (132, 13),
            (173, 13), (175, 13)
        ] #posiciones en las que van a aparecer los goombas en el nivel 1
        self.num = biblioteca(self)

        self.TILES_SOLIDOS = [14, 15, 16, 21, 22, 27, 28, 40, 41]
        self.END_WORLD_SCROLL = [2985]
        self.GRAVEDAD = 1.0
        self.instanciar_objetos()
        self.path_musica = self.ASSETS_DIR / "music" / "musica-mario-bros.mp3"


    def obtener_grafico(self, nombreArchivo):
        # Ajustado para usar la ruta dinámica
        IMAGE_PATH = self.ASSETS_DIR / "img" / nombreArchivo
        img = pygame.image.load(str(IMAGE_PATH)).convert_alpha()
        image = pygame.transform.scale(img, (img.get_width() * self.ESCALA, img.get_height()* self.ESCALA))
        image.set_colorkey((255, 255, 255))
        rect = image.get_rect()
        return (image, rect)


    def instanciar_objetos(self):
        # VACIAR TODO: Si no haces esto, los Marios se acumulan
        self.listas_sprites["all_sprites"].empty()
        self.listas_sprites["mario"].empty()
        self.listas_sprites["enemigos"].empty()

        # Crear el nuevo Mario
        self.mario = Mario(self, 11, 13)
        
        # Añadirlo a los grupos limpios
        self.listas_sprites["all_sprites"].add(self.mario)
        self.listas_sprites["mario"].add(self.mario)

        # Re-crear enemigos
        for pos in self.pos_goombas:
            goomba = Goomba(self, pos[0], pos[1])
            self.listas_sprites["enemigos"].add(goomba)
        
        
        
        
    def update(self, dt):
       
        self.listas_sprites["all_sprites"].update()
        self.listas_sprites["enemigos"].update()

    def quitar_vida(self):
        # Esta función llama a la del juego principal (mario_game.py)
        # Asegúrate de que en el __init__ guardaste la referencia como self.game
        if hasattr(self, 'game'):
            self.game.quitar_vida() 
        else:
            print("Error: No tengo la referencia al juego principal")
            
            
    def draw(self, surface, Nivel=NIVEL_1):
         surface.fill((100, 170, 180))
         
         TILE_X=32 #ancho del bloque
         TILE_Y=32 #alto del bloque 
    # Dividimos el ancho de la pantalla (1024) entre el ancho del bloque (32).
    # Esto evita procesar las 212 columnas si solo vemos 32.
         tiles_on_screen_x = surface.get_width() // self.TILE_X
         start_tile_x = int(self.game.scroll_x // self.TILE_X)
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
                     pantalla_x = x * self.TILE_X - (self.game.scroll_x % self.TILE_X)
                     pantalla_y = (y * self.TILE_Y) + self.offset_y
                     surface.blit(self.num[tile][0], (pantalla_x, pantalla_y))
                else:
                # Si el bloque es None (como el cielo), no hacemos nada y pasamos al siguiente
                        continue
         self.listas_sprites["all_sprites"].draw(surface)
         #self.listas_sprites["mario"].draw(surface)
         for enemigo in self.listas_sprites["enemigos"]:
            surface.blit(enemigo.image, (enemigo.rect.x - self.game.scroll_x, enemigo.rect.y))