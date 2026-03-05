import pygame
from pathlib import Path
from src.utils.constantsmario import *
from src.components.player import Mario
from src.components.enemies import Goomba
from src.components.moneda import moneda
from src.utils.helpers import *
from src.utils.sonidos import Sonidos
from src.components.hud import *
from src.components.interactive import Flag
from src.components.hongo import hongo

class Level1State:
    def __init__(self, game_reference, hud_reference=None):
        self.game = game_reference 
        self.hud = hud_reference
        if self.hud is not None:
            self.hud.set_world("1-1")
            self.nivel = 1
        self.ESCALA = ESCALA 
        self.TILE_X = TILE_X 
        self.TILE_Y = TILE_Y
        self.FILAS = 15
        self.COLUMNAS = 212
        self.offset_y = 0 
        self.INI_POS_MARIO = (11, 13)
        self.sonidos = Sonidos()
       
        self.iniciar_fundido = False
        self.fade_alpha=0

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
       
        self.listas_sprites = {
        "all_sprites": pygame.sprite.Group(),
            "mario": pygame.sprite.Group(),
            "enemigos": pygame.sprite.Group(),
            "bandera": pygame.sprite.Group(),
            "escenario": pygame.sprite.Group(),
           
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
        ] 
        self.num = biblioteca(self)

        self.TILES_SOLIDOS = [14, 15, 16, 21, 22, 27, 28, 40, 41]
        self.END_WORLD_SCROLL = [2985]
        self.GRAVEDAD = 1.0
        self.lista_triggers = []
        self.instanciar_objetos()
        self.path_musica = self.ASSETS_DIR / "music" / "musica-mario-bros.mp3"

    def obtener_grafico(self, nombreArchivo, colorkey=None):
        IMAGE_PATH = self.ASSETS_DIR / "img" / nombreArchivo
        img = pygame.image.load(str(IMAGE_PATH)).convert_alpha()
        nuevo_ancho = int(img.get_width() * self.ESCALA)
        nuevo_alto = int(img.get_height() * self.ESCALA)
        image = pygame.transform.scale(img, (nuevo_ancho, nuevo_alto))
        
        if colorkey is not None:
            image.set_colorkey(colorkey)
        else:
            image.set_colorkey((255, 255, 255)) 
            
        rect = image.get_rect()
        return (image, rect)

    def instanciar_objetos(self):
        self.game.scroll_x = 0  
        
        for grupo in self.listas_sprites.values():
            grupo.empty()

        self.mario = Mario(self, self.INI_POS_MARIO[0], self.INI_POS_MARIO[1])
        self.listas_sprites["mario"].add(self.mario)
        self.bandera_obj = Flag(self, 197, 4) 
        self.listas_sprites["bandera"].add(self.bandera_obj)
        for pos in self.pos_goombas:
            goomba = Goomba(self, pos[0], pos[1])
            self.listas_sprites["enemigos"].add(goomba)
        
        self.lista_triggers = ColisionadoresInvisibles(self, self.nivel)

    def instanciar_moneda(self, index, x, y, multiplyByTile):
        Moneda = moneda(self, index, x, y, multiplyByTile)
        self.listas_sprites["all_sprites"].add(Moneda)

        self.bandera_obj = Flag(self, 197, 4) 
        self.listas_sprites["bandera"].add(self.bandera_obj)
        
    def instanciar_hongo(self, index, x, y, multiplyByTile, extra=False):
        fungus = hongo(self, index, x, y, multiplyByTile, extra=extra)
        # --- AQUÍ ESTÁ EL CAMBIO MAGICO ---
        self.listas_sprites["enemigos"].add(fungus)
        
    def update(self, dt):
        for lista in self.listas_sprites.values():
            lista.update()

        if not self.mario.secuencia_final:
            mario_mundo_x = self.mario.rect.x + self.game.scroll_x

            for bandera in self.listas_sprites["bandera"]:
                if mario_mundo_x >= bandera.rect.x:
                    self.mario.secuencia_final = True
                    bandera.bajando = True
                    self.mario.acc = 0
                    self.mario.rect.x = bandera.rect.x - self.game.scroll_x
                    self.game.cambiar_musica("gameover_mario.mp3", 0)
                    break

        if hasattr(self, "iniciar_fundido") and self.iniciar_fundido:
            if not hasattr(self, "fade_alpha"): self.fade_alpha = 0

            if self.fade_alpha < 255:
                self.fade_alpha += 4 
            else:
                self.game.cambiar_musica("intro-mario-snes.mp3")
                self.iniciar_fundido = False
                self.fade_alpha = 0
                self.game.estado_actual = "MENU"

    def quitar_vida(self):
            if hasattr(self, 'game'):
                self.game.quitar_vida() 
            else:
                print("Error: No tengo la referencia al juego principal")
                
    def draw(self, surface, Nivel=NIVEL_1):
        surface.fill((100, 170, 180))
        
        tiles_on_screen_x = surface.get_width() // self.TILE_X
        start_tile_x = int(self.game.scroll_x // self.TILE_X)
        self.offset_y = surface.get_height() - (self.FILAS * self.TILE_Y)
        
        for y in range(self.FILAS):
            for x in range(tiles_on_screen_x + 2):
                tile_index = y * self.COLUMNAS + (start_tile_x + x)

                if tile_index >= len(Nivel):
                    continue  
                tile = Nivel[tile_index]
                if self.num[tile] is not None:
                     pantalla_x = x * self.TILE_X - (self.game.scroll_x % self.TILE_X)
                     pantalla_y = (y * self.TILE_Y) + self.offset_y
                     surface.blit(self.num[tile][0], (pantalla_x, pantalla_y))
                else:
                        continue
        for sprite in self.listas_sprites["all_sprites"]:
            surface.blit(sprite.image, (sprite.rect.x - self.game.scroll_x, sprite.rect.y+self.offset_y ))
          
        for enemigo in self.listas_sprites["enemigos"]:
            surface.blit(enemigo.image, (enemigo.rect.x - self.game.scroll_x, enemigo.rect.y))

            if tile_index < len(Nivel):
                    tile = Nivel[tile_index]
                    if self.num[tile] is not None:
                        pantalla_x = x * self.TILE_X - (self.game.scroll_x % self.TILE_X)
                        pantalla_y = (y * self.TILE_Y) + self.offset_y
                        surface.blit(self.num[tile][0], (pantalla_x, pantalla_y))

        for bandera in self.listas_sprites["bandera"]:
            bandera.draw(surface)

        surface.blit(self.mario.image, (self.mario.rect.x, self.mario.rect.y))

        for enemigo in self.listas_sprites["enemigos"]:
            surface.blit(enemigo.image, (enemigo.rect.x - self.game.scroll_x, enemigo.rect.y))

        if hasattr(self, "fade_alpha") and self.fade_alpha > 0:
            fade_surf = pygame.Surface((surface.get_width(), surface.get_height()))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            surface.blit(fade_surf, (0, 0))