import pygame
from arcade_machine_sdk import GameBase
from src.states.menu import MenuState
from src.states.nivel1 import Level1State
from pathlib import Path

class Game(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.menu = None
        self.nivel1 = None
        self.estado_actual = "MENU"
        
        # --- CARGA GLOBAL DE SONIDOS ---
        self.BASE_DIR = Path(__file__).resolve().parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        
        try:
            path_coin = self.ASSETS_DIR / "music" / "p-ping.mp3"
            self.sonido_click = pygame.mixer.Sound(str(path_coin))
        except:
            self.sonido_click = None
            print("Error: No se encontró p-ping.mp3")

    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)
        self.menu = MenuState(self.sonido_click)
        self.nivel1 = Level1State()

    def handle_events(self, events: list[pygame.event.Event]):
        if self.estado_actual == "MENU" and self.menu:
            proximo = self.menu.handle_events(events)
            if proximo == "SELECTOR":
                self.estado_actual = "JUEGO"

    def update(self, dt: float):
        if self.estado_actual == "MENU" and self.menu:
            self.menu.update(dt)
        
        elif self.estado_actual == "JUEGO" and self.nivel1:
            self.nivel1.update(dt)

    def render(self, surface=None):
        target_surface = surface if surface is not None else self.surface
        
        if self.estado_actual == "MENU" and self.menu:
            self.menu.draw(target_surface)
        elif self.estado_actual == "JUEGO" and self.nivel1:
            self.nivel1.draw(target_surface)