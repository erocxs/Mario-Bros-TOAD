import pygame 
from src.utils.constantsmario import *
from src.components.hud import *

class moneda(pygame.sprite.Sprite):
    
    ARRAY_DESACTIVADAS = []
    def __init__(self, game, index, x, y, multiplyByTile, marcador=False):
        super().__init__()
        self.game = game
        self.marcador = marcador
        self.BONUS = 200    # 200 ptos
        self.index = index
        self.ARRAY_DESACTIVADAS.append(self.index)
        

        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y

        # Sprite sheet
        self.spritesheet_img_rect = self.game.obtener_grafico("SMB_Sprite_Coin.png")
        self.image = self.spritesheet_img_rect[0]
        self.rect = self.spritesheet_img_rect[1]


        # Posición:
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TX if multiplyByTile else x
        pos_y = y * self.TY if multiplyByTile else y
        self.rect.y = pos_y - self.TY
        print(self.index)

        if self.marcador:
            self.rect.center = (x, y)
            
        else:
            # midbottom: La base de la moneda toca el techo del bloque (pos_y)
            # pos_x + (self.TX // 2): Centra la moneda horizontalmente en el bloque
            self.rect.midbottom = (self.rect.x + (self.TX//2 ), self.rect.y)

        # Movimiento:
        self.vel_y = -2 * self.game.ESCALA
        self.TOPE_RECORRIDO = self.rect.y - (self.TY * 2)

        # Velocidad de las animaciones:
        self.ultimo_update = pygame.time.get_ticks()
        self.VEL_FRAMES_ANIMA = 20

        if not self.marcador:
            self.sonido_coin()
            self.game.hud.coins += 1
            self.game.hud.add_score(200)
           

            if self.index != 2002:
                NIVEL_1[self.index] = 41# cambiarlo a block-desactivado
                
    def sonido_coin(self):
        self.game.sonidos.reproducir("p-ping.mp3")


    def update(self):
        if self.marcador:
            return
        
        if self.rect.y <= self.TOPE_RECORRIDO:
            self.kill()
        
        self.rect.y += self.vel_y
        self.actualizar_animacion()

    
    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()

        if ahora - self.ultimo_update > self.VEL_FRAMES_ANIMA:
            self.ultimo_update = ahora
           