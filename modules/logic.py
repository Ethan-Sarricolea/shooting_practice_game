"""
Description: Modulo encarhado del funcionamiento logico del proyecto

Notas de funcionamiento:
La funcion pos_aleatoria una de las 3 columnas de aparición del objetivo
la función puntaje a texto convierte la suma de puntaje en texto para la visualización

Autor: Sarricolea Cortés Ethan Yahel
"""
import random
import time
from tkinter import messagebox

class logicgame:
    def __init__(self):
        print("logicGame inicializado")
        self.puntajeMaximo = 200
        self.logicRunning = True
        red = (255,0,0)
        green = (0,255,0)
        yellow = (255, 255, 0)
        self.objetive_colors = [red,green,yellow]
        column1 = 1
        column2 = 2
        column3 = 3
        self.columnas = [column1,column2,column3]
        
        
    def color_aleatorio(self):
        self.random_color = random.choice(self.objetive_colors)
        return self.random_color
    
    def pos_aleatoria(self):
        self.columna_aleatoria = random.choice(self.columnas)
        return self.columna_aleatoria
    
    def puntaje_a_texto(self,puntajeActual): #Conectada
        self.puntajeNum = puntajeActual
        self.puntajePrimerParte = "Puntaje: "
        self.textPuntaje = self.puntajePrimerParte + str(self.puntajeNum)
        return self.textPuntaje

    def tiempo_espera(self,continuar):
        while continuar:
            self.objetivo_pos = self.pos_aleatoria()
            self.objetivo_color = self.color_aleatorio()
            time.sleep(3)
            if self.puntajeNum>=self.puntajeMaximo:
                continuar = False
                print("Aleatoriedad terminada")
                messagebox.showinfo("¡Victoria!",self.textPuntaje)
                self.logicRunning = False
        
    def aparicion_objetivo(self,character_pos):
        if character_pos == self.objetivo_pos:
            return True
        else:
            return False
        
