import pygame


class ColisionadoresInvisibles:
    COORDENADAS_XY = [
        [(10, 13), (69, 13), (70, 13), (86, 13), (88, 13)],#  Nivel 1
    ]

    def __init__(self, game, nivel):
        self.game = game
        self.TX = self.game.TILE_X
        self.TY = self.game.TILE_Y
        self.nivel = nivel

        # Llamamos 'TRIGGERS' a la lista de colisionadores-invisibles:
        self.TRIGGERS = []
        self.crear_lista_colisionadores_invisibles()
    





    def crear_lista_colisionadores_invisibles(self):
        colisionadores_nivel = ColisionadoresInvisibles.COORDENADAS_XY[self.nivel - 1]

        for coorXY in colisionadores_nivel:
            x, y = coorXY[0], coorXY[1]

            self.TRIGGERS.append(pygame.Rect(x * self.TX, y * self.TY, self.TX, self.TY))