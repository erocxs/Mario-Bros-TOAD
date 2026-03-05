import pygame
from src.utils.constantsmario import *
from src.components.player import *



class hongo(pygame.sprite.Sprite):
    ARRAY_DESACTIVADAS = []

    def __init__(self, game, index, x, y, multiplyByTile, extra=False):
        super().__init__()
        self.game = game
        self.extra = extra
        self.BONUS = 1000    # 1000 ptos
        self.index = index
        hongo.ARRAY_DESACTIVADAS.append(self.index)

        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y

        # Sprite sheet
        nombreArchivo = "20241213050648!SMB_1-up_Mushroom_Sprite.png" if self.extra else "SMB_Supermushroom.png"
        self.spritesheet_img_rect = self.game.obtener_grafico(nombreArchivo)
        self.image = self.spritesheet_img_rect[0]
        self.rect = self.spritesheet_img_rect[1]

        self.ancho_ssheet = self.image.get_width()
        self.numero_sprites_ssheet = self.ancho_ssheet // self.TX
        self.rango_animacion = (0, 6) # fotogramas animacion-goomba (0, 1, 2, 3, 4, 5)

        # Recorte de sprites y los almacenamos individualmente en una LISTA:
        self.anim_index = 0
        self.lista_imagenes = []

        for i in range(self.numero_sprites_ssheet):
            img = pygame.Surface((self.TX, self.TY), pygame.SRCALPHA)
            img.blit(self.image, (0, 0), (i * self.TX, 0, self.TX, self.TY))
            # img.set_colorkey((255, 255, 255))
            self.lista_imagenes.append(img)
        
        # for i in range(self.numero_sprites_ssheet):
        #     img = pygame.Surface((self.TX, self.TY))
        #     color_fondo = self.image.get_at((0, 0)) 
        #     img.fill(color_fondo)
        #     img.blit(self.image, (0, 0), (i * self.TX, 0, self.TX, self.TY))
        #     img.set_colorkey(color_fondo)
        #     self.lista_imagenes.append(img)
        # self.image = self.lista_imagenes[self.anim_index]
        
       

        # Posición:
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TX if multiplyByTile else x
        self.rect.x += self.game.game.scroll_x
        self.rect.y = y * self.TY if multiplyByTile else y
        print(self.index)

        # Movimiento:
        self.vel_x = 1 * self.game.ESCALA
        self.vel_y = 0

      
        # CONST 'horizontal' y 'vertical':
        self.DIRECC_VERTICAL = 'ver'
        self.DIRECC_HORIZONTAL = 'hor'

        # Velocidad de las animaciones:
        self.ultimo_update = pygame.time.get_ticks()
        self.VEL_FRAMES_ANIMA = 90

        # World-limit-bottom:
        self.WORLD_LIMIT_BOTTOM = self.game.TILE_Y * self.game.FILAS

        # Bonificacion 1000ptos:
        #self.sonido_seta()
        self.game.hud.add_score(self.BONUS)
        NIVEL_1[self.index] = 41# cambiarlo a block-desactivado
    
    






    def update(self):
      
        self.aplicar_gravedad()
        
        self.chequear_colisiones(self.DIRECC_VERTICAL)

        # 3. Movimiento horizontal
        
        self.chequear_colisiones(self.DIRECC_HORIZONTAL)
        
        # 4. Límites
        self.movimiento()
        manejar_colisiones_obstaculos(self, self.DIRECC_VERTICAL)
        

        
        
    def chequear_colisiones(self, direccion):
        # Usamos la lista de sólidos del nivel
        col_inicio = max(self.rect.left // self.TX, 0)
        col_fin = min(self.rect.right // self.TX + 1, self.game.COLUMNAS)
        fila_inicio = max(self.rect.top // self.TY, 0)
        fila_fin = min(self.rect.bottom // self.TY + 1, self.game.FILAS)

        for fila in range(int(fila_inicio), int(fila_fin)):
            for col in range(int(col_inicio), int(col_fin)):
                index = fila * self.game.COLUMNAS + col
                if index < len(NIVEL_1) and NIVEL_1[index] in self.game.TILES_SOLIDOS:
                    tile_rect = pygame.Rect(col * self.TX, fila * self.TY, self.TX, self.TY)
                    
                    if self.rect.colliderect(tile_rect):
                        if direccion == self.DIRECC_VERTICAL:
                            if self.vel_y > 0: # Cayendo
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                        elif direccion == self.DIRECC_HORIZONTAL:
                            if self.vel_x > 0: # Hacia la derecha
                                self.rect.right = tile_rect.left
                                self.vel_x *= -1 # Rebota
                            elif self.vel_x < 0: # Hacia la izquierda
                                self.rect.left = tile_rect.right
                                self.vel_x *= -1 # Rebota
    
   
             






    def aplicar_gravedad(self):
        self.vel_y += self.game.GRAVEDAD
        self.rect.y += int(self.vel_y)
    









    def movimiento(self):
        self.rect.x += self.vel_x

        
        if self.rect.y > self.WORLD_LIMIT_BOTTOM:
            print("item-eliminado")
            self.kill()
    







    # def sonido_seta(self):
    #     self.game.sonidos.reproducir("seta")