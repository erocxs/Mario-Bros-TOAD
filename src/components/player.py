import pygame
from src.utils.constantsmario import *
from src.components.moneda import moneda
from src.components.hongo import hongo

class Mario(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.TX = TILE_X
        self.TY = TILE_Y
        self.estado_finalizado = False

        # Sprite sheet (Usamos SOLO tu archivo original)
        self.spritesheet_img_rect = self.game.obtener_grafico("mario-ss1.png") 
        self.image = self.spritesheet_img_rect[0] 
        self.rect = self.spritesheet_img_rect[1] 
        self.ancho_imagen = self.image.get_width()
        self.alto_imagen = self.image.get_height()
        self.numero_sprites_ssheet = self.ancho_imagen // self.TX 
        self.rango_animacion = (1, 4)
        
        self.anim_index = 0
        self.lista_imagenes = []

        for i in range(self.numero_sprites_ssheet):
            img = pygame.Surface((self.TX, self.TY), pygame.SRCALPHA)
            img.blit(self.image, (0, 0), (i * self.TX, 0, self.TX, self.TY))
            self.lista_imagenes.append(img)
        
        self.image = self.lista_imagenes[self.anim_index]
        
        self.rect = self.image.get_rect() 
        self.rect.x = x * self.TX
        self.rect.y = y * self.TY
        self.rect.inflate_ip(-2, 0)
        
        self.DIRECC_HORIZONTAL = 'hor'
        self.acc = 0    
        self.acc_acum = 0   
        self.flip = False
        self.VEL_MAX = 7.5
        self.ACELERACION = 0.14
        self.DECELERACION = 0.2
        
        self.DIRECC_VERTICAL = 'ver'
        self.vel_y = 0
        self.GRAVEDAD = self.game.GRAVEDAD
        self.en_suelo = False
        self.saltando = False
        self.POTENCIA_SALTO = -18
        self.POT_EXTRA = 1.75 
        self.secuencia_final = False
        
        # --- VARIABLES SUPER MARIO ---
        self.es_grande = False
        self.en_transformacion = False
        self.timer_transformacion = 0
        self.imagenes_pequenas = self.lista_imagenes.copy()
        self.imagenes_grandes = []
        
        self.ultimo_update = pygame.time.get_ticks()
        self.VEL_FRAMES_ANIMA = 90
        self.ganado = False
        
    def update(self):
        if self.en_transformacion:
            self.animacion_transformacion()
        else:
            self.mover() 
            self.animacion()
            self.chequear_muerte()
        
    def chequear_muerte(self):
        if self.rect.y > 800: 
            self.game.quitar_vida() 

    def morir(self):
        pass
        
    def mover(self):
        if self.secuencia_final:
            limite_suelo = (13 * self.TY) + self.game.offset_y
            if not hasattr(self, "en_suelo_final"):
                if self.rect.bottom < limite_suelo:
                    self.rect.y += 4
                    self.acc = 0
                    return 
                else:
                    self.rect.bottom = limite_suelo
                    self.en_suelo_final = True
                    self.saltando = False 
                    self.vel_y = 0
                    return
            else:
                bandera = self.game.bandera_obj 
                if bandera.rect.y < (12 * self.TY): 
                    self.acc = 0
                    return 
                self.acc = 2 
                self.flip = False 
                self.rect.x += self.acc 
                pos_mundo = self.rect.x + self.game.game.scroll_x
                if pos_mundo >= (204 * self.TX): 
                    self.acc = 0 
                    self.rect.x = (204 * self.TX) - self.game.game.scroll_x
                    self.game.iniciar_fundido = True 
                return

        self.aplicar_gravedad()
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.gestionar_aceleracion(True)
            self.flip = True
        elif teclas[pygame.K_RIGHT]:
            self.gestionar_aceleracion(False)
            self.flip = False
        else:
            if self.acc > 0: self.acc = max(0, self.acc - self.DECELERACION)
            elif self.acc < 0: self.acc = min(0, self.acc + self.DECELERACION)
        
        if teclas[pygame.K_SPACE]:
            self.saltar()

        self.game.game.scroll_x += self.acc
        self.manejar_colisiones_obstaculos(self.DIRECC_HORIZONTAL)
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
        self.en_suelo = False  
        self.manejar_colisiones_obstaculos(self.DIRECC_VERTICAL)
        
    def saltar(self):
        if self.en_suelo:
            self.vel_y = self.POTENCIA_SALTO - abs(self.acc_acum / self.POT_EXTRA)
            self.en_suelo = False
            self.saltando = True
            try:
                self.game.sonidos.reproducir("jumpbros.ogg")
            except:
                pass
            
    def manejar_colisiones_obstaculos(self, hor_ver):
        nivel = NIVEL_1
        ancho_tiles = self.game.COLUMNAS
        alto_tiles = len(nivel) // ancho_tiles
        mario_rect = self.rect
        margen_tiles = 2 

        col_inicio = max((self.rect.left + self.game.game.scroll_x) // self.TX - margen_tiles, 0)
        col_fin = min((self.rect.right + self.game.game.scroll_x) // self.TX + margen_tiles, ancho_tiles)
        fila_inicio = max(self.rect.top // self.TY - margen_tiles, 0)
        fila_fin = min(self.rect.bottom // self.TY + margen_tiles, alto_tiles)

        for fila in range(int(fila_inicio), int(fila_fin)):
            for col in range(int(col_inicio), int(col_fin)):
                index = fila * ancho_tiles + col
                if index >= len(nivel):
                    continue
                tile_id = nivel[index]
                if tile_id in self.game.TILES_SOLIDOS:
                    tile_rect = pygame.Rect(col * self.TX - self.game.game.scroll_x, 
                        (fila * self.TY) + self.game.offset_y, 
                        self.TX, self.TY)
                    if mario_rect.colliderect(tile_rect):
                        self.resolver_colision(tile_rect, hor_ver,tile_id, index)
    
    def resolver_colision(self, tile_rect, hor_ver, tile_id, index):
        if hor_ver == self.DIRECC_VERTICAL:
            if self.vel_y > 0:  
                if self.rect.bottom > tile_rect.top and self.rect.top < tile_rect.top and abs(
                    self.rect.centerx - tile_rect.centerx) < self.TX - (self.game.ESCALA * 3):
                    self.vel_y = 0
                    self.rect.bottom = tile_rect.top
                    self.en_suelo = True
                    self.saltando = False

            elif self.vel_y < 0:  
                if self.rect.top < tile_rect.bottom and self.rect.bottom > tile_rect.bottom and abs(
                    self.rect.centerx - tile_rect.centerx) < self.TX - (self.game.ESCALA * 3):
                    self.vel_y = 0
                    self.rect.top = tile_rect.bottom
                    
                    if tile_id == 14:
                        if index == 1929 or index == 1986 or index == 1169:
                            if not index in hongo.ARRAY_DESACTIVADAS:
                                self.game.instanciar_hongo(index, tile_rect.left, tile_rect.top - self.TY, False)
                        elif not index in moneda.ARRAY_DESACTIVADAS:
                            moneda_x = tile_rect.left + self.game.game.scroll_x 
                            moneda_y = tile_rect.top - self.TY
                            self.game.instanciar_moneda(index, moneda_x, moneda_y, False)
                            
                    elif tile_id == 15:
                        if index == 2002 or index == 2009:
                            moneda_x = tile_rect.left + self.game.game.scroll_x 
                            moneda_y = tile_rect.top - self.TY
                            self.game.instanciar_moneda(index, moneda_x, moneda_y, False)

        elif hor_ver == self.DIRECC_HORIZONTAL:
            if self.acc > 0:  
                if self.rect.right > tile_rect.left and self.rect.left < tile_rect.left:
                    self.acc = 0
            elif self.acc < 0:  
                if self.rect.left < tile_rect.right and self.rect.right > tile_rect.right:
                    self.acc = 0
            
    def animacion(self):
        if self.secuencia_final and not hasattr(self, "en_suelo_final"):
            self.image = self.lista_imagenes[5]
            self.image = pygame.transform.flip(self.image, self.flip, False)
            return

        if self.saltando and not hasattr(self, "en_suelo_final"):
            self.image = self.lista_imagenes[5]
            self.image = pygame.transform.flip(self.image, self.flip, False)
            return

        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_update > self.VEL_FRAMES_ANIMA:
            self.ultimo_update = ahora
            self.anim_index += 1
            if self.anim_index >= self.rango_animacion[1]:
                self.anim_index = self.rango_animacion[0]
        
        if -0.1 < self.acc < 0.1:
            self.image = self.lista_imagenes[0]
        else:
            self.image = self.lista_imagenes[self.anim_index]

        self.image = pygame.transform.flip(self.image, self.flip, False)
                
    def limites_mundo(self):
        END_WORLD = self.game.END_WORLD_SCROLL[self.game.nivel - 1] * self.game.ESCALA 
        if self.game.game.scroll_x <= 0:
            self.game.game.scroll_x = 0 
        elif self.game.game.scroll_x >= END_WORLD:
            self.game.game.scroll_x = END_WORLD
            
    def aplicar_gravedad_final(self):
        limite_suelo = (13 * self.TY) + self.game.offset_y
        if self.rect.bottom < limite_suelo:
            self.rect.y += 3  
            self.vel_y = 0 
        else:
            self.rect.bottom = limite_suelo

    # Metodo nuevo, metodo crecer para hacer a mario mas grande cuando toca el hongo
    def crecer(self):
        if not self.es_grande:
            self.es_grande = True
            self.en_transformacion = True
            self.timer_transformacion = pygame.time.get_ticks()
            try:
                self.game.sonidos.reproducir("smb_powerup.wav") 
            except:
                pass
            
           #Aqui pueden jugar con el ancho y el alto para ver como queda mejor
            nuevo_ancho = int(self.TX * 1.3)
            nuevo_alto = self.TY * 2
            
            self.imagenes_grandes = []
            for img in self.imagenes_pequenas:
                img_grande = pygame.transform.scale(img, (nuevo_ancho, nuevo_alto))
                self.imagenes_grandes.append(img_grande)
            
            self.lista_imagenes = self.imagenes_grandes

    def animacion_transformacion(self):
        ahora = pygame.time.get_ticks()
        tiempo_transcurrido = ahora - self.timer_transformacion
        
        viejo_bottom = self.rect.bottom 
        
        if tiempo_transcurrido < 900: 
            if (tiempo_transcurrido // 100) % 2 == 0:
                self.image = self.imagenes_pequenas[0]
            else:
                self.image = self.imagenes_grandes[0]
                
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, viejo_bottom))
        else:
            self.en_transformacion = False
            self.image = self.imagenes_grandes[0]
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, viejo_bottom))
            self.rect.inflate_ip(-2, 0)