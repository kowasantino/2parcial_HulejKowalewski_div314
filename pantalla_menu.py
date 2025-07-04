import pygame
from boton import Boton
from constantes import *

class PantallaMenu:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.boton_ranking = Boton(75, 300, 150, 30, "Ranking", FUENTE_RANK)
        self.boton_config = Boton(275, 300, 150, 30, "Ajustes", FUENTE_RANK)
        self.boton_jugar = Boton(100, 200, ANCHO_BOTON, ALTO_BOTON, "Jugar", FUENTE_BOTON)
        self.fondo = pygame.image.load("fondo_menu.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        self.img_titulo = pygame.image.load("titulo.png").convert_alpha()
        self.img_titulo = pygame.transform.scale(self.img_titulo, (400, 300))

    def actualizar(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_ranking.esta_clickeado(evento.pos):
                CLICK_SONIDO.play()
                return "ranking"
            if self.boton_config.esta_clickeado(evento.pos):
                CLICK_SONIDO.play()
                return "config"
            if self.boton_jugar.esta_clickeado(evento.pos):
                CLICK_SONIDO.play()
                return "juego"
        return "menu"


    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.boton_jugar.dibujar(self.pantalla)
        self.boton_ranking.dibujar(self.pantalla)
        self.boton_config.dibujar(self.pantalla)
        ancho = self.img_titulo.get_width()
        x = (self.pantalla.get_width() - ancho) // 2
        self.pantalla.blit(self.img_titulo, (x, -30))
