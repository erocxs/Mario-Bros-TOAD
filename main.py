from mario_game import Game
from arcade_machine_sdk import GameMeta
import pygame

if not pygame.get_init():
    pygame.init()

metadata = (GameMeta()
            .with_title("Super Mario Bros")
            .with_description("Juego de prueba")
            .with_release_date("10/02/2026")
            .with_group_number(1)
            .add_tag("Plataforma")
            .add_author("Anelissa Espin, Erick Gomez, Abelardo Drika"))

game = Game(metadata)

if __name__ == "__main__":
    game.run_independently()