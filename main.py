import pygame
from constantes import *
from pantalla_menu import PantallaMenu
from juego import Juego
from pantalla_ranking import PantallaRanking
from pantalla_config import PantallaConfig
pygame.init()
pantalla = pygame.display.set_mode(PANTALLA)
pygame.display.set_caption("Preguntados UTN")

reloj = pygame.time.Clock()

# Estados
estado = "menu"
pantalla_actual = PantallaMenu(pantalla)

corriendo = True
nombre_jugador = ""
ingresando_nombre = False

pygame.mixer.music.load("musica_menu.mp3")
pygame.mixer.music.play(-1)

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if estado == "menu":
            nuevo_estado = pantalla_actual.actualizar(evento)
            if nuevo_estado == "juego":
                pantalla_actual = Juego(pantalla)
                estado = "juego"
            elif nuevo_estado == "ranking":
                pantalla_actual = PantallaRanking(pantalla)
                estado = "ranking"
            elif nuevo_estado == "config":
                pantalla_actual = PantallaConfig(pantalla)
                estado = "config"
        elif estado == "ranking":
            nuevo_estado = pantalla_actual.actualizar(evento)
            if nuevo_estado == "menu":
                pantalla_actual = PantallaMenu(pantalla)
                estado = "menu"
        elif estado == "config":
            nuevo_estado = pantalla_actual.actualizar(evento)
            if nuevo_estado == "menu":
                pantalla_actual = PantallaMenu(pantalla)
                estado = "menu"
        elif estado == "juego":
            resultado = pantalla_actual.actualizar(evento)
            if resultado == "fin":
                ingresando_nombre = True
                nombre_jugador = ""
                estado = "ingresar_nombre"

        elif estado == "ingresar_nombre":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre_jugador.strip():
                    pantalla_actual.guardar_partida(nombre_jugador)
                    estado = "menu"
                    pantalla_actual = PantallaMenu(pantalla)
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                else:
                    if len(nombre_jugador) < 15 and evento.unicode.isprintable():
                        nombre_jugador += evento.unicode

    if estado == "ingresar_nombre":
        pantalla.fill(COLOR_NEGRO)
        texto1 = FUENTE_TEXTO.render("¡Juego terminado!", True, COLOR_BLANCO)
        texto2 = FUENTE_TEXTO.render("Ingresá tu nombre:", True, COLOR_BLANCO)
        texto3 = FUENTE_TEXTO.render(nombre_jugador + "|", True, COLOR_AMARILLO)
        pantalla.blit(texto1, (80, 120))
        pantalla.blit(texto2, (80, 180))
        pantalla.blit(texto3, (80, 220))
    else:
        pantalla_actual.dibujar()

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()

