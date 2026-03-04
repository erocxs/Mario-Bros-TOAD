import pygame
from arcade_machine_sdk import GameBase
from src.states.menu import MenuState
from src.states.nivel1 import Level1State
from pathlib import Path
from src.components.hud import HUD
from src.utils.constantsmario import TILE_X

class Game(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.menu = None
        self.nivel1 = None
        self.vidas = 5
        self.estado_actual = "MENU"
        self.timer_muerte = 0
        # En tu archivo principal de juego (Game Class)
        self.scroll_x = 185 * TILE_X - 200
        self.tiempo_inicial = 400  
        self.tiempo_restante=self.tiempo_inicial # Aparece con la cámara ya adelantada
        
        # --- CARGA GLOBAL DE SONIDOS ---
        self.BASE_DIR = Path(__file__).resolve().parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"
        
        try:
            path_coin = self.ASSETS_DIR / "sounds" / "p-ping.mp3"
            path_muerte = self.ASSETS_DIR / "sounds" / "mario-lose-life.mp3"
            self.sonido_click = pygame.mixer.Sound(str(path_coin))
            self.sonido_muerte = pygame.mixer.Sound(str(path_muerte))
        except:
            self.sonido_click = None
            self.sonido_muerte = None
            print("Error: No se encontrón los sonidos. Asegúrate de que 'p-ping.mp3' y 'mario-lose-life.mp3' estén en la carpeta correcta.")
            
            

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
                # --- AQUÍ ESTÁ EL CAMBIO ---
                self.resetear_nivel() # Limpiamos el scroll, mario y banderas
                # Reiniciamos las variables de fundido del nivel
                self.nivel1.iniciar_fundido = False
                self.nivel1.fade_alpha = 0
                
                self.estado_actual = "JUEGO"
                self.cambiar_musica("musica-mario-bros.mp3")

    def update(self, dt: float):
        if self.estado_actual == "MENU":
            self.menu.update(dt)
        elif self.estado_actual == "JUEGO":
            self.nivel1.update(dt)
            self.tiempo_restante -= dt 
            
            # Si el tiempo llega a 0, Mario muere
            if self.tiempo_restante <= 0:
                self.tiempo_restante = 0
                self.quitar_vida()
        elif self.estado_actual == "MUERTO":
            # Esperar 2 segundos en la pantalla negra antes de renacer
            if pygame.time.get_ticks() - self.timer_muerte > 3000:
                if self.vidas > 0:
                    self.resetear_nivel()
                    self.estado_actual = "JUEGO"
                    self.cambiar_musica("musica-mario-bros.mp3")
                else:
                    self.estado_actual = "MENU"
                    self.vidas = 5
                    self.cambiar_musica("intro-mario-snes.mp3")
        self.hud.update(dt)
        
        
        
    # En mario_game.py
    def cambiar_musica(self, nombre_archivo,bucle=-1):
        try:
            ruta = self.ASSETS_DIR / "music" / nombre_archivo
            pygame.mixer.music.stop() # Detiene la música actual
            pygame.mixer.music.load(str(ruta))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(bucle) # Reproduce en bucle
        except Exception as e:
            print(f"Error al cambiar música: {e}")
            
    def quitar_vida(self):
        if self.estado_actual != "MUERTO":
            # 1. Detener la música del nivel inmediatamente
            pygame.mixer.music.stop()
            
            # 2. Reproducir el efecto de sonido de muerte
            if self.sonido_muerte:
                self.sonido_muerte.play()
                
            # 3. Restar vida y cambiar estado
            self.vidas -= 1
            self.estado_actual = "MUERTO"
            self.timer_muerte = pygame.time.get_ticks()
            
            # Resetear el scroll para que al renacer la cámara esté bien
            self.scroll_x = 0 
            
    def resetear_nivel(self):
        print("EJECUTANDO RESET TOTAL")
        self.scroll_x = 0  # Reseteamos el scroll global del juego
        self.tiempo_restante = self.tiempo_inicial
        if self.hud:
            self.hud.reset_timer()  # Reseteamos el timer del HUD
        
        if self.nivel1:
            # Importante: resetear las variables de control de meta en el nivel
            self.nivel1.iniciar_fundido = False
            self.nivel1.fade_alpha = 0
            
            # Re-instanciar objetos (Mario, Goombas, Bandera)
            self.nivel1.instanciar_objetos() 
            
            # Aseguramos que Mario aparezca al inicio real (columna 2 o 11 según quieras)
            self.nivel1.mario.rect.x = 11 * self.nivel1.TILE_X # O usa tu INI_POS_MARIO
            self.nivel1.mario.rect.y = 13 * self.nivel1.TILE_Y
            self.nivel1.mario.vel_y = 0
            self.nivel1.mario.acc = 0
            # Resetear el estado de meta de Mario por si acaso
            self.nivel1.mario.secuencia_final = False
            if hasattr(self.nivel1.mario, "en_suelo_final"):
                delattr(self.nivel1.mario, "en_suelo_final")
        
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