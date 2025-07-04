import pygame
import json
from constantes import *
from boton import Boton

class PantallaRanking:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.boton_volver = Boton(300, 400, 150, 30, "Volver", FUENTE_RANK)


    def obtener_top10(self):
        try:
            with open("partidas.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
                datos = [(item["nombre"], int(item["puntaje"])) for item in datos if "nombre" in item and "puntaje" in item]
                datos.sort(key=lambda x: x[1], reverse=True)
                return datos[:10]
        except Exception:
            return []

    def actualizar(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_volver.esta_clickeado(evento.pos):
                CLICK_SONIDO.play()    
                return "menu"
        return "ranking"

    def dibujar(self):
        self.pantalla.fill((30, 30, 30))
        fuente = pygame.font.Font("PressStart2P.ttf", 12)
        top10 = self.obtener_top10()
        y = 80
        for i, (nombre, puntaje) in enumerate(top10, 1):
            texto = fuente.render(f"{i}. {nombre} - {puntaje}", True, (255, 255, 255))
            self.pantalla.blit(texto, (100, y))
            y += 40
        self.boton_volver.dibujar(self.pantalla)

