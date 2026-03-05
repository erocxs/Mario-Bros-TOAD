import pygame
from src.utils.constantsmario import *
from src.components.player import *

class hongo(pygame.sprite.Sprite):
    ARRAY_DESACTIVADAS = []

    def __init__(self, game, index, x, y, multiplyByTile, extra=False):
        super().__init__()
        self.game = game
        self.extra = extra
        self.BONUS = 1000 
        self.index = index
        hongo.ARRAY_DESACTIVADAS.append(self.index)

        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y

        # Solución de los pixeles blancos: pasamos un color que no esté en el sprite (magenta)
        nombreArchivo = "20241213050648!SMB_1-up_Mushroom_Sprite.png" if self.extra else "SMB_Supermushroom.png"
        self.spritesheet_img_rect = self.game.obtener_grafico(nombreArchivo, colorkey=(255, 0, 255))
        self.image = self.spritesheet_img_rect[0]
        self.rect = self.spritesheet_img_rect[1]

        self.ancho_ssheet = self.image.get_width()
        self.numero_sprites_ssheet = self.ancho_ssheet // self.TX
        self.rango_animacion = (0, 6) 

        self.anim_index = 0
        self.lista_imagenes = []

        # Usamos SRCALPHA para mantener la transparencia intacta
        for i in range(self.numero_sprites_ssheet):
            img = pygame.Surface((self.TX, self.TY), pygame.SRCALPHA)
            img.blit(self.image, (0, 0), (i * self.TX, 0, self.TX, self.TY))
            self.lista_imagenes.append(img)
        
        self.image = self.lista_imagenes[self.anim_index]

        # Posición inicial corregida para que nazca en su bloque
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TX if multiplyByTile else x
        self.rect.x += self.game.game.scroll_x 
        self.rect.y = y * self.TY if multiplyByTile else y
        
        print(f"Hongo instanciado en índice: {self.index}")

        self.vel_x = 1 * self.game.ESCALA
        self.vel_y = 0

        self.DIRECC_VERTICAL = 'ver'
        self.DIRECC_HORIZONTAL = 'hor'
        self.en_suelo = False

        self.ultimo_update = pygame.time.get_ticks()
        self.VEL_FRAMES_ANIMA = 90

        self.WORLD_LIMIT_BOTTOM = (self.game.TILE_Y * self.game.FILAS) + self.game.offset_y

        NIVEL_1[self.index] = 41 
    
    def update(self):
        self.aplicar_gravedad()
        
        self.chequear_colisiones(self.DIRECC_VERTICAL)
        self.chequear_colisiones(self.DIRECC_HORIZONTAL)
        
        self.movimiento()
        self.chequear_colision_mario()

    def chequear_colisiones(self, direccion):
        nivel = NIVEL_1
        ancho_tiles = self.game.COLUMNAS
        
        col_inicio = max(self.rect.left // self.TX, 0)
        col_fin = min(self.rect.right // self.TX + 1, ancho_tiles)
        
        fila_inicio = max((self.rect.top - self.game.offset_y) // self.TY, 0)
        fila_fin = min((self.rect.bottom - self.game.offset_y) // self.TY + 1, self.game.FILAS)

        for fila in range(int(fila_inicio), int(fila_fin)):
            for col in range(int(col_inicio), int(col_fin)):
                index = fila * ancho_tiles + col
                
                if index < len(nivel) and nivel[index] in self.game.TILES_SOLIDOS:
                    tile_rect = pygame.Rect(col * self.TX, 
                                            (fila * self.TY) + self.game.offset_y, 
                                            self.TX, self.TY)
                    
                    if self.rect.colliderect(tile_rect):
                        if direccion == self.DIRECC_VERTICAL:
                            if self.vel_y > 0: 
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.en_suelo = True
                        elif direccion == self.DIRECC_HORIZONTAL:
                            if self.vel_x > 0: 
                                self.rect.right = tile_rect.left
                                self.vel_x *= -1 
                            elif self.vel_x < 0: 
                                self.rect.left = tile_rect.right
                                self.vel_x *= -1 

    def aplicar_gravedad(self):
        self.vel_y += self.game.GRAVEDAD
        self.rect.y += int(self.vel_y)
        self.en_suelo = False

    def movimiento(self):
        self.rect.x += self.vel_x
        if self.rect.y > self.WORLD_LIMIT_BOTTOM:
            print("item-eliminado")
            self.kill()

    def chequear_colision_mario(self):
        mario = list(self.game.listas_sprites["mario"])[0]
        
        hongo_rect_camara = self.rect.copy()
        hongo_rect_camara.x -= self.game.game.scroll_x
        
        if mario.rect.colliderect(hongo_rect_camara):
            if not self.extra:
                mario.crecer() 
            else:
                self.game.hud.score += 0 
            
            self.game.hud.add_score(self.BONUS)
            try:
                self.game.sonidos.reproducir("smb_powerup.wav")
            except:
                pass
            
            self.kill()