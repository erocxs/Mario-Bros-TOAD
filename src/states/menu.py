import pygame
from pathlib import Path

class MenuState:
    def __init__(self, sonido_global):
        self.sonido_boton = sonido_global
        if self.sonido_boton:
            self.sonido_boton.set_volume(0.4)
        # 1. Rutas
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.ASSETS_DIR = self.BASE_DIR / "assets" / "menu"

        # 2. Carga de imágenes
        self.img_fondo = pygame.image.load(str(self.ASSETS_DIR / "fondoMario.png"))
        self.img_titulo = pygame.image.load(str(self.ASSETS_DIR / "TituloMariobg.png"))
        self.img_btn_normal = pygame.image.load(str(self.ASSETS_DIR / "BotonMariobg.png"))
        
        try:
            self.img_btn_hover = pygame.image.load(str(self.ASSETS_DIR / "BotonMarioHover.png"))
        except:
            self.img_btn_hover = self.img_btn_normal
            
        self.area_clic_real = pygame.Rect(350, 475, 312, 50) 
        
        try:
            path_musica = self.BASE_DIR / "assets" / "music" / "intro-mario-snes.mp3"
            pygame.mixer.music.load(str(path_musica))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("Error: No se encontró la música del menú")
            
        self.timer_parpadeo = 0
        self.mostrar_boton = True
        self.velocidad_parpadeo = 13  
        self.esta_encima = False

    def handle_events(self, events):

        teclas = pygame.key.get_pressed()
            
        # 3. CAMBIO CLAVE: Detectar la tecla Espacio
        if teclas[pygame.K_SPACE]:
            if self.sonido_boton:
                self.sonido_boton.play()
            pygame.mixer.music.fadeout(500)
            return "SELECTOR"
            
        return "MENU" 
        

    def update(self, dt):
        if not self.esta_encima:
            self.timer_parpadeo += 1
            if self.timer_parpadeo >= self.velocidad_parpadeo:
                self.mostrar_boton = not self.mostrar_boton
                self.timer_parpadeo = 0
        else:
            self.mostrar_boton = True

    def draw(self, surface):
        surface.blit(self.img_fondo, (0, 0))
        surface.blit(self.img_titulo, (0, 0))
        
        if self.mostrar_boton:
            if self.esta_encima:
                surface.blit(self.img_btn_hover, (0, 0))
            else:
                surface.blit(self.img_btn_normal, (0, 0))