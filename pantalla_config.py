import pygame
from boton import Boton
from constantes import *
import constantes 

class PantallaConfig:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.boton_volver = Boton(300, 400, 150, 30, "Volver", FUENTE_RANK)
        self.boton_musica = Boton(100, 40, 150, 40, "Música: ON", FUENTE_VOLUMEN)
        self.boton_efectos = Boton(100, 180, 150, 40, "Efectos: ON", FUENTE_VOLUMEN)
        self.volumen_musica = 0.2
        self.volumen_efectos = 0.5
        self.musica_activada = True
        self.efectos_activados = True
        # Barras de volumen (x, y, ancho, alto)
        self.rect_vol_musica = pygame.Rect(100, 120, 200, 20)
        self.rect_vol_efectos = pygame.Rect(100, 260, 200, 20)
        pygame.mixer.music.set_volume(self.volumen_musica)



    def actualizar(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_volver.esta_clickeado(evento.pos):
                CLICK_SONIDO.play()
                return "menu"
            if self.boton_musica.esta_clickeado(evento.pos):
                self.musica_activada = not self.musica_activada
                if self.musica_activada:
                    pygame.mixer.music.set_volume(self.volumen_musica)
                    pygame.mixer.music.unpause()
                    self.boton_musica.texto = "Música: ON"
                else:
                    pygame.mixer.music.set_volume(0)
                    pygame.mixer.music.pause()
                    self.boton_musica.texto = "Música: OFF"
            if self.boton_efectos.esta_clickeado(evento.pos):
                self.efectos_activados = not self.efectos_activados
                self.boton_efectos.texto = "Efectos: ON" if self.efectos_activados else "Efectos: OFF"
                constantes.EFECTOS_ACTIVADOS = self.efectos_activados
            # Control de volumen música con barra
            if self.rect_vol_musica.collidepoint(evento.pos):
                x = evento.pos[0]
                rel_x = x - self.rect_vol_musica.x
                self.volumen_musica = max(0, min(1, rel_x / self.rect_vol_musica.width))
                if self.musica_activada:
                    pygame.mixer.music.set_volume(self.volumen_musica)
            # Control de volumen efectos con barra
            if self.rect_vol_efectos.collidepoint(evento.pos):
                    x = evento.pos[0]
                    rel_x = x - self.rect_vol_efectos.x
                    self.volumen_efectos = max(0, min(1, rel_x / self.rect_vol_efectos.width))
                    constantes.VOLUMEN_EFECTOS = self.volumen_efectos
            return "config"

    def dibujar(self):
        self.pantalla.fill(COLOR_NEGRO)
        self.boton_volver.dibujar(self.pantalla)
        self.boton_musica.dibujar(self.pantalla)
        self.boton_efectos.dibujar(self.pantalla)
        fuente = pygame.font.Font("PressStart2P.ttf", 14)
        # Volumen música
        texto_vol = fuente.render(f"Volumen Música: {int(self.volumen_musica*100)}%", True, COLOR_BLANCO)
        self.pantalla.blit(texto_vol, (100, 100))
        pygame.draw.rect(self.pantalla, COLOR_AZUL, self.rect_vol_musica)
        pygame.draw.rect(self.pantalla, COLOR_BLANCO, (self.rect_vol_musica.x, self.rect_vol_musica.y, int(self.rect_vol_musica.width * self.volumen_musica), self.rect_vol_musica.height))
        # Volumen efectos
        texto_ef = fuente.render(f"Volumen Efectos: {int(self.volumen_efectos*100)}%", True, COLOR_BLANCO)
        self.pantalla.blit(texto_ef, (100, 240))
        pygame.draw.rect(self.pantalla, COLOR_AZUL, self.rect_vol_efectos)
        pygame.draw.rect(self.pantalla, COLOR_BLANCO, (self.rect_vol_efectos.x, self.rect_vol_efectos.y, int(self.rect_vol_efectos.width * self.volumen_efectos), self.rect_vol_efectos.height))
