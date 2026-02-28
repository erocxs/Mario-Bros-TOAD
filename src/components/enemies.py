import pygame
from src.utils.constantsmario import *



class Goomba(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y

        # Sprite sheet
        self.spritesheet_img_rect = self.game.obtener_grafico("goomba-ssheet.png")
        self.image = self.spritesheet_img_rect[0]
        self.rect = self.spritesheet_img_rect[1]

        self.ancho_ssheet = self.image.get_width()
        self.alto_ssheet = self.image.get_height()
        self.numero_sprites_ssheet = self.ancho_ssheet // self.TX
        self.rango_animacion = (0, 2) # fotogramas animacion-goomba (0, 1)

        # Recorte de sprites y los almacenamos individualmente en una LISTA:
        self.anim_index = 0
        self.lista_imagenes = []

        for i in range(self.numero_sprites_ssheet):
            img = pygame.Surface((self.TX, self.TY))
            color_fondo = self.image.get_at((0, 0)) 
            img.fill(color_fondo)
            img.blit(self.image, (0, 0), (i * self.TX, 0, self.TX, self.TY))
            img.set_colorkey(color_fondo)
            self.lista_imagenes.append(img.convert_alpha())
        
        self.image = self.lista_imagenes[self.anim_index]
        # Posición y velocidad
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TX
        self.rect.y = y * self.TY
        self.vel_x = -2
        self.vel_y = 0
        # Activo / Parado:
        self.activo = False
        self.DISTANCIA_ACTIVACION = 16 * self.TX #esto es para que el goomba se active (camine) cuando este dentro de la camara
        # CONST 'horizontal' y 'vertical':
        self.DIRECC_VERTICAL = 'ver'
        self.DIRECC_HORIZONTAL = 'hor'
        # Velocidad de las animaciones:
        self.ultimo_update = pygame.time.get_ticks()
        self.VEL_ANIMACION = 270
    
    
    
    def update(self):
        self.aplicar_gravedad()
        self.actualizar_animacion()
        manejar_colisiones_obstaculos(self, self.DIRECC_VERTICAL)

        self.movimiento()
        manejar_colisiones_obstaculos(self, self.DIRECC_HORIZONTAL)
       
        
    
    def actualizar_animacion(self):
       
        ahora = pygame.time.get_ticks()

        if ahora - self.ultimo_update > self.VEL_ANIMACION:
            self.ultimo_update = ahora
            self.anim_index += 1

            if self.anim_index >= self.rango_animacion[1]:
                self.anim_index = self.rango_animacion[0]

            self.image = self.lista_imagenes[self.anim_index]
            
    def aplicar_gravedad(self):
        self.vel_y += self.game.GRAVEDAD
        self.rect.y += int(self.vel_y)     
        
           
    def movimiento(self):
        """Goombas inicialmente quietos hasta que Mario este cerca"""
        if not self.activo and abs(self.get_pos_x_mario() - self.rect.x) <= self.DISTANCIA_ACTIVACION:
            self.activo = True
        
        if self.activo:
             self.rect.x += self.vel_x
    
    
    def get_pos_x_mario(self):
        return self.game.game.scroll_x + self.game.INI_POS_MARIO[0] * self.TX