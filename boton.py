import pygame
from constantes import *

class Boton:
    def __init__(self, x, y, ancho, alto, texto, fuente):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente
        self.habilitado = True

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_ROJO, self.rect, border_radius=10)
        texto_render = self.fuente.render(self.texto, True, COLOR_BLANCO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def esta_clickeado(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
