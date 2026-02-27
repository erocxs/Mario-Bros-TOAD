import pygame
from arcade_machine_sdk import BASE_WIDTH
from pathlib import Path
from src.states.nivel1 import Level1State

class HUD:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parents[2] 
        FONT_PATH = BASE_DIR / "assets" / "fonts" / "pixelmix.ttf"

        try:
            
            self.font = pygame.font.Font(str(FONT_PATH), 30)
        except FileNotFoundError:
            print(f"Error: No se encontró la fuente en {FONT_PATH}. Usando fuente por defecto.")
            self.font = pygame.font.SysFont('monospace', 30, bold=True)
        self.score = 0
        self.coins = 0
        self.world_text = "1-1"
        self.time = 400 
        self.timer_event = 0
        
        self.color = (255, 255, 255)
        
    def set_world(self, world_name):
        self.world_text = world_name

    def update(self, dt):
        if self.time > 0:
            self.timer_event += dt
            if self.timer_event >= 1: 
                self.time -= 1
                self.timer_event = 0

    def add_score(self, points):
        self.score += points

    def render(self, surface):
        if surface is not None:
            # Colores y Textos
            score_title = self.font.render("MARIO", True, self.color)
            score_num = self.font.render(str(self.score).zfill(6), True, self.color)
            
            world_title = self.font.render("WORLD", True, self.color)
            world_val = self.font.render(str(self.world_text), True, self.color)
            
            time_title = self.font.render("TIME", True, self.color)
            time_val = self.font.render(str(int(self.time)), True, self.color)

            # Coordenadas calculadas
            # Usamos un espacio vertical (ej: 30 píxeles) para la segunda línea
            line_spacing = 30 
            
            # Dibujamos MARIO (Izquierda)
            surface.blit(score_title, (50, 20))
            surface.blit(score_num, (50, 20 + line_spacing))
            
            # Dibujamos WORLD (Centro)
            # Centramos respecto a BASE_WIDTH del SDK
            surface.blit(world_title, (BASE_WIDTH // 2 - 50, 20))
            surface.blit(world_val, (BASE_WIDTH // 2 - 20, 20 + line_spacing)) 
            
            # Dibujamos TIME (Derecha)
            surface.blit(time_title, (BASE_WIDTH - 200, 20))
            surface.blit(time_val, (BASE_WIDTH - 190, 20 + line_spacing))