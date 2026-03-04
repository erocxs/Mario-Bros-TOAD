import pygame

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Físicas de la estrella
        self.vel_x = 150  # Velocidad horizontal
        self.vel_y = 0    # Velocidad vertical (salto)
        self.gravedad = 800
        self.fuerza_salto = -300
        self.direccion = 1 # 1 derecha, -1 izquierda

    def update(self, dt, plataformas):
        # Movimiento horizontal
        self.rect.x += self.vel_x * self.direccion * dt
        self._check_colisiones_horizontales(plataformas)

        # Movimiento vertical (Gravedad)
        self.vel_y += self.gravedad * dt
        self.rect.y += self.vel_y * dt
        self._check_colisiones_verticales(plataformas)

    def _check_colisiones_horizontales(self, plataformas):
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.direccion > 0: # Choca derecha
                    self.rect.right = plataforma.rect.left
                else: # Choca izquierda
                    self.rect.left = plataforma.rect.right
                self.direccion *= -1 # Rebota hacia el otro lado

    def _check_colisiones_verticales(self, plataformas):
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0: # Cayendo
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = self.fuerza_salto # ¡Rebota!
                elif self.vel_y < 0: # Subiendo (choca con techo)
                    self.rect.top = plataforma.rect.bottom
                    self.vel_y = 0
