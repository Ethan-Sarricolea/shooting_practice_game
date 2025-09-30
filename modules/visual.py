"""
Description: Modulo encargado del apartado visual del videojuego

Notas:
la función background_game: dibuja el fondo principal del mapa del juego
la función play_game: importa las imagenes y comienza el ciclo de la ventana de juego
    detecta el uso de teclas Q, W, E y ESCAPE

El movimiento del jugador se maneja por medio de columnas, al iniciar el jugador se encuentra en la columna 2
que esta en el medio, al moverse se guarda su posición de columna en la variable character_position

Autor: Sarricolea Cortés Ethan Yahel
"""

import pygame
from modules import logicgame
from threading import Thread,Lock
import sys

#Colors // https://htmlcolorcodes.com/es/
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255, 255, 0)
blue = (0,0,255)
grey = (200,200,200)
background_grey = (175, 175, 175 )
doors_grey = (100, 115, 120 )
floor_grey = (155, 155, 155)
grey_dark = (75, 75, 75 )
grey_bit_dark = (90,90,90)

class visualgame:
    def __init__(self,running,moduleLogic):
        pygame.init()
        pygame.mixer.init()
        self.sonido_disparo = pygame.mixer.Sound("modules\sources\gun_sound.mp3")
        self.sonido_correr = pygame.mixer.Sound("modules\sources\Running.mp3")
        self.running = running
        self.logicGame = moduleLogic
        self.game_size = (700,600)
        self.ventana = pygame.display.set_mode(self.game_size)
        self.ventana.fill(background_grey)
        pygame.display.set_caption("Shooting practice")
        self.door1Color = doors_grey
        self.door2Color = doors_grey
        self.door3Color = doors_grey

        self.continuar_hilo = True
        self.hilo_accion = Thread(target=self.logicGame.tiempo_espera, args=(self.continuar_hilo,))
        self.hilo_accion.start()

        self.play_game(self.ventana,self.running,self.logicGame)

    def background_game(self,ventana):
        for i in range(0,701,100):
                pygame.draw.line(ventana,color=floor_grey,start_pos=(i,0),end_pos=(i,600),width=10)
        for i in range(0,601,100):
            pygame.draw.line(ventana,color=floor_grey,start_pos=(0,i),end_pos=(700,i),width=10)

        pygame.draw.rect(ventana,self.door1Color,[(106,106),(90,90)])
        pygame.draw.rect(ventana,self.door2Color,[(306,106),(90,90)])
        pygame.draw.rect(ventana,self.door3Color,[(506,106),(90,90)])
        pygame.draw.line(ventana,color=grey_dark,start_pos=(0,450),end_pos=(700,450),width=30)


    def play_game(self,ventana,running,logic):
        self.logicgame = logic
        self.puntajeNum = 0

        self.textPuntaje = self.logicgame.puntaje_a_texto(self.puntajeNum)      #Funcion logica
        self.background_game(ventana)

        # Character / Personaje // https://es.pixilart.com/
        character_image1 = pygame.image.load("modules\sources\character.png")
        character_image2 = pygame.image.load("modules\sources\character_shooting.png")
        character = character_image1
        posX = 300
        posY = 500
        character_position = 2

        change_start_time = 0
        changing_image = False
        self.pause_activo = False

        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 50)
        puntaje_text = font.render(self.textPuntaje,True,white)
        pause_text = title_font.render("Pausa",True,white)

        clock = pygame.time.Clock()
        while running:

            ventana.blit(character,(posX,posY))
            ventana.blit(puntaje_text,(25,25))

            if self.pause_activo==False:                            #Si el juego NO esta en pausa
                
                if self.logicGame.objetivo_pos == 1:
                    self.door1Color = self.logicGame.objetivo_color
                    self.door2Color = doors_grey
                    self.door3Color = doors_grey
                    ventana.fill(background_grey)
                    self.background_game(ventana)
                    ventana.blit(character,(posX,posY))
                    ventana.blit(puntaje_text,(25,25))

                if self.logicGame.objetivo_pos == 2:
                    self.door2Color = self.logicGame.objetivo_color
                    self.door1Color = doors_grey
                    self.door3Color = doors_grey
                    ventana.fill(background_grey)
                    self.background_game(ventana)
                    ventana.blit(character,(posX,posY))
                    ventana.blit(puntaje_text,(25,25))

                if self.logicGame.objetivo_pos == 3:
                    self.door3Color = self.logicGame.objetivo_color
                    self.door2Color = doors_grey
                    self.door1Color = doors_grey
                    ventana.fill(background_grey)
                    self.background_game(ventana)
                    ventana.blit(character,(posX,posY))
                    ventana.blit(puntaje_text,(25,25))

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:                   #Cerrar el juego
                        running = False
                        sys.exit()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:                 # Al presionar la tecla Q
                            if (character_position>1):
                                self.sonido_correr.play()
                                character_position-=1
                                posX-=200
                                ventana.fill(background_grey)
                                self.background_game(ventana)
                            else:
                                print("Llegaste al tope")

                        if event.key == pygame.K_e:                 #Al presionar la tecla E
                            if (character_position<3):
                                self.sonido_correr.play()
                                character_position+=1
                                posX+=200
                                ventana.fill(background_grey)
                                self.background_game(ventana)
                            else:
                                print("Llegaste al tope")

                        if event.key == pygame.K_w:                 #Al presionar la tecla w
                            self.sonido_disparo.play()
                            self.acierto = self.logicGame.aparicion_objetivo(character_position)    #Acierto
                            if self.acierto:
                                if self.logicGame.objetivo_color == red: 
                                    self.puntajeNum -=10
                                elif self.logicGame.objetivo_color == yellow:
                                    self.puntajeNum +=5
                                elif self.logicGame.objetivo_color == green:
                                    self.puntajeNum +=10

                            ventana.fill(background_grey)
                            self.background_game(ventana)
                            self.textPuntaje = self.logicgame.puntaje_a_texto(self.puntajeNum)      #Funcion logica
                            puntaje_text = font.render(self.textPuntaje,True,white)
                            changing_image = True
                            change_start_time = pygame.time.get_ticks()

                        if event.key == pygame.K_ESCAPE:            #Al presionar ESCAPE
                            self.pause_activo = True
                            pygame.draw.rect(ventana,grey_bit_dark,[(100,100),(500,400)])
                            ventana.blit(pause_text,(300,150))

            elif self.pause_activo==True:                           #Si el juego esta en pausa
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                          running=False
                    if evento.type == pygame.KEYDOWN:  
                        if evento.key == pygame.K_ESCAPE:
                            self.pause_activo = False
                            ventana.fill(background_grey)
                            self.background_game(ventana)

            if changing_image:                                                  # Si se presiono E se realiza el cambio de imagen
                elapsed_time = pygame.time.get_ticks() - change_start_time      # Calcula el tiempo transcurrido
                if elapsed_time < 25:                                           # Si no sobrepasa el limite se queda la imagen2
                        character = character_image2
                else:
                        changing_image = False
                        character = character_image1
                        ventana.blit(character,(posX,posY))
            
            pygame.display.flip()
            clock.tick(30)
            if self.logicGame.logicRunning == False:
                running = False

        self.continuar_hilo = False
        self.hilo_accion.join()
        pygame.quit()