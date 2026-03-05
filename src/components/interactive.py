

import pygame


class Flag(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y
        
        self.image_stuff = self.game.obtener_grafico("smb-mastil-bandera2.png", colorkey=(0, 0, 255)) 
        self.image = self.image_stuff[0]
        
        # Posición inicial
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TX
        self.rect.y = y * self.TY
        
        # TRUCO: Inflamos el rect hacia la izquierda para que Mario lo toque 
        # antes de llegar al centro exacto del palo.
        self.rect.inflate_ip(self.TX, 0) 
        
        self.bajando = False
        self.finalizado = False # Nueva bandera para avisar a Mario

    def update(self):
        base_y = (13 * self.TY) + self.game.offset_y
        if self.bajando:
            if self.rect.bottom < base_y:
                self.rect.y += 5
            else:
                self.rect.bottom = base_y
                self.bajando = False # IMPORTANTE: Esto libera a Mario para caminar

    def draw(self, surface):
        # Dibujamos restando el scroll del motor principal
        surface.blit(self.image, (self.rect.x - self.game.game.scroll_x, self.rect.y))