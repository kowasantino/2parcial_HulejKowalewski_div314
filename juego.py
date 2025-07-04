import pygame
import csv
import random
from constantes import *
from boton import Boton
import json
from datetime import datetime
from constantes import CLICK_SONIDO, ERROR_SONIDO, EFECTOS_ACTIVADOS, VOLUMEN_EFECTOS


class Juego:
    
    
    
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.preguntas = self.cargar_preguntas()
        self.pregunta_actual = random.choice(self.preguntas)
        self.botones_opciones = self.crear_botones_respuesta()
        self.fondo = pygame.image.load("fondo_juego.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        self.vidas = CANTIDAD_VIDAS
        self.puntaje = 0
        self.bloqueado = False
        self.racha_aciertos = 0
        self.comodines= {
            "bomba": True,
            "x2": True,
            "doble_chance": True,
            "pasar": True
        }
        self.usando_x2= False
        self.usando_doble_chance= False
        self.primer_intento_fallido = False
        self.boton_bomba = Boton(25, 200, 60, 15, "Bomba", FUENTE_COMODIN)
        self.boton_x2 = Boton(25, 400, 60, 15, "x2", FUENTE_COMODIN)
        self.boton_doble = Boton(425, 400, 60, 15, "Doble", FUENTE_COMODIN)
        self.boton_pasar = Boton(425, 200, 60, 15, "Pasar", FUENTE_COMODIN)
        self.tiempo_limite = 15  # segundos
        self.tiempo_restante = self.tiempo_limite
        self.ultimo_tick = pygame.time.get_ticks()
        pygame.mixer.music.load("musica_juego.mp3")
        pygame.mixer.music.play(-1)

    def cargar_preguntas(self):
        preguntas = []
        with open("preguntas.csv", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                preguntas.append(fila)
        return preguntas

    def crear_botones_respuesta(self):
        botones = []
        letras = ['a', 'b', 'c','d']
        for i, letra in enumerate(letras):
            texto = self.pregunta_actual[f"opcion_{letra}"]
            boton = Boton(100, 200 + i * 70, ANCHO_BOTON, ALTO_BOTON, texto, FUENTE_RESPUESTA)
            botones.append((boton, letra))
        return botones
    
    def cargar_nueva_pregunta(self):
        self.pregunta_actual = random.choice(self.preguntas)
        self.botones_opciones = self.crear_botones_respuesta()
        self.primer_intento_fallido = False
        self.usando_doble_chance = False
        self.tiempo_restante = self.tiempo_limite
        self.ultimo_tick = pygame.time.get_ticks()
        self.bloqueado = False


    def actualizar(self, evento):
        ahora = pygame.time.get_ticks()
        delta = (ahora - self.ultimo_tick) / 1000  # en segundos
        self.ultimo_tick = ahora
        self.tiempo_restante -= delta

        # Si se acaba el tiempo, perder vida y cargar otra pregunta
        if self.tiempo_restante <= 0:
            self.vidas -= 1
            self.puntaje -= PUNTUACION_ERROR
            self.racha_aciertos = 0
            if self.vidas <= 0:
                return "fin"
            self.cargar_nueva_pregunta()
            return

        # Si se hizo click, procesar evento
        if evento.type == pygame.MOUSEBUTTONDOWN:

            # Comodines
            if self.comodines["bomba"] and self.boton_bomba.esta_clickeado(evento.pos):
                self.usar_bomba()
                self.comodines["bomba"] = False

            if self.comodines["x2"] and self.boton_x2.esta_clickeado(evento.pos):
                self.usando_x2 = True
                self.comodines["x2"] = False

            if self.comodines["doble_chance"] and self.boton_doble.esta_clickeado(evento.pos):
                self.usando_doble_chance = True
                self.comodines["doble_chance"] = False

            if self.comodines["pasar"] and self.boton_pasar.esta_clickeado(evento.pos):
                self.pasar_pregunta()
                self.comodines["pasar"] = False
                return

            # Respuesta
            for i, (boton, letra) in enumerate(self.botones_opciones):
                if boton.esta_clickeado(evento.pos) and boton.habilitado:
                    if str(i+1) == self.pregunta_actual["respuesta_correcta"]:
                        puntos = PUNTUACION_ACIERTO
                        if self.usando_x2:
                            puntos *= 2
                            self.usando_x2 = False
                        self.puntaje += puntos
                        self.racha_aciertos += 1
                        if self.racha_aciertos == 5:
                            self.vidas += 1
                            self.racha_aciertos = 0
                        if EFECTOS_ACTIVADOS:
                            CLICK_SONIDO.set_volume(VOLUMEN_EFECTOS)
                            CLICK_SONIDO.play()
                        self.cargar_nueva_pregunta()
                        return
                    else:
                        if self.usando_doble_chance and not self.primer_intento_fallido:
                            self.primer_intento_fallido = True
                            boton.habilitado = False
                            if EFECTOS_ACTIVADOS:
                                ERROR_SONIDO.set_volume(VOLUMEN_EFECTOS)
                                ERROR_SONIDO.play()
                            return
                        else:
                            self.vidas -= 1
                            self.puntaje -= PUNTUACION_ERROR
                            self.racha_aciertos = 0
                            if EFECTOS_ACTIVADOS:
                                ERROR_SONIDO.set_volume(VOLUMEN_EFECTOS)
                                ERROR_SONIDO.play()
                            if self.vidas <= 0:
                                return "fin"
                            self.cargar_nueva_pregunta()
                            return

    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))

        lineas = Juego.renderizar_texto_multilinea(self.pregunta_actual["pregunta"], FUENTE_PREGUNTA, COLOR_BLANCO, ANCHO_PREGUNTA)
        y = 50
        x_cuadro = 80  # posición X donde empieza el cuadro de la pregunta

        for linea in lineas:
            texto_render = FUENTE_PREGUNTA.render(linea, True, COLOR_BLANCO)
            ancho_texto = texto_render.get_width()
            # Centrar cada línea dentro del cuadro de la pregunta
            x = x_cuadro + (ANCHO_PREGUNTA - ancho_texto) // 2
            self.pantalla.blit(texto_render, (x, y))
            y += FUENTE_PREGUNTA.get_height()

        for boton, _ in self.botones_opciones:
            boton.dibujar(self.pantalla)

        if self.comodines["bomba"]:
            self.boton_bomba.dibujar(self.pantalla)
        if self.comodines["x2"]:
            self.boton_x2.dibujar(self.pantalla)
        if self.comodines["doble_chance"]:
            self.boton_doble.dibujar(self.pantalla)
        if self.comodines["pasar"]:
            self.boton_pasar.dibujar(self.pantalla)

        texto_info = FUENTE_TEXTO.render(f"Puntaje: {self.puntaje}   Vidas: {self.vidas}", True, COLOR_AMARILLO)
        self.pantalla.blit(texto_info, (20, 10))
        texto_tiempo = FUENTE_TEXTO.render(f"Tiempo: {int(self.tiempo_restante)}s", True, COLOR_ROJO)
        self.pantalla.blit(texto_tiempo, (350, 10))

    def renderizar_texto_multilinea(texto, fuente, color, ancho_max):
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            if fuente.size(test_linea)[0] <= ancho_max:
                linea_actual = test_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        lineas.append(linea_actual)
        return lineas
    def usar_bomba(self):
    
        correcta = int(self.pregunta_actual["respuesta_correcta"]) - 1
    
        incorrectas = [i for i in range(len(self.botones_opciones)) if i != correcta]
   
        a_eliminar = random.sample(incorrectas, 2)
        for i in a_eliminar:
            self.botones_opciones[i][0].texto = ""  # Vacía el texto del botón para deshabilitarlo visualmente
            self.botones_opciones[i][0].habilitado = False  # Si tu clase Boton tiene este atributo
    def pasar_pregunta(self):
        self.pregunta_actual = random.choice(self.preguntas)
        self.botones_opciones = self.crear_botones_respuesta()
        self.bloqueado = False
        
    def guardar_partida(self, nombre):
        datos = {
            "nombre": nombre,
            "puntaje": self.puntaje,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open("partidas.json", "r", encoding="utf-8") as f:
                partidas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            partidas = []
        partidas.append(datos)
        with open("partidas.json", "w", encoding="utf-8") as f:
            json.dump(partidas, f, ensure_ascii=False, indent=4)
    
    
