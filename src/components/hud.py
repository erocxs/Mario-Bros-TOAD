import pygame
from arcade_machine_sdk import BASE_WIDTH
from pathlib import Path

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
        self.world = "1-1"
        self.time = 400 
        self.timer_event = 0
        
        self.color = (255, 255, 255)

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

            score_txt = self.font.render(f"MARIO {str(self.score).zfill(6)}", True, self.color)
            world_txt = self.font.render(f"WORLD {self.world}", True, self.color)
            time_txt = self.font.render(f"TIME {int(self.time)}", True, self.color)

       
            surface.blit(score_txt, (50, 20))
           
            surface.blit(world_txt, (BASE_WIDTH // 2 - 70, 20)) 
            surface.blit(time_txt, (BASE_WIDTH - 200, 20))