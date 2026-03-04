import pygame

class Flag(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y
        
        self.image_stuff = self.game.obtener_grafico("smb-mastil-bandera2.png") 
        self.image = self.image_stuff[0]
        self.rect = self.image.get_rect()
        
        # Posición absoluta en el mundo
        self.rect.x = x * self.TX
        self.rect.y = y * self.TY
        
        # Hitbox para la colisión (basada en coordenadas de mundo)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.TX // 2, self.TY * 10)
        
        self.bajando = False

    def update(self):
        # Actualizamos la posición del suelo
        base_y = (13 * self.TY) + self.game.offset_y

        if self.bajando:
            if self.rect.bottom < base_y:
                self.rect.y += 4
            else:
                self.rect.bottom = base_y
                self.bajando = False

    def draw(self, surface):
        # Dibujamos restando el scroll del motor principal
        surface.blit(self.image, (self.rect.x - self.game.game.scroll_x, self.rect.y))