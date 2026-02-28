import pygame
from arcade_machine_sdk import GameBase
from src.states.menu import MenuState
from src.states.nivel1 import Level1State
from pathlib import Path
from src.components.hud import HUD

class Game(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.menu = None
        self.nivel1 = None
        self.vidas = 5
        self.estado_actual = "MENU"
        self.timer_muerte = 0
        self.scroll_x = 0
        
        # --- CARGA GLOBAL DE SONIDOS ---
        self.BASE_DIR = Path(__file__).resolve().parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        
        try:
            path_coin = self.ASSETS_DIR / "sounds" / "p-ping.mp3"
            self.sonido_click = pygame.mixer.Sound(str(path_coin))
        except:
            self.sonido_click = None
            print("Error: No se encontró p-ping.mp3")

    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)
        self.hud = HUD()
        self.menu = MenuState(self.sonido_click)
        self.nivel1 = Level1State(self, self.hud)
        # Iniciar música del menú
        self.cambiar_musica("intro-mario-snes.mp3") # Pon el nombre exacto de tu archivo de menú

    # En mario_game.py
    def handle_events(self, events: list[pygame.event.Event]):
        if self.estado_actual == "MENU" and self.menu:
            proximo = self.menu.handle_events(events)
            if proximo == "SELECTOR":
                self.estado_actual = "JUEGO"
                # ¡Aquí haces el cambio!
                self.cambiar_musica("musica-mario-bros.mp3")

    def update(self, dt: float):
        if self.estado_actual == "MENU":
            self.menu.update(dt)
        elif self.estado_actual == "JUEGO":
            self.nivel1.update(dt)
        elif self.estado_actual == "MUERTO":
            # Esperar 2 segundos en la pantalla negra antes de renacer
            if pygame.time.get_ticks() - self.timer_muerte > 2000:
                if self.vidas > 0:
                    self.resetear_nivel()
                    self.estado_actual = "JUEGO"
                else:
                    self.estado_actual = "MENU"
                    self.vidas = 5
        self.hud.update(dt)
        
    # En mario_game.py
    def cambiar_musica(self, nombre_archivo):
        try:
            ruta = self.ASSETS_DIR / "music" / nombre_archivo
            pygame.mixer.music.stop() # Detiene la música actual
            pygame.mixer.music.load(str(ruta))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1) # Reproduce en bucle
        except Exception as e:
            print(f"Error al cambiar música: {e}")
            
    def quitar_vida(self):
        if self.estado_actual != "MUERTO":
            self.vidas -= 1
            self.estado_actual = "MUERTO"
            self.timer_muerte = pygame.time.get_ticks()
            
            # --- EL SECRETO ESTÁ AQUÍ ---
            # Forzamos el reset de la cámara INMEDIATAMENTE al morir
            self.scroll_x = 0 
            
    def resetear_nivel(self):
        print("EJECUTANDO RESET TOTAL")
        self.scroll_x = 0 # El del juego
        if self.nivel1:
            self.nivel1.instanciar_objetos() # Esto crea un Mario nuevo con acc=0
            # Forzamos posición inicial (11 * 48 = 528 aprox)
            self.nivel1.mario.rect.x = 11 * self.nivel1.TILE_X
            self.nivel1.mario.rect.y = 13 * self.nivel1.TILE_Y
            self.nivel1.mario.vel_y = 0
            self.nivel1.mario.acc = 0
        
    def render(self, surface=None):
        target_surface = surface if surface is not None else self.surface
        
        if self.estado_actual == "MENU":
                self.menu.draw(target_surface)
        elif self.estado_actual == "JUEGO":
                self.nivel1.draw(target_surface)
                self.hud.render(target_surface, self.vidas)
        elif self.estado_actual == "MUERTO":
                # PANTALLA NEGRA DE MUERTE
                target_surface.fill((0, 0, 0))
                texto = self.hud.font.render(f"X  {self.vidas}", True, (255, 255, 255))
                # Dibujamos a Mario (puedes usar el primer frame de tu lista)
                target_surface.blit(self.nivel1.mario.lista_imagenes[0], (450, 330))
                target_surface.blit(texto, (510, 350))