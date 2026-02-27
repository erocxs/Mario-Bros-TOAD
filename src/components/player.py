import pygame
from src.utils.constantsmario import *


class Mario(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.TX = TILE_X
        self.TY = TILE_Y

        # Sprite sheet
        self.spritesheet_img_rect = self.game.obtener_grafico("mario-ss1.png") #guarda un tuple que tiene la imagen del mario y la hitbox
        self.image = self.spritesheet_img_rect[0] #imagen
        self.rect = self.spritesheet_img_rect[1] #hitbox de toda la imagen
        self.ancho_imagen = self.image.get_width()
        self.alto_imagen = self.image.get_height()
        self.numero_sprites_ssheet = self.ancho_imagen // self.TX #calcula cuantos marios hay en la imagen, Si la imagen mide 480 y cada bloque (TX) mide 48, el resultado es 10.
        self.rango_animacion = (1, 4)
        
        # Recorte de sprites y los almacenamos individualmente en una LISTA:
        self.anim_index = 0
        self.lista_imagenes = []

        for i in range(self.numero_sprites_ssheet):
            img = pygame.Surface((self.TX, self.TY), pygame.SRCALPHA)
            img.blit(self.image, (0, 0), (i * self.TX, 0, self.TX, self.TY))
            self.lista_imagenes.append(img)
        
        self.image = self.lista_imagenes[self.anim_index]
        
         # Posición y velocidad
        self.rect = self.image.get_rect() #hitbox del mario
        self.rect.x = x * self.TX
        self.rect.y = y * self.TY
        self.rect.inflate_ip(-2, 0)
         # Dirección, aceleracion, limites y físicas:
        # VALORES RELATIVOS A LA HORIZONTAL:
        self.DIRECC_HORIZONTAL = 'hor'
        self.acc = 0    # Aceleracion (vel) del personaje
        self.acc_acum = 0   # Aceleracion-acumulada (solo para poder saltar más)
        self.flip = False
        self.VEL_MAX = 7.5
        self.ACELERACION = 0.14
        self.DECELERACION = 0.2
       # VALORES RELATIVOS A LA VERTICAL:
        self.DIRECC_VERTICAL = 'ver'
        self.vel_y = 0
        self.GRAVEDAD = self.game.GRAVEDAD
        self.en_suelo = False
        self.saltando = False
        self.POTENCIA_SALTO = -16
        # Velocidad de las animaciones:
        self.ultimo_update = pygame.time.get_ticks()
        self.VEL_FRAMES_ANIMA = 90
        
    def update(self):
        self.mover() 
        self.animacion()
        
    def mover(self):
        """Controles-Mario y movimiento (vertical y horizontal)"""

        self.aplicar_gravedad()

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            
            self.gestionar_aceleracion(self.flip)
            self.flip = True
        
        elif teclas[pygame.K_RIGHT]:
            
            self.gestionar_aceleracion(self.flip)
            self.flip = False
        
        else:
            if self.acc > 0:
                self.acc -= self.DECELERACION
                self.acc = 0 if self.acc < 0 else self.acc

                self.acc_acum -= self.DECELERACION
                self.acc_acum = 0 if self.acc_acum < 0 else self.acc_acum

            else:
                self.acc += self.DECELERACION
                self.acc = 0 if self.acc > 0 else self.acc

                self.acc_acum += self.DECELERACION
                self.acc_acum = 0 if self.acc_acum > 0 else self.acc_acum
                
        
        if teclas[pygame.K_SPACE]:
            self.saltar()
        
        self.manejar_colisiones_obstaculos(self.DIRECC_HORIZONTAL)

        # Mover scroll (mario no se mueve realmente):
        self.game.scroll_x += self.acc
        self.limites_mundo()
        
    def gestionar_aceleracion(self, flip):
        if flip:
            self.acc -= self.ACELERACION
            self.acc = -self.VEL_MAX if self.acc < -self.VEL_MAX else self.acc

            self.acc_acum -= self.ACELERACION
            self.acc_acum = -self.VEL_MAX if self.acc_acum < -self.VEL_MAX else self.acc_acum
            
        else:
            self.acc += self.ACELERACION
            self.acc = self.VEL_MAX if self.acc > self.VEL_MAX else self.acc

            self.acc_acum += self.ACELERACION
            self.acc_acum = self.VEL_MAX if self.acc_acum > self.VEL_MAX else self.acc_acum
            
    
    def aplicar_gravedad(self):
        self.vel_y += self.GRAVEDAD
        self.rect.y += int(self.vel_y)
        self.en_suelo = False  # se actualizará en colisiones

        self.manejar_colisiones_obstaculos(self.DIRECC_VERTICAL)
        
   
    def saltar(self):
        if self.en_suelo:
            self.vel_y = self.POTENCIA_SALTO 
            self.en_suelo = False
            #self.saltando = True
            #self.game.sonidos.reproducir("salto")
    
            
            
            
    def manejar_colisiones_obstaculos(self, hor_ver):
        #Checkeamos los tiles del escenario que son 'solidos' (bloques, suelo, tuberias)
        nivel = NIVEL_1
        ancho_tiles = self.game.COLUMNAS
        alto_tiles = len(nivel) // ancho_tiles

        mario_rect = self.rect
        

        # Determinar el área de tiles a revisar cerca de Mario
        margen_tiles = 2  # chequeamos un margen alrededor de Mario

        # Calculamos los rangos de los bucles for (checkeando solo cercanos, NO todo el nivel):
        col_inicio = max((self.rect.left + self.game.scroll_x) // self.TX - margen_tiles, 0)
        col_fin = min((self.rect.right + self.game.scroll_x) // self.TX + margen_tiles, ancho_tiles)

        fila_inicio = max(self.rect.top // self.TY - margen_tiles, 0)
        fila_fin = min(self.rect.bottom // self.TY + margen_tiles, alto_tiles)

        for fila in range(int(fila_inicio), int(fila_fin)):
            for col in range(int(col_inicio), int(col_fin)):
                # Obtenemos el indice y el valor:
                index = fila * ancho_tiles + col

                if index >= len(nivel):
                    continue

                tile_id = nivel[index]

                # Averiguamos si el número de tile (id), está en la lista 'solidos':
                if tile_id in self.game.TILES_SOLIDOS:
                    tile_rect = pygame.Rect(col * self.TX - self.game.scroll_x, 
                        (fila * self.TY) + self.game.offset_y, 
                        self.TX, self.TY)
                    if mario_rect.colliderect(tile_rect):
                        self.resolver_colision(tile_rect, hor_ver)
    

    




    def resolver_colision(self, tile_rect, hor_ver):
        # Acciones dependiendo de donde colisionemos (VERTICAL)
        if hor_ver == self.DIRECC_VERTICAL:
            if self.vel_y > 0:  # cayendo
                if self.rect.bottom > tile_rect.top and self.rect.top < tile_rect.top:
                
                    self.vel_y = 0
                    self.rect.bottom = tile_rect.top
                    self.en_suelo = True
                    self.saltando = False

            elif self.vel_y < 0:  # subiendo
                if self.rect.top < tile_rect.bottom and self.rect.bottom > tile_rect.bottom:
                
                    self.vel_y = 0
                    self.rect.top = tile_rect.bottom
       
        elif hor_ver == self.DIRECC_HORIZONTAL:
            if self.acc > 0:  # derecha
                if self.rect.right > tile_rect.left and self.rect.left < tile_rect.left:
                    self.acc = 0

            elif self.acc < 0:  # izquierda
                if self.rect.left < tile_rect.right and self.rect.right > tile_rect.right:
                    self.acc = 0
            
    def animacion(self):
       
        ahora = pygame.time.get_ticks()

        if ahora - self.ultimo_update > self.VEL_FRAMES_ANIMA:
            self.ultimo_update = ahora
            self.anim_index += 1

            if self.anim_index >= self.rango_animacion[1]:
                self.anim_index = self.rango_animacion[0]
            
            # Si va muy lento (cerca de 0), entonces 'animacion parado'[0]:
            if -0.01 <= self.acc <= 0.01:
                self.image = self.lista_imagenes[0]
                self.image = pygame.transform.flip(self.image, self.flip, False)
            else:
                # Si no, cambia la secuencia de animacion de forma normal:
                self.image = self.lista_imagenes[self.anim_index]
                self.image = pygame.transform.flip(self.image, self.flip, False)
                
                
    def limites_mundo(self):
        END_WORLD = self.game.END_WORLD_SCROLL[self.game.nivel - 1] * self.game.ESCALA 
        if self.game.scroll_x <= 0:
            self.game.scroll_x = 0 
        elif self.game.scroll_x >= END_WORLD:
            self.game.scroll_x = END_WORLD