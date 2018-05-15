
# -*- coding: utf-8 -*-

# Python:  3.5.0
# Script:  Mapz
# Versión: 1.6.8

import Arbol
import pygame
from pygame.locals import *
import explorer
import random
import sys, os

#===================================================================================================
#===================================================================================================
#===================================================================================================

# Clases:
 
class Personaje(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para El Personaje Principal.
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Personaje.
		
		pygame.sprite.Sprite.__init__(self)							# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)						# Carga La Imagen Con la función load_image.
		self.image = pygame.transform.flip(self.image, True, False)	# Gira La Imagen en Espejo de (Izquierda a Drecha en este caso).
		self.direccion = 'R'										# Indica que la posición Actual es volteando ahora a la derecha 'Right'.
		
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		
		self.image = pygame.transform.scale(self.image, (TX, TY))
	
	def flip(self, TX=True, TY=False):	# TX, Gira La Imagen De Izquierda a Derecha o viceversa, en espejo. TY Giraria de Arriba a Abajo o viceversa.
		
		self.image = pygame.transform.flip(self.image, TX, TY)
	
	def setDireccion(self, direccion): self.direccion = direccion	# Se Almacena La Direccion: 'L' (Left), 'R' (Right).
	
	def getDireccion(self): return self.direccion		# Devuelve el Valor de la Dirección Actual: 'L' o 'R'.


class Bloque(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Cada Tipo de Terreno.
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		
		self.image = pygame.transform.scale(self.image, (TX, TY))


class Boton(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Botones.
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		
		self.image = pygame.transform.scale(self.image, (TX, TY))


class Flecha(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Flechas.
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		
		self.image = pygame.transform.scale(self.image, (TX, TY))
	
	def rotate(self, Grados=90):	# Grados de Rotacion de la imagen.
		
		self.image = pygame.transform.rotate(self.image, Grados)


class BotonDir(pygame.sprite.Sprite, pygame.font.Font):		# Clase Para Los Botones De Dirección (Flechas Izquierda y Derecha)
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		
		self.image = pygame.transform.scale(self.image, (TX, TY))
	
	def flip(self, TX=True, TY=False):	# TX, Gira La Imagen De Izquierda a Derecha o viceversa, en espejo. TY Giraria de Arriba a Abajo o viceversa.
		
		self.image = pygame.transform.flip(self.image, TX, TY)


#===================================================================================================
#===================================================================================================
#===================================================================================================


# Función Que Dibuja La Matriz Para Cargar Los Terrenos. Dibuja El Mapa.
def dibujarMapa(XPOS, YPOS, screen, dimension, p_inicio, tamanio_fuente, Fuentes, SelTemp, Matriz, Lisy, Objetos, BtnMaskPressed):		# Dibuja El Mapa y Valida Todo Lo Necesiario para este.
	
	global SELECT, VALORES, seleccion, PuntoInicio, PuntoDestino, Mask
	global DibujarInfo, InfoSelTemp, Error, CadenaError, DibujarInfoXY
	
	'''
	# Función que dibuja el tablero
	XPOS:			Cantidad de Columnas (Letras)
	YPOS:			Cantidad de Fila (Numeros)
	screen: 		Objeto Principal, Referencia a la Vantana Para Dibujar en ella.
	dimension: 		Tamanio de Los Rectangulos. (Tamanio de los Terrenos en Pixeles)
	p_inicio: 		Coordenadas en Pixeles del Punto de Inicio del Mapa a Dibujar en La Ventana.
	tamanio_fuente: Tamanio de fuente para las letras y numeros de la matriz. (Margen)
	Fuentes: 		Diccionario con Fuentes de Letras.
	seleccion: 		Posición del Personaje.
	SelTemp: 		Posición de Selección Temporal Al Dar Clic.
	Matriz:			Matriz con los valores Cargados del Archivo.txt
	Lisy			Lista con los valores Ordenados y sin Repetir, Cargados del Archivo.txt
	Objetos:		Diccionario con los Objetos tipo Bloque Para Dibujarlos En La Pantalla, en su posición correspondiente.
	'''
	
	VALORES = []
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]		# Se Obtiene La Posición X en Pixeles, del Bloque Matriz[j][i]
			y = j * dimension + p_inicio[1]		# Se Obtiene La Posición Y en Pixeles, del Bloque Matriz[j][i]
			
			xp = (i+1) * dimension + p_inicio[0]	# Se Obtiene La Posición siguiente de X en Pixeles, del Bloque Matriz[j][i+1]
			yp = (j+1) * dimension + p_inicio[1]	# Se Obtiene La Posición siguiente de Y en Pixeles, del Bloque Matriz[j+1][i]
			
			DistX = xp - x		# Se Calcula La Distancia en Pixeles en X desde la Posición Matriz[i][j] hasta Matriz[i+1][j]
			DistY = yp - y		# Se Calcula La Distancia en Pixeles en Y desde la Posición Matriz[i][j] hasta Matriz[i][j+1]
			
			if Matriz[j][i] == Lisy[Pared]:	# Dibuja el Bloque de Pared.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Pared], 'Pared', Costos[NombrePersonaje[NumPlayer]][0]))
				
				if not Iniciar:
					
					Objetos['Pared'].resize(DistX, DistY)
					bloque = Objetos['Pared']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Pared'].resize(DistX, DistY)
					bloque = Objetos['Pared']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Camino]:	# Dibuja el Bloque de Camino.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Camino], 'Camino', Costos[NombrePersonaje[NumPlayer]][1]))
				
				if not Iniciar:
					
					Objetos['Camino'].resize(DistX, DistY)
					bloque = Objetos['Camino']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Camino'].resize(DistX, DistY)
					bloque = Objetos['Camino']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Bosque]:	# Dibuja el Bloque de Bosque.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Bosque], 'Bosque', Costos[NombrePersonaje[NumPlayer]][2]))
				
				if not Iniciar:
					
					Objetos['Bosque'].resize(DistX, DistY)
					bloque = Objetos['Bosque']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Bosque'].resize(DistX, DistY)
					bloque = Objetos['Bosque']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Lava]:	# Dibuja el Bloque de Lava.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Lava], 'Lava', Costos[NombrePersonaje[NumPlayer]][3]))
				
				if not Iniciar:
					
					Objetos['Lava'].resize(DistX, DistY)
					bloque = Objetos['Lava']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Lava'].resize(DistX, DistY)
					bloque = Objetos['Lava']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Agua]:	# Dibuja el Bloque de Agua.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Agua], 'Agua', Costos[NombrePersonaje[NumPlayer]][4]))
				
				if not Iniciar:
						
					Objetos['Agua'].resize(DistX, DistY)
					bloque = Objetos['Agua']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Agua'].resize(DistX, DistY)
					bloque = Objetos['Agua']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Arena]:	# Dibuja el Bloque de Arena.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Arena], 'Arena', Costos[NombrePersonaje[NumPlayer]][5]))
				
				if not Iniciar:
						
					Objetos['Arena'].resize(DistX, DistY)
					bloque = Objetos['Arena']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Arena'].resize(DistX, DistY)
					bloque = Objetos['Arena']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Montaña]:	# Dibuja el Bloque de Montaña.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Montaña], 'Montaña', Costos[NombrePersonaje[NumPlayer]][6]))
				
				if not Iniciar:
					
					Objetos['Montaña'].resize(DistX, DistY)
					bloque = Objetos['Montaña']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Montaña'].resize(DistX, DistY)
					bloque = Objetos['Montaña']
					screen.blit(bloque.image, (x,y))
					
			elif Matriz[j][i] == Lisy[Nieve]:	# Dibuja el Bloque de Nieve.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Montaña], 'Nieve', Costos[NombrePersonaje[NumPlayer]][7]))
				
				if not Iniciar:
					
					Objetos['Nieve'].resize(DistX, DistY)
					bloque = Objetos['Nieve']
					screen.blit(bloque.image, (x,y))
					
				elif Mask[j][i] == True or not BtnMaskPressed:
					
					Objetos['Nieve'].resize(DistX, DistY)
					bloque = Objetos['Nieve']
					screen.blit(bloque.image, (x,y))
			
			#===========================================================
			
			# Dibuja Temporalmente La Selección con el Clic en el Mapa.
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1:
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [x, y, dimension, dimension], 0)
				
				if Iniciar:
					
					DibujarInfo = True
					InfoSelTemp = SelTemp
					
			#===========================================================
			
			# Imprime Letra I en Estdo Inicial e Imprimir Letra F Para el Estado Final.
			if [LETRAS[i],j+1] == PuntoInicio:
				
				dibujarTexto(screen, 'I', [x + (DistX-20), y + (DistY-30)], Fuentes['Droid 30'], COLOR['Rojo'])
				
				MaskTrue(i, j, YPOS, XPOS)
				
			elif [LETRAS[i],j+1] == PuntoDestino:
				
				dibujarTexto(screen, 'F', [x + (DistX-20), y + (DistY-30)], Fuentes['Droid 30'], COLOR['Rojo'])
				Mask[j][i] = True
				
			#===========================================================
			
			# Si se Inicio el Juego Cargará el personaje en la posición de la seleccion.
			if PuntoInicio != None and Iniciar:
				
				if seleccion[0] == LETRAS[i] and j == seleccion[1] - 1:
					
					# Dibuja el Personaje Seleccionado.
					Objetos['Personaje'].resize(DistX, DistY)
					personaje = Objetos['Personaje']
					screen.blit(personaje.image, (x, y))
				
				# Imprimir El Recorrido: ===============================
				
				Pos = XPOS if XPOS > YPOS else YPOS		# Se obtiene el mayor de X y Y.
				TempCont = 0
				DT = dimension / 3
				DTY = dimension / 6
				
				if   Pos >= 10 and Pos < 13: F = 'Droid 8'
				elif Pos >= 7 and Pos < 10:  F = 'Droid 10'
				elif Pos >= 5 and Pos < 7:  F = 'Droid 15'
				elif Pos >= 2 and Pos < 5:  F = 'Droid 20'
				else: F = 'Droid 7'
				
				for Pos, Movs in SELECT:
					
					if [LETRAS[i],j+1] == Pos:
						
						for mov in Movs:
							
							if TempCont == len(Movs)-1: dibujarTexto(screen, str(mov), [x + ((TempCont%3)*DT), y + ((TempCont//3)*DTY)], Fuentes[F], COLOR['Rojo'])
							else: dibujarTexto(screen, str(mov)+',', [x + ((TempCont%3)*DT), y + ((TempCont//3)*DTY)], Fuentes[F], COLOR['Rojo'])
							
							TempCont += 1
				
				#=======================================================
			
			else:	# Se Elige El Punto De Inicio Y El Punto Destino Para El Personaje en el Mapa.
				
				if not DibujarInfoXY and not Iniciar and SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1:
					
					if seleccion != SelTemp:
						
						if PuntoInicio == None: PuntoInicio = SelTemp
						elif PuntoDestino == None: PuntoDestino = SelTemp
						else:
							
							if PuntoInicio != None and PuntoDestino != None:
								PuntoInicio = SelTemp
								PuntoDestino = None
						
						Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia la Matriz de Enmascaramiento del Mapa.
						
						seleccion = SelTemp
			
			#===========================================================
			
			# Si El Terreno Para Estado Inicial Elegido es igual a No Aplica, Manda Error Y No Selecciona ese Estado Inicial.
			for Valores in VALORES:
				if PuntoInicio == Valores[0]:
					if Valores[3] == '':	# Si El Peso es No Aplica, Entonces No Se Permitira Colocar ahi el Estado de Inicio.
						
						PuntoInicio	 = None
						PuntoDestino = None
						Error		 = True
						CadenaError = 'Costo N/A Para Estado Inicial'
						
						break
						
				if PuntoDestino == Valores[0]:
					if Valores[3] == '':	# Si El Peso es No Aplica, Entonces No Se Permitira Colocar ahi el Estado de Inicio.
						
						PuntoDestino = None
						Error		 = True
						CadenaError = 'Costo N/A Para Estado Final'
						
						break
			
			#===========================================================
			
			# Dibuja Los Numeros En Y
			if i == 0:
				
				dibujarTexto(screen, str(j + 1), 
				[p_inicio[0] - tamanio_fuente, j * dimension + p_inicio[1] + ((DistY // 2) - (tamanio_fuente//2))],		# Posición Centrada en su Fila Correspondiente.
				Fuentes['Alice 30'], 
				COLOR['Azul'])
			
		# Dibuja Las Letras En X
		dibujarTexto(screen, LETRAS[i], 
		[i * dimension + p_inicio[0] + ((DistX // 2) - 7), p_inicio[1] - tamanio_fuente],	# Posición Centrada en su Columna Correspondiente.
		Fuentes['Alice 30'], COLOR['Azul'])


def DibujarInformacionClic(screen, Fuentes, SelTemp):		# Dibuja La Información Cuando se le da Clic Derecho el Un Terreno del Mapa.
	
	Cont = 0
	Temp = False	# Si no hay Visitas se queda en False.
	NA = False	# Si no hay Visitas se queda en False.
	
	# Dibuja Toda La Información Al Dar Clic En Un Terreno.
	
	PosY = 110
	dibujarTexto(screen, 'Información', [919, PosY-1], Fuentes['Droid 25'], COLOR['Azul Claro'])
	dibujarTexto(screen, 'Información', [920, PosY], Fuentes['Droid 25'], COLOR['Azul'])
	
	PosY += 30
	dibujarTexto(screen, 'de Selección: ', [919, PosY-1], Fuentes['Droid 25'], COLOR['Azul Claro'])
	dibujarTexto(screen, 'de Selección: ', [920, PosY], Fuentes['Droid 25'], COLOR['Azul'])
	
	PosY += 40
	dibujarTexto(screen, 'Posición: ', [919, PosY-1], Fuentes['Droid 15'], COLOR['Azul Claro'])
	dibujarTexto(screen, 'Posición: ', [920, PosY], Fuentes['Droid 15'], COLOR['Azul'])
	dibujarTexto(screen, str(InfoSelTemp[0])+', '+str(InfoSelTemp[1]), [989, PosY-1], Fuentes['Droid 15'], COLOR['Verde Claro'])
	dibujarTexto(screen, str(InfoSelTemp[0])+', '+str(InfoSelTemp[1]), [990, PosY], Fuentes['Droid 15'], COLOR['Verde'])
	
	# Dibuja El Tipo De Terreno, extraido de la Lista Global VALORES que contiene La Información de Cada Bloque,
	# Los cuales son:  Posición en La Matriz,  Posicion en La Lista de Terrenos  y  Tipo de Terreno.
	
	PosY += 25
	
	for X in VALORES:
		
		if X[0] == InfoSelTemp:
			
			dibujarTexto(screen, 'Terreno: ', [919, PosY-1], Fuentes['Droid 15'], COLOR['Azul Claro'])
			dibujarTexto(screen, 'Terreno: ', [920, PosY], Fuentes['Droid 15'], COLOR['Azul'])
			dibujarTexto(screen, str(X[2]), [989, PosY-1], Fuentes['Droid 15'], COLOR['Verde Claro'])
			dibujarTexto(screen, str(X[2]), [990, PosY], Fuentes['Droid 15'], COLOR['Verde'])
			
			PosY += 25
			dibujarTexto(screen, 'Costo: ', [919, PosY-1], Fuentes['Droid 15'], COLOR['Azul Claro'])
			dibujarTexto(screen, 'Costo: ', [920, PosY], Fuentes['Droid 15'], COLOR['Azul'])
			
			if X[3] == '':
				NA = True
				dibujarTexto(screen, 'N/A', [989, PosY-1], Fuentes['Droid 15'], COLOR['Verde Claro'])
				dibujarTexto(screen, 'N/A', [990, PosY], Fuentes['Droid 15'], COLOR['Verde'])
			else:
				dibujarTexto(screen, str(round(float(X[3]),2)), [989, PosY-1], Fuentes['Droid 15'], COLOR['Verde Claro'])
				dibujarTexto(screen, str(round(float(X[3]),2)), [990, PosY], Fuentes['Droid 15'], COLOR['Verde'])
			
			break
	
	# Dibuja Si Es Estado Inicial O Final, el Terreno Seleccionado:
	
	PosY += 25
	dibujarTexto(screen, 'Estado: ', [919, PosY-1], Fuentes['Droid 15'], COLOR['Azul Claro'])
	dibujarTexto(screen, 'Estado: ', [920, PosY], Fuentes['Droid 15'], COLOR['Azul'])
	
	if InfoSelTemp == PuntoInicio:
		
		dibujarTexto(screen, 'Inicial', [1049, PosY], Fuentes['Droid 15'], COLOR['Rojo Claro'])
		dibujarTexto(screen, 'Inicial', [1050, PosY], Fuentes['Droid 15'], COLOR['Rojo'])
		
	elif InfoSelTemp == PuntoDestino:
		
		dibujarTexto(screen, 'Final', [1058, PosY], Fuentes['Droid 15'], COLOR['Rojo Claro'])
		dibujarTexto(screen, 'Final', [1059, PosY], Fuentes['Droid 15'], COLOR['Rojo'])
	
	# Dibujar Visitas:
	
	PosY += 25
	dibujarTexto(screen, 'Lista de Visitas: ', [919, PosY-1], Fuentes['Droid 15'], COLOR['Azul Claro'])
	dibujarTexto(screen, 'Lista de Visitas: ', [920, PosY], Fuentes['Droid 15'], COLOR['Azul'])
	
	PosY += 20
	
	# Recorre la lista con los Datos de las Visitas (Posición y Su Lista de Visitas.
	for Pos, Visits in SELECT:
		
		if InfoSelTemp == Pos:
			
			Temp = True		# Si hubo Visitas, entonces será True.
			
			for vis in Visits:
				
				if Cont == len(Visits)-1:
					dibujarTexto(screen, str(vis), [919 + ((Cont%5)*35), PosY + ((Cont//5)*15)], Fuentes['Droid 15'], COLOR['Rojo Claro'])
					dibujarTexto(screen, str(vis), [920 + ((Cont%5)*35), PosY + ((Cont//5)*15)], Fuentes['Droid 15'], COLOR['Rojo'])
				else:
					dibujarTexto(screen, str(vis)+',', [919 + ((Cont%5)*35), PosY + ((Cont//5)*15)], Fuentes['Droid 15'], COLOR['Rojo Claro'])
					dibujarTexto(screen, str(vis)+',', [920 + ((Cont%5)*35), PosY + ((Cont//5)*15)], Fuentes['Droid 15'], COLOR['Rojo'])
				
				Cont += 1
				
			break
	
	# Si hubo Visitas:
	if Temp: dibujarTexto(screen, 'Visitado', [975, PosY-45], Fuentes['Droid 15'], COLOR['Naranja'])
	else: # Si no...
		if NA:
			dibujarTexto(screen, 'N/A', [990, PosY-45], Fuentes['Droid 15'], COLOR['Naranja'])	
			dibujarTexto(screen, 'N/A', [920, PosY],    Fuentes['Droid 15'], COLOR['Naranja'])	
		else:
			dibujarTexto(screen, 'No Visitado', [975, PosY-45], Fuentes['Droid 15'], COLOR['Naranja'])	
			dibujarTexto(screen, 'Sin Visitas', [920, PosY],    Fuentes['Droid 15'], COLOR['Naranja'])	



#===================================================================================================

def dibujarTexto(screen, texto, posicion, fuente, color):		# Dibuja Texto En Pantalla.
	
	Texto = fuente.render(texto, 1, color)		# Se Pasa El Texto Con La Fuente Especificada.
	screen.blit(Texto, posicion)				# Se Dibuja En Pantalla El Texto en la Posición Indicada.

#===================================================================================================

def ajustarMedidas(POS, tamanio_fuente):		# Ajusta el Recuadro del Mapa (la Seccion Centro) en las Medidas Ajustadas al Tamaño de la Ventana.
	
	# Para Imprimir La Matriz:
	MargenX = 300
	MargenY = 10
	
	ancho = int((DIMENCIONES[1] - (tamanio_fuente * 2)) / POS)
	inicio = tamanio_fuente + MargenX, tamanio_fuente + MargenY
	
	return [inicio, ancho]

#===================================================================================================

def obtenerPosicionClic(XPOS, YPOS, mouse, dimension, p_inicio, actual):		# Obtiene La Coordenada del Mapa en la que se le de clic.
	
	xr, yr = mouse[0], mouse[1]
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]
			y = j * dimension + p_inicio[1]
			
			if (xr >= x) and (xr <= x + dimension) and (yr >= y) and (yr <= y + dimension):
				actual = [LETRAS[i], j + 1]
				return actual
			else: actual = ['P',16]
			
	return actual



def DibujarCaminoBacktracing(screen, XPOS, YPOS, dimension, p_inicio, Seleccion, Lista):		# Dibuja El Camino Más Corto Hecho Con Backtracking.
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			Actual = [LETRAS[i], j + 1]
			
			if Actual in Lista:
				
				x = i * dimension + p_inicio[0]
				y = j * dimension + p_inicio[1]
				
				if Actual == PuntoInicio or Actual == PuntoDestino: pygame.draw.circle(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], 6)
					
				Padre = Lista[Lista.index(Actual)-1]
				try: Hijo = Lista[Lista.index(Actual)+1]
				except: Hijo = Seleccion
				
				X1 = LETRAS.index(Actual[0])
				Y1 = Actual[1]
				# ~ print(Padre == [LETRAS[X1], Y1+1])
				# ~ Pause()
				if Padre == [LETRAS[X1], Y1-1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x+(dimension//2), y], 5)
				if Padre == [LETRAS[X1+1], Y1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x+dimension, y+(dimension//2)], 5)
				if Padre == [LETRAS[X1], Y1+1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x+(dimension//2), y+dimension], 5)
				if Padre == [LETRAS[X1-1], Y1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x, y+(dimension//2)], 5)
				
				#===================================================
				
				if Hijo == [LETRAS[X1], Y1-1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x+(dimension//2), y], 5)
				if Hijo == [LETRAS[X1+1], Y1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x+dimension, y+(dimension//2)], 5)
				if Hijo == [LETRAS[X1], Y1+1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x+(dimension//2), y+dimension], 5)
				if Hijo == [LETRAS[X1-1], Y1]:
					pygame.draw.line(screen, COLOR['Morado'], [x+(dimension//2), y+(dimension//2)], [x, y+(dimension//2)], 5)



#===================================================================================================

def obtenerPosicion(XPOS, YPOS, Dir, Actual, personaje, ArbolRaiz):		# Obtiene la posicion para cada movimiento del Personaje en el Mapa.
	
	global SELECT, Movimientos, CostoTotal
	
	Padre = Actual
	PosLetra = LETRAS.index(Actual[0])
	
	x, y = PosLetra, Actual[1]
	
	if Dir == 'U':
		
		if   Actual[0] in LETRAS and Actual[1] == 1: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(2,YPOS+1)]:
			
			y -= 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[3] == '': pass
					else:
						
						MaskTrue(x, y-1, YPOS, XPOS)
						
						CostoTotal += float(z[3])
						
						Actual = [Actual[0],Actual[1]-1]
						
						Add = False
						Movimientos += 1
						
						for Pos, Movs in SELECT:
							
							if Actual == Pos:
								Movs.append(Movimientos)
								Add = False
								break
								
							else: Add = True
							
						if Add: SELECT.append((Actual, [Movimientos]))
						
						AgregarAlArbol(ArbolRaiz, Padre, Actual, x, y, YPOS, XPOS)
						
						break
		
	elif Dir == 'D':
		
		if   Actual[0] in LETRAS and Actual[1] == YPOS: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(1,YPOS)]:
			
			y += 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[3] == '': pass
					else:
						
						MaskTrue(x, y-1, YPOS, XPOS)
						
						CostoTotal += float(z[3])
						
						Actual = [Actual[0],Actual[1]+1]
						
						Add = False
						Movimientos += 1
						
						for Pos, Movs in SELECT:
							
							if Actual == Pos:
								Movs.append(Movimientos)
								Add = False
								break
								
							else: Add = True
							
						if Add: SELECT.append((Actual, [Movimientos]))
						
						AgregarAlArbol(ArbolRaiz, Padre, Actual, x, y, YPOS, XPOS)
						
						break
		
	elif Dir == 'L':
		
		if personaje.getDireccion() == 'R':
			
			personaje.flip()
			personaje.setDireccion('L')
			
		if   Actual[0] == LETRAS[0]  and Actual[1] in [x for x in range(1,YPOS+1)]:	pass
		elif Actual[0] in LETRAS[1:] and Actual[1] in [x for x in range(1,YPOS+1)]:
			
			x -= 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[3] == '': pass
					else:
						
						MaskTrue(x, y-1, YPOS, XPOS)
						
						CostoTotal += float(z[3])
						
						Actual = [LETRAS[PosLetra-1],Actual[1]]
						
						Add = False
						Movimientos += 1
						
						for Pos, Movs in SELECT:
							
							if Actual == Pos:
								Movs.append(Movimientos)
								Add = False
								break
								
							else: Add = True
							
						if Add: SELECT.append((Actual, [Movimientos]))
						
						AgregarAlArbol(ArbolRaiz, Padre, Actual, x, y, YPOS, XPOS)
						
						break
		
	elif Dir == 'R':
		
		if personaje.getDireccion() == 'L':
			
			personaje.flip()
			personaje.setDireccion('R')
			
		if   Actual[0] == LETRAS[XPOS-1]   and Actual[1] in [x for x in range(1,YPOS+1)]: pass
		elif Actual[0] in LETRAS[0:XPOS-1] and Actual[1] in [x for x in range(1,YPOS+1)]:
			
			x += 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[3] == '': pass
					else:
						
						MaskTrue(x, y-1, YPOS, XPOS)
						
						CostoTotal += float(z[3])
						
						Actual = [LETRAS[PosLetra+1],Actual[1]]
						
						Add = False
						Movimientos += 1
						
						for Pos, Movs in SELECT:
							
							if Actual == Pos:
								Movs.append(Movimientos)
								Add = False
								break
								
							else: Add = True
							
						if Add: SELECT.append((Actual, [Movimientos]))
						
						AgregarAlArbol(ArbolRaiz, Padre, Actual, x, y, YPOS, XPOS)
						
						break
		
	return Actual



def MaskTrue(X, Y, YPOS, XPOS):		# Pone En True La Posicion Actual del Personaje y sus 4 lados de esa posicion, en la Matriz de Enmascaramiento Para El Mapa.
	
	global Mask
	
	Mask[Y][X] = True
	if Y > 0:		Mask[Y-1][X] = True	
	if Y < YPOS-1:	Mask[Y+1][X] = True
	if X > 0:		Mask[Y][X-1] = True
	if X < XPOS-1:	Mask[Y][X+1] = True



def AgregarAlArbol(ArbolRaiz, Padre, Actual, X, Y, YPOS, XPOS):		# XPOS y YPOS son Las Medidad Del Mapa, desde 2x2 hasta 15x15.
	
	global VISITA, NoRepetir
	
	VISITA += 1
	
	# ~ NoRepetir = True	# Sin Repetir Los Nodos.
	AlFinal = True		# Si Se Repiten Nodos, Agrega Hasta El Padre Más Alejado Correspondiente, Si es False, Agrega al Padre Más Próximo Correspondiente.
	
	Up    = [LETRAS[X], Y-1]
	Right = [LETRAS[X+1], Y]
	Down  = [LETRAS[X], Y+1]
	Left  = [LETRAS[X-1], Y]
	
	Lista = [Up, Right, Down, Left]
	
	# Verifica que sean Coordenadas Con Costos, Los que son N/A No se agregan al Árbol.
	#==================================================================================
	
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(1)] and x[3] != '':
			# ~ if Y > 1 and  Y < YPOS and  X > 0 and X < XPOS-1:
				Arbol.Agregar(ArbolRaiz, Actual, Lista[Direcciones.index(1)], NoRepetir, AlFinal)		# Se Crea Un Nodo Hijo Para El Nodo Actual.
	
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(2)] and x[3] != '':
			# ~ if Y > 1 and  Y < YPOS and  X > 0 and X < XPOS-1:
				Arbol.Agregar(ArbolRaiz, Actual, Lista[Direcciones.index(2)], NoRepetir, AlFinal)		# Se Crea Un Nodo Hijo Para El Nodo Actual.
	
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(3)] and x[3] != '':
			# ~ if Y > 1 and  Y < YPOS and  X > 0 and X < XPOS-1:
				Arbol.Agregar(ArbolRaiz, Actual, Lista[Direcciones.index(3)], NoRepetir, AlFinal)		# Se Crea Un Nodo Hijo Para El Nodo Actual.
	
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(4)] and x[3] != '':
			# ~ if Y > 1 and  Y < YPOS and  X > 0 and X < XPOS-1:
				Arbol.Agregar(ArbolRaiz, Actual, Lista[Direcciones.index(4)], NoRepetir, AlFinal)		# Se Crea Un Nodo Hijo Para El Nodo Actual.
	#==================================================================================
	
	Val = Arbol.ExtraerDatos(ArbolRaiz, Padre, Actual)
	
	if Val[0]:
		if Val[1]['Padre'] == None:
			Arbol.AgregarPadre(ArbolRaiz, Actual, Padre)				# Se le agrega al Nodo Actual cual es su Padre.
	
	Arbol.AgregarOrden(ArbolRaiz, Actual, VISITA)			# Se Agrega La Lista Con El Orden De Visitas.
	
	if Val[0]:
		if Val[1]['Hijos'] == []:
			
			if Arbol.BusquedaPrecisa(ArbolRaiz, Actual, Lista[Direcciones.index(1)]):
				Arbol.AgregarPadre(ArbolRaiz, Lista[Direcciones.index(1)], Actual)			# Se Le agrega a los Hijos del Nodo Actual, el Nodo Actual Como Padre (Solo La Coordenada).
				Arbol.AgregarHijos(ArbolRaiz, Actual, Lista[Direcciones.index(1)])			# Se Le agrega una lista de Hijos al Nodo Actual (Solo las Coordenadas).
			if Arbol.BusquedaPrecisa(ArbolRaiz, Actual, Lista[Direcciones.index(2)]):
				Arbol.AgregarPadre(ArbolRaiz, Lista[Direcciones.index(2)], Actual)
				Arbol.AgregarHijos(ArbolRaiz, Actual, Lista[Direcciones.index(2)])
			if Arbol.BusquedaPrecisa(ArbolRaiz, Actual, Lista[Direcciones.index(3)]):
				Arbol.AgregarPadre(ArbolRaiz, Lista[Direcciones.index(3)], Actual)
				Arbol.AgregarHijos(ArbolRaiz, Actual, Lista[Direcciones.index(3)])
			if Arbol.BusquedaPrecisa(ArbolRaiz, Actual, Lista[Direcciones.index(4)]):
				Arbol.AgregarPadre(ArbolRaiz, Lista[Direcciones.index(4)], Actual)
				Arbol.AgregarHijos(ArbolRaiz, Actual, Lista[Direcciones.index(4)])
	
	# Se Indica Si Es El Nodo Inicial.
	if Actual == PuntoInicio:    Arbol.AgregarIniFin(ArbolRaiz, Actual, True)
	elif Actual == PuntoDestino: Arbol.AgregarIniFin(ArbolRaiz, Actual, False, True)
	
	Arbol.AgregarEstado(ArbolRaiz, Actual, 'Cerrado')	# Si el Nodo es Visitado, Es Cerrado.



def MostrarArbol(arbol, screen, PX, PY, X1, Y1, Fuentes):		# Muestra EL Arbol de Forma Grafica. (Recorrido en Profundidad).
	
	pygame.draw.rect(screen, COLOR['Blanco'], [PX, PY, X1+120, Y1], 0)		# Dibuja El Cuadro Para Cada Nodo.
	
	dibujarTexto(screen, 'Coordenada:    ' + str(arbol.Coord), [PX+6, PY+6], Fuentes['Droid 12'], COLOR['Azul'])
	dibujarTexto(screen, 'Coordenada:    ' + str(arbol.Coord), [PX+7, PY+6], Fuentes['Droid 12'], COLOR['Negro'])
	
	dibujarTexto(screen, 'Padre:    ' + str(arbol.Padre), [PX+6, PY+18],  Fuentes['Droid 12'], COLOR['Azul'])
	dibujarTexto(screen, 'Padre:    ' + str(arbol.Padre), [PX+7, PY+18],  Fuentes['Droid 12'], COLOR['Negro'])
	
	if arbol.Hijos == []:
		dibujarTexto(screen, 'Hijos:      Ninguno', [PX+6, PY+30], Fuentes['Droid 12'], COLOR['Azul'])
		dibujarTexto(screen, 'Hijos:      Ninguno', [PX+7, PY+30], Fuentes['Droid 12'], COLOR['Negro'])
	else:
		dibujarTexto(screen, 'Hijos:      ' + str(arbol.PHijos), [PX+6, PY+30], Fuentes['Droid 12'], COLOR['Azul'])
		dibujarTexto(screen, 'Hijos:      ' + str(arbol.PHijos), [PX+7, PY+30], Fuentes['Droid 12'], COLOR['Negro'])
	
	if arbol.Orden == []:
		dibujarTexto(screen, 'Visitas:   Sin Visitas', [PX+6, PY+42], Fuentes['Droid 12'], COLOR['Azul'])
		dibujarTexto(screen, 'Visitas:   Sin Visitas', [PX+7, PY+42], Fuentes['Droid 12'], COLOR['Negro'])
	else:
		dibujarTexto(screen, 'Visitas:   ' + str(arbol.Orden), [PX+6, PY+42], Fuentes['Droid 12'], COLOR['Azul'])
		dibujarTexto(screen, 'Visitas:   ' + str(arbol.Orden), [PX+7, PY+42], Fuentes['Droid 12'], COLOR['Negro'])
	
	dibujarTexto(screen, 'Estado:   ' + str(arbol.Estado), [PX+6, PY+54], Fuentes['Droid 12'], COLOR['Azul'])
	dibujarTexto(screen, 'Estado:   ' + str(arbol.Estado), [PX+7, PY+54], Fuentes['Droid 12'], COLOR['Negro'])
	
	if arbol.EsIni: 
		dibujarTexto(screen, 'EsInicial:  Si', [PX+6, PY+78], Fuentes['Droid 12'], COLOR['Azul'])
		dibujarTexto(screen, 'EsInicial:  Si', [PX+7, PY+78], Fuentes['Droid 12'], COLOR['Negro'])
	
	if arbol.EsFin: 
		dibujarTexto(screen, 'EsFinal:    Si', [PX+6, PY+78], Fuentes['Droid 12'], COLOR['Azul'])
		dibujarTexto(screen, 'EsFinal:    Si', [PX+7, PY+78], Fuentes['Droid 12'], COLOR['Negro'])
	
	PY += Y1+20
	
	for hijo in arbol.Hijos:
		
		xD = Arbol.ContadorDeNodos(hijo, 0)
		
		if arbol.Hijos.index(hijo) != arbol.Hijos.index(arbol.Hijos[-1]):		# Rellena Los Espacios Faltante de las Conexiones de Nodos.
			for x in range(xD): pygame.draw.line(screen, COLOR['Rojo'], [ PX+int(X1/2), (PY-20) + ((Y1) * x) ], [ PX+int(X1/2), PY+int(X1/2) + ((Y1+20) * x) + 50], 10)
		
		pygame.draw.line(screen, COLOR['Rojo'], [ PX+int(X1/2), PY-20 ],        [ PX+int(X1/2),    PY+int(X1/2) + 5 ], 10)
		pygame.draw.line(screen, COLOR['Rojo'], [ PX+int(X1/2), PY+int(X1/2) ], [ PX+int(X1/2)+X1, PY+int(X1/2) ], 10)
		
		MostrarArbol(hijo, screen, PX+X1+50, PY, X1, Y1, Fuentes)
		
		PY += (Y1+20) * xD



#===================================================================================================
#===================================================================================================
#===================================================================================================



def Backtracking(XPOS, YPOS, Padre, ArbolRaiz, Abue=[]):
	
	global Direcciones, ListaHijos
	global Movimientos, Pila
	
	# ~ os.system('cls')
	
	Hijos = []
	xD = False
	
	X = LETRAS.index(Padre[0])
	Y = Padre[1]
	
	Up    = [LETRAS[X], Y-1]
	Right = [LETRAS[X+1], Y]
	Down  = [LETRAS[X], Y+1]
	Left  = [LETRAS[X-1], Y]
	
	Lista = [Up, Right, Down, Left]
	
	if Padre != PuntoInicio and Abue == []: Abue = Pila[-2][0]
	
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(1)] and x[3] != '' and not Abue == x[0]: Hijos.append(Lista[Direcciones.index(1)]); break
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(2)] and x[3] != '' and not Abue == x[0]: Hijos.append(Lista[Direcciones.index(2)]); break
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(3)] and x[3] != '' and not Abue == x[0]: Hijos.append(Lista[Direcciones.index(3)]); break
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(4)] and x[3] != '' and not Abue == x[0]: Hijos.append(Lista[Direcciones.index(4)]); break
	
	for x in ListaHijos:
		if Padre == x[0]: xD = True; break
	
	if xD == False: ListaHijos.append([Padre, Hijos, []])
	
	Movimientos += 1
	
	for Pos, Hijs, Movs in ListaHijos:
		if Pos == Padre:
			if Hijs != []:
				
				Movs.append(Movimientos)
				Pila[-1][1].append(Movimientos)
				
				Pila.append((Hijs[0], [Movimientos]))
				
				X = ListaHijos.index([Pos, Hijs, Movs])
				ListaHijos[X][1].pop(0)
				
			else: Pila.pop()
			
			break
			
	# ~ print('\n\nPila:')
	# ~ for x in Pila: print(x)
	
	# ~ print('\n\nLista:')
	# ~ for x in ListaHijos: print(x)
	
	Actual = Pila[-1][0]
	
	AgregarAlArbolBacktracking(Actual, Padre, XPOS, YPOS, ArbolRaiz)
	
	return Actual


def AgregarAlArbolBacktracking(Actual, Padre, XPOS, YPOS, ArbolRaiz):
	
	global Direcciones, SELECT, NoRepetir
	global Movimientos, CostoTotal
	
	AlFinal = True
	xD = False
	
	for z in VALORES:
		if z[0] == Actual: CostoTotal += float(z[3]); break
	
	for Pos, Movs in SELECT:
		
		if Actual == Pos:
			Movs.append(Movimientos)
			xD = False
			break
			
		else: xD = True
		
	if xD: SELECT.append((Actual, [Movimientos]))
	
	MaskTrue(LETRAS.index(Actual[0]), Actual[1]-1, YPOS, XPOS)
	
	Arbol.Agregar(ArbolRaiz, Padre, Actual, NoRepetir, AlFinal)		# Se Crea Un Nodo Hijo Para El Nodo Actual.
	Arbol.AgregarOrden(ArbolRaiz, Actual, Movimientos)				# Se Agrega La Lista Con El Orden De Visitas.
	
	Val = Arbol.ExtraerDatos(ArbolRaiz, Padre, Actual)
	
	if Val[0]:
		if Val[1]['Padre'] == None:
			Arbol.AgregarPadre(ArbolRaiz, Actual, Padre)				# Se le agrega al Nodo Actual cual es su Padre.
	
	if Val[0]:
		if Val[1]['Hijos'] == []:
			if Arbol.BusquedaPrecisa(ArbolRaiz, Padre, Actual):
				
				# ~ Arbol.AgregarHijos(ArbolRaiz, Padre, Actual)			# Se Le agrega una lista de Hijos al Nodo Actual (Solo las Coordenadas).
				
				#================================================================================
				X_2 = LETRAS.index(Actual[0])
				Y_2 = Actual[1]
				
				Up_2    = [LETRAS[X_2], Y_2-1]
				Right_2 = [LETRAS[X_2+1], Y_2]
				Down_2  = [LETRAS[X_2], Y_2+1]
				Left_2  = [LETRAS[X_2-1], Y_2]
				
				Lista_2 = [Up_2, Right_2, Down_2, Left_2]
				
				# Se Le agrega a lista de Hijos sus Hijos (Solo las Coordenadas).
				for x in VALORES:
					if x[0] == Lista_2[Direcciones.index(1)] and x[3] != '' and not Padre == x[0]:
						Arbol.AgregarHijos(ArbolRaiz, Actual, Lista_2[Direcciones.index(1)]); break
				for x in VALORES:
					if x[0] == Lista_2[Direcciones.index(2)] and x[3] != '' and not Padre == x[0]:
						Arbol.AgregarHijos(ArbolRaiz, Actual, Lista_2[Direcciones.index(2)]); break
				for x in VALORES:
					if x[0] == Lista_2[Direcciones.index(3)] and x[3] != '' and not Padre == x[0]:
						Arbol.AgregarHijos(ArbolRaiz, Actual, Lista_2[Direcciones.index(3)]); break
				for x in VALORES:
					if x[0] == Lista_2[Direcciones.index(4)] and x[3] != '' and not Padre == x[0]:
						Arbol.AgregarHijos(ArbolRaiz, Actual, Lista_2[Direcciones.index(4)]); break
				#================================================================================
	
	# Se Indica Si Es El Nodo Inicial.
	if Actual == PuntoInicio:    Arbol.AgregarIniFin(ArbolRaiz, Actual, True)
	elif Actual == PuntoDestino: Arbol.AgregarIniFin(ArbolRaiz, Actual, False, True)
	
	Arbol.AgregarEstado(ArbolRaiz, Actual, 'Cerrado')	# Si el Nodo es Visitado, Es Cerrado.



def DistanciaManhattan(Coord):
	
	X1 = LETRAS.index(Coord[0]) + 1
	Y1 = Coord[1]
	
	X2 = LETRAS.index(PuntoDestino[0]) + 1
	Y2 = PuntoDestino[1]
	
	X = X1 - X2
	X = -X if X < 0 else X
	Y = Y1 - Y2
	Y = -Y if Y < 0 else Y
	
	return X + Y



def AEstrella(XPOS, YPOS, Padre, ArbolRaiz, Abue=[]):
	
	global Direcciones, ListaHijos
	global Movimientos, Pila
	
	os.system('cls')
	
	Hijos = []
	xD = False
	
	X = LETRAS.index(Padre[0])
	Y = Padre[1]
	
	Up    = [LETRAS[X], Y-1]
	Right = [LETRAS[X+1], Y]
	Down  = [LETRAS[X], Y+1]
	Left  = [LETRAS[X-1], Y]
	
	Lista = [Up, Right, Down, Left]
	
	# ~ if Padre != PuntoInicio and Abue == []: Abue = Pila[-2][0]
	
	xD = False
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(1)] and x[3] != '':
			for y in Pila:
				if not Lista[Direcciones.index(4)] == y[0]: xD = True
			if xD == False: Pila.append([Lista[Direcciones.index(1)], DistanciaManhattan(Lista[Direcciones.index(1)])])
			break
	
	xD = False
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(2)] and x[3] != '':
			for y in Pila:
				if not Lista[Direcciones.index(4)] == y[0]: xD = True
			if xD == False: Pila.append([Lista[Direcciones.index(2)], DistanciaManhattan(Lista[Direcciones.index(2)])])
			break
	
	xD = False
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(3)] and x[3] != '':
			for y in Pila:
				if not Lista[Direcciones.index(4)] == y[0]: xD = True
			if xD == False: Pila.append([Lista[Direcciones.index(3)], DistanciaManhattan(Lista[Direcciones.index(3)])])
			break
	
	xD = False
	for x in VALORES:
		if x[0] == Lista[Direcciones.index(4)] and x[3] != '':
			for y in Pila:
				if not Lista[Direcciones.index(4)] == y[0]: xD = True
			if xD == False: Pila.append([Lista[Direcciones.index(4)], DistanciaManhattan(Lista[Direcciones.index(4)])])
			break
	
	# ~ for x in ListaHijos:
		# ~ if Padre == x[0]: xD = True; break
	
	# ~ if xD == False: ListaHijos.append([Padre, Hijos, []])
	
	# ~ Val = DistanciaManhattan(Padre)
	
	Menor = [None, 1000]
	
	Cont = 0
	for x in Pila:
		
		if x[1] < Menor[1]: Menor = x
		Cont += 1
		print('\t', Cont, '-', x)
	
	print('\n\tMenor:',Menor)
	
	return Menor[0]



#===================================================================================================
#===================================================================================================
#===================================================================================================

def AbrirArchivo():
	
	global Error, CadenaError
	
	Cadena = ''
	Nombre = explorer.Explorer.GetFileName(DirInicial=os.getcwd()+'/Mapas')
	
	if Nombre == None:
		
		CadenaError = ''
		Error = True
		return None
	
	with open(Nombre, 'r') as Archivo: Cadena = Archivo.read()
	Archivo.close()
	
	return Cadena

#===================================================================================================

def ObtenerMatriz(Cadena):
	
	global Error, CadenaError
	
	if Cadena == '':
		
		CadenaError = 'Archivo Vacío.'
		Error = True
		return None
	
	# Remplazamos de la Cadena los espacios y tabulaciones por cadenas vacia
	# Luego Generamos una lista que estara dividida por cada salto de linea:
	Lista = Cadena.replace(' ', '').replace('\t', '').split('\n')
	
	# Cuenta cuantos objetos de la lista son vacios y luego los elimina de la lista cada uno:
	for x in range(Lista.count('')): Lista.remove('')
	
	Matriz = []
	Longitud = len(Lista[0].replace(' ','').replace('\t','').split(','))
	
	for x in Lista:
		
		x = x.replace(' ','').replace('\t','').split(',')
		
		if not Longitud == len(x): return True
		
		Longitud = len(x)
		Matriz.append(x)
	
	for x in Matriz:
		for y in x:
			if not y.isdigit(): return False
			
	return Matriz

#===================================================================================================

def Pause(Quiet = False): os.system('Pause') if Quiet == False else os.system('Pause > Nul')

#===================================================================================================

def load_image(filename, transparent=False):
	
	global Error
	
	try: image = pygame.image.load(filename)
	except pygame.error as message: raise SystemError
	
	image = image.convert()
	
	if transparent:
		
		color = image.get_at((0,0))
		image.set_colorkey(color, RLEACCEL)
		
	return image

#===================================================================================================

def TODOArchivo():
	
	global Error, CadenaError
	
	Cadena = AbrirArchivo()
	
	if Cadena == None: return None, None, None, None, None
	
	Matrixy = ObtenerMatriz(Cadena)
	
	if Matrixy == None: return None, None, None, None, None
	
	if Matrixy == True:
		
		CadenaError = 'Archivo No Compatible.'
		Error = True
		return None, None, None, None, None
		
	elif Matrixy == False:
		
		CadenaError = 'Archivo No Compatible.'
		Error = True
		return None, None, None, None, None
	
	Lisy = []
	
	for x in Matrixy:
		for y in x:
			if not y in Lisy: Lisy.append(y)
	
	Lisy = sorted(Lisy)
	
	XPOS = len(Matrixy[0])
	YPOS = len(Matrixy)
	
	POS  = (XPOS if XPOS > YPOS else YPOS)
	
	if XPOS <= 1 or YPOS <= 1:
		
		CadenaError = 'Cuadrícula Mínima: 2x2.'
		Error = True
		return None, None, None, None, None
		
	elif XPOS >= 16 or YPOS >= 16:
		
		CadenaError = 'Cuadrícula Máxima: 15x15.'
		Error = True
		return None, None, None, None, None
	
	return Matrixy, Lisy, XPOS, YPOS, POS

#===================================================================================================

def DibujarMiniaturaTextura(screen, Costo, TextInput, Objetos, BtnIzq, BtnDer, X, Y, Nombre, List, LisyPosX, Fuentes, Repetido=False):
	
	# Dibuja un Recuadro Blanco con Contorno Negro Para La Miniatura.
	pygame.draw.rect(screen, COLOR['Blanco'], [X, Y, 35, 35], 0)
	if Repetido: pygame.draw.rect(screen, COLOR['Rojo'],  [X, Y, 35, 35], 2)
	else: pygame.draw.rect(screen, COLOR['Negro'],  [X, Y, 35, 35], 2)
	
	# Ajusta El Tamaño de la Imagen Para La Miniatura.
	Objetos[Nombre].resize(34, 34)
	bloque = Objetos[Nombre]
	screen.blit(bloque.image, (X+1,Y+1))		# Coloca La Miniatura.
	
	# Dibuja Los Botones Izquierda y Derecha Para Cambiar Valores.
	dibujarTexto(screen, 'Tipo:   ' + Nombre, [X+40, Y-5], Fuentes['Droid 20'], COLOR['Negro'])
	
	# Imprime el Input Para los Costos en Pared.
	dibujarTexto(screen, 'Costo:', [X+40, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	if Costo: pygame.draw.rect(screen, COLOR['Blanco'], [X+98, Y+17, 80, 20], 0)
	else: pygame.draw.rect(screen, COLOR['Gris Claro'], [X+98, Y+17, 80, 20], 0)
	
	if NumPlayer != None:
		if Costos[NombrePersonaje[NumPlayer]][TextInput] == '': dibujarTexto(screen, 'N/A', [X+100, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
		else:
			if '.' in Costos[NombrePersonaje[NumPlayer]][TextInput]: dibujarTexto(screen, str(round(float(Costos[NombrePersonaje[NumPlayer]][TextInput]),2)), [X+100, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
			else: dibujarTexto(screen, Costos[NombrePersonaje[NumPlayer]][TextInput], [X+100, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	else: dibujarTexto(screen, 'N/A', [X+100, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	
	
	dibujarTexto(screen, 'Valor: ', [X+40, Y+35], Fuentes['Droid 20'], COLOR['Negro'])
	
	# Dibuja Los Botones Izquierda y Derecha Para Cambiar Valores.
	BtnIzq.resize(25,20); screen.blit(BtnIzq.image, (X+96, Y+38))
	BtnDer.resize(25,20); screen.blit(BtnDer.image, (X+146, Y+38))
	
	# Dibuja El Numero De Terreno Que se Le Sera Asignado.
	if Repetido: dibujarTexto(screen, str(List[LisyPosX]), [X+125, Y+35], Fuentes['Droid 20'], COLOR['Rojo'])
	else: dibujarTexto(screen, str(List[LisyPosX]), [X+125, Y+35], Fuentes['Droid 20'], COLOR['Negro'])

#===================================================================================================

def BotonesFlechas(X, Y, xr, yr, Lisy, LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6, LisyPos7, LisyPos8):
	
	# Cambia Los Valores Cuando Se Presiona Un Botón en Su Respectiva Posición.
	if Pagina1:
		
		# Miniatura Bloque Pared:
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos1 > 0 and LisyPos1 < len(Lisy): LisyPos1 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos1 >= 0 and LisyPos1 < len(Lisy)-1: LisyPos1 += 1

		# Miniatura Bloque Camino:
		Y += 70
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos2 > 0 and LisyPos2 < len(Lisy): LisyPos2 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos2 >= 0 and LisyPos2 < len(Lisy)-1: LisyPos2 += 1

		# Miniatua Bloque Bosque:
		Y += 70
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos3 > 0 and LisyPos3 < len(Lisy): LisyPos3 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos3 >= 0 and LisyPos3 < len(Lisy)-1: LisyPos3 += 1

		# Miniatua Bloque Lava:
		Y += 70
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos4 > 0 and LisyPos4 < len(Lisy): LisyPos4 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos4 >= 0 and LisyPos4 < len(Lisy)-1: LisyPos4 += 1

		# Miniatua Bloque Agua:
		Y += 70
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos5 > 0 and LisyPos5 < len(Lisy): LisyPos5 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos5 >= 0 and LisyPos5 < len(Lisy)-1: LisyPos5 += 1
	
	else:
		
		# Miniatua Bloque Arena:
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos6 > 0 and LisyPos6 < len(Lisy): LisyPos6 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos6 >= 0 and LisyPos6 < len(Lisy)-1: LisyPos6 += 1
		
		# Miniatua Bloque Montaña:
		Y += 70
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos7 > 0 and LisyPos7 < len(Lisy): LisyPos7 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos7 >= 0 and LisyPos7 < len(Lisy)-1: LisyPos7 += 1
		
		# Miniatua Bloque Nieve:
		Y += 70
		if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
			if LisyPos8 > 0 and LisyPos8 < len(Lisy): LisyPos8 -= 1
		elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
			if LisyPos8 >= 0 and LisyPos8 < len(Lisy)-1: LisyPos8 += 1
		
	return LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6, LisyPos7, LisyPos8

#===================================================================================================

def InputAdd(Add, C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8):
	
	if C1:
		if '.' in TI1:
			if len(TI1.split('.')[1]) == 2: TI1 = TI1[:-1]
			TI1 += Add
		else:
			if len(TI1.split('.')[0]) == 4: TI1 = TI1[:-1] + Add
			else:
				if Add != '0' and TI1 == '0': TI1 = TI1[:-1]
				if Add == '0' and TI1 == '0': pass
				else: TI1 += Add
	elif C2:
		if '.' in TI2:
			if len(TI2.split('.')[1]) == 2:  TI2 = TI2[:-1]
			TI2 += Add
		else:
			if len(TI2.split('.')[0]) == 4:  TI2 = TI2[:-1] + Add
			else:
				if Add != '0' and TI2 == '0': TI2 = TI2[:-1]
				if Add == '0' and TI2 == '0': pass
				else: TI2 += Add
	elif C3:
		if '.' in TI3:
			if len(TI3.split('.')[1]) == 2: TI3 = TI3[:-1]
			TI3 += Add
		else:
			if len(TI3.split('.')[0]) == 4:  TI3 = TI3[:-1] + Add
			else:
				if Add != '0' and TI3 == '0': TI3 = TI3[:-1]
				if Add == '0' and TI3 == '0': pass
				else: TI3 += Add
	elif C4:
		if '.' in TI4:
			if len(TI4.split('.')[1]) == 2: TI4 = TI4[:-1]
			TI4 += Add
		else:
			if len(TI4.split('.')[0]) == 4: TI4 = TI4[:-1] + Add
			else:
				if Add != '0' and TI4 == '0': TI4 = TI4[:-1]
				if Add == '0' and TI4 == '0': pass
				else: TI4 += Add
	elif C5:
		if '.' in TI5:
			if len(TI5.split('.')[1]) == 2: TI5 = TI5[:-1]
			TI5 += Add
		else:
			if len(TI5.split('.')[0]) == 4: TI5 = TI5[:-1] + Add
			else:
				if Add != '0' and TI5 == '0': TI5 = TI5[:-1]
				if Add == '0' and TI5 == '0': pass
				else: TI5 += Add
	elif C6:
		if '.' in TI6:
			if len(TI6.split('.')[1]) == 2: TI6 = TI6[:-1]
			TI6 += Add
		else:
			if len(TI6.split('.')[0]) == 4: TI6 = TI6[:-1] + Add
			else:
				if Add != '0' and TI6 == '0': TI6 = TI6[:-1]
				if Add == '0' and TI6 == '0': pass
				else: TI6 += Add
	elif C7:
		if '.' in TI7:
			if len(TI7.split('.')[1]) == 2: TI7 = TI7[:-1]
			TI7 += Add
		else:
			if len(TI7.split('.')[0]) == 4: TI7 = TI7[:-1] + Add
			else:
				if Add != '0' and TI7 == '0': TI7 = TI7[:-1]
				if Add == '0' and TI7 == '0': pass
				else: TI7 += Add
	elif C8:
		if '.' in TI8:
			if len(TI8.split('.')[1]) == 2: TI8 = TI8[:-1]
			TI8 += Add
		else:
			if len(TI8.split('.')[0]) == 4: TI8 = TI8[:-1] + Add
			else:
				if Add != '0' and TI8 == '0': TI8 = TI8[:-1]
				if Add == '0' and TI8 == '0': pass
				else: TI8 += Add
	
	return TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8

#===================================================================================================
#===================================== Declaraciones Globales ======================================
#===================================================================================================

# Constantes Globales: =================================================

COLOR  = {'Blanco':		(255, 255, 255),		'Negro':		(  0,   0,   0),
		  'Gris':		(189, 189, 189),		'Gris Claro':	(216, 216, 216),
		  'Rojo':		(255,   0,   0),		'Rojo Claro':	(255,  50,  50),
		  'Verde':		(  4, 180,   4),		'Verde Claro':	(  0, 255,   0),
		  'Azul':		( 20,  80, 240),		'Azul Claro':	( 40, 210, 250),
		  'Amarillo':	(255, 255,   0),		'Naranja':		(255, 120,   0),
		  'Morado':		( 76,  11,  95),		'Purpura':		( 56,  11,  97),
		  'Fondo':		( 24,  25,  30),		'Seleccion':	(220, 200,   0)
		 }	# Diccionario de Colores.

DIMENCIONES = (1120, 605)		# Tamaño de La Ventana, Ancho (1120) y Alto (600).
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']	# Letras Para La Matriz.

VALORES   = []		# Lista de Valores para Los Terrenos y Mostrar su Informacion.
SELECT    = []		# Lista de Seleccionados, Contendra: Posiciones Visitadas, Número de Visita.
Direcciones = [1,2,3,4]	# Lista de Orden de Expansión de Nodos.
NoRepetir = True
VISITA = 0
ListaHijos = []
TipoBusqueda = 2	# Variable Para Elegir El Tipo de Algoritmo de Busqueda a Utilizar: 0 = Normal (Manual), 1 = Backtracking, 2 = A* (A Estrella).


# Variables Globales: ==================================================

seleccion = None	# Lista con Las Posiciones, ejemplo [ 'A', 1 ].
PuntoInicio = None	# Posición de Inicio, ejemplo [ 'A', 1 ].
PuntoDestino = None	# Posición de Destino, ejemplo [ 'O', 15 ].

Error = False		# Marca Errores En Carga de Archivos y Otros.
Error2 = False		# Marca errores solamente en la sección de selección de bloques, si hay repetidos.
CadenaError = ''	# Marca Errores En Carga de Archivos y Otros. 
CadenaError2 = ''	# Marca errores solamente en la sección de selección de bloques, si hay repetidos.

Pagina1 = True			# Indica si la Pagina de Selección de Terrenos Es Alctualmente la primera.
Iniciar = False			# Indica si ya Inició el Juego.
SelectEstados = False	# Permite Saber Si Ya Se Permite Seleccionar Estado Inicial Y Final.
DibujarInfo = False		# Booleano que Indica si se debe o no Dibujar la Informacion en La Derecha con el Clic en un Terreno.
InfoSelTemp = []		# Lista que almacenara la Selección Temporal para poder mostrar la Información Constante.
Costos = {}				# Diccionario de los Costos de Cada Tipo de Terreno.
CostoTotal = 0			# Suma Costos en cada Movimiento.
Movimientos = 1
NombrePersonaje = []
DibujarInfoXY = False
NumPlayer = None				# Variable Que Almacena el Numero de Jugador (Num Player)

# Posiciones en La Lista (Lisy) con Los Números Ordenados Para Cada Tipo de Terreno.
# La Posición 0 equivale al valor -1 que Simboliza A Los Terrenos No Seleccionados Para El Mapa. 
Pared   = 0
Camino  = 0
Bosque  = 0
Lava    = 0
Agua    = 0
Arena   = 0
Montaña = 0
Nieve	= 0

Mask = []
Pila = []

#===================================================================================================
#============================================== Main ===============================================
#===================================================================================================

def main():
	
	global SELECT, Movimientos, DibujarInfo, Pagina1, SelectEstados, DibujarInfoXY
	global seleccion, PuntoInicio, PuntoDestino, Iniciar, Costos, CostoTotal
	global Error, Error2, CadenaError, CadenaError2, NombrePersonaje, NumPlayer
	global Bosque, Camino, Pared, Lava, Agua, Arena, Montaña, Nieve, Mask
	global Direcciones, NoRepetir, Pila, ListaHijos, TipoBusqueda
	
	XPOS = 1			# Variable con la Cantidad de columnas en la Matriz, solo la Inicializamos, para modificar poseteriormente.
	YPOS = 1			# Lo Mismo Con La Anterior pero con Columnas.
	POS  = (XPOS if XPOS > YPOS else YPOS)		# Obtenemos Cual de los 2 es Mayor, para Manipular mejor la Matriz más adelante.
	
	xD = 0
	DibujarInfoXY = False
	DibujarInfoX = 0
	DibujarInfoY = 0
	SelInfoTemp  = []
	PadreSeleccion = []
	
	Lisy = ['-1']		# Lista de Terrenos, -1 igual al Terreno Vacio
	LisyPos1 = 0		# Para Terreno Tipo Pared
	LisyPos2 = 0		# Para Terreno Tipo Camino
	LisyPos3 = 0		# Para Terreno Tipo Bosque
	LisyPos4 = 0		# Para Terreno Tipo Lava
	LisyPos5 = 0		# Para Terreno Tipo Agua
	LisyPos6 = 0		# Para Terreno Tipo Arena
	LisyPos7 = 0		# Para Terreno Tipo Montaña
	LisyPos8 = 0		# Para Terreno Tipo Nieve
	
	CargarMapa = None		# Variable Booleana Para Hacer Validaciones al Cargar Mapa.
	CargarPers = False		# Variable Booleana Para Hacer Validaciones al Cargar Un Personaje.
	FULL = False			# Variable Booleana Para Hacer Pantalla Completa.
	Cargar = False			# Variable Booleana Para Hacer Validaciones al Dibujar El Tablero.
	
	NumPlayer = None			# Numero de Personaje, Posicionamineto en la Lista de Personajes.
	seleccion = None			# Lista con Las Posiciones, ejemplo [ 'A', 1 ].
	PuntoInicio = None			# Posición de Inicio, ejemplo [ 'A', 1 ].
	SelTemp = ['P',16]			# Selección Temporal.
	
	pygame.init()				# Inicia El Juego.
	pygame.mixer.init()			# Inicializa el Mesclador.
	
	screen = pygame.display.set_mode(DIMENCIONES)	# Objeto Que Crea La Ventana.
	
	BGimg = load_image('img/fondo-negro.jpg')		# Carga el Fondo de la Ventana.
	
	Icono = pygame.image.load("img/Icon.png")
	pygame.display.set_icon(Icono)
	
	pygame.display.set_caption("Laberinto")			# Titulo de la Ventana del Juego.
	game_over = False								# Variable Que Permite indicar si se termino el juego o no.
	clock = pygame.time.Clock()						# Obtiener El Tiempo para pasar la cantidad de FPS más adelante.
	tamanio_fuente = 30				# Constante, para hacer manipulación del tamaño de algunas letras y en la matriz
									# para tener un margen correcto y otras cosas más.
	
	TextInput1 = ''		# Input Para El Costo en Terreno 1 (Pared).
	TextInput2 = ''		# Input Para El Costo en Terreno 2 (Camino).
	TextInput3 = ''		# Input Para El Costo en Terreno 3 (Bosque).
	TextInput4 = ''		# Input Para El Costo en Terreno 4 (Lava).
	TextInput5 = ''		# Input Para El Costo en Terreno 5 (Agua).
	TextInput6 = ''		# Input Para El Costo en Terreno 6 (Arena).
	TextInput7 = ''		# Input Para El Costo en Terreno 7 (Montaña).
	TextInput8 = ''		# Input Para El Costo en Terreno 8 (Nieve).
	
	# Incializamos El Diccionario de Costos Por Terreno.
	Costos = {
			  'Hombre':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Gato':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Lobo':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'CatBug':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Pez':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Caricatura':	[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Mujer':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Pizza':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Mono':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Pulpo':		[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Fantasma':	[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8],
			  'Peleador':	[TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8]
			 }
	
	Costo1 = False		# Para El Costo en Terreno 1 (Pared).
	Costo2 = False		# Para El Costo en Terreno 1 (Camino).
	Costo3 = False		# Para El Costo en Terreno 1 (Bosque).
	Costo4 = False		# Para El Costo en Terreno 1 (Lava).
	Costo5 = False		# Para El Costo en Terreno 1 (Agua).
	Costo6 = False		# Para El Costo en Terreno 1 (Arena).
	Costo7 = False		# Para El Costo en Terreno 1 (Montaña).
	Costo8 = False		# Para El Costo en Terreno 1 (Nieve).
	
	#===================================================================
	
	# Fuentes de Letra:
	Fuentes = {
			   'Alice 30':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 30),
			   'Wendy 30':pygame.font.Font("fuentes/Wendy.ttf", 	30),
			   'Wendy 25':pygame.font.Font("fuentes/Wendy.ttf", 	25),
			   'Droid 30':pygame.font.Font("fuentes/DroidSans.ttf", 30),
			   'Droid 25':pygame.font.Font("fuentes/DroidSans.ttf", 25),
			   'Droid 20':pygame.font.Font("fuentes/DroidSans.ttf", 20),
			   'Droid 18':pygame.font.Font("fuentes/DroidSans.ttf", 18),
			   'Droid 16':pygame.font.Font("fuentes/DroidSans.ttf", 16),
			   'Droid 15':pygame.font.Font("fuentes/DroidSans.ttf", 15),
			   'Droid 12':pygame.font.Font("fuentes/DroidSans.ttf", 12),
			   'Droid 10':pygame.font.Font("fuentes/DroidSans.ttf", 10),
			   'Droid 8': pygame.font.Font("fuentes/DroidSans.ttf", 8),
			   'Droid 7': pygame.font.Font("fuentes/DroidSans.ttf", 7),
			   'Droid 6': pygame.font.Font("fuentes/DroidSans.ttf", 6)
			  }
	
	#===================================================================
	
	puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
	
	# Objetos:
	
	#Objetos Para El Mapa:
	personaje = None		# Inicializamos la variable objeto para el futuro personaje a elegir.
	bloque1 = Bloque("img/Texturas/Pared.jpg")		# Objeto Pared.
	bloque3 = Bloque("img/Texturas/Camino.jpg")		# Objeto Camino.
	bloque4 = Bloque("img/Texturas/Bosque.jpg")		# Objeto Bosque.
	bloque5 = Bloque("img/Texturas/Lava.jpg")		# Objeto Lava.
	bloque6 = Bloque("img/Texturas/Agua.jpg")		# Objeto Agua.
	bloque7 = Bloque("img/Texturas/Arena.jpg")		# Objeto Arena.
	bloque8 = Bloque("img/Texturas/Montania.jpg")	# Objeto Montaña.
	bloque9 = Bloque("img/Texturas/Nieve.jpg")		# Objeto Nieve.
	
	# Miniaturas para elección de Terrenos para el Mapa:
	bloque11 = Bloque("img/Texturas/Pared.jpg")
	bloque13 = Bloque("img/Texturas/Camino.jpg")
	bloque14 = Bloque("img/Texturas/Bosque.jpg")
	bloque15 = Bloque("img/Texturas/Lava.jpg")
	bloque16 = Bloque("img/Texturas/Agua.jpg")
	bloque17 = Bloque("img/Texturas/Arena.jpg")
	bloque18 = Bloque("img/Texturas/Montania.jpg")
	bloque19 = Bloque("img/Texturas/Nieve.jpg")
	
	# Botón Cargar Mapa:
	boton1 = Boton("img/Botones/BotonRojo.png")
	boton2 = Boton("img/Botones/BotonNaranja.png")
	
	# Botón Comezar:
	botonPers1 = Boton("img/Botones/BotonAzul.png")
	botonPers2 = Boton("img/Botones/BotonPurpura.png")
	
	# Botón Reiniciar:
	btnReiniciar1 = Boton("img/Botones/BotonAzul.png")
	btnReiniciar2 = Boton("img/Botones/BotonPurpura.png")
	
	# Botón Seleccionar Personaje:
	btnSelect1 = Boton("img/Botones/BotonAzul.png")
	btnSelect2 = Boton("img/Botones/BotonPurpura.png")
	
	# Botones Con Flechas Izquierda y Derecha Para Elección de Terrenos.
	# flip() Invierte la Imágen en Espejo en el eje de las X.
	# flip(False, True) Invierte la Imágen en Espejo en el eje de las Y.
	# flip(True, True) Invierte la Imágen en Espejo en ambos ejes (X, Y).
	
	RutaBtn = "img/Botones/BotonIzq.png"			# Ruta del Botón a Cargar.
	BtnIzq1 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Pared.
	BtnDer1 = BotonDir(RutaBtn); BtnDer1.flip()		# Botón Derecha   Para Elección de Pared. ====
	BtnIzq2 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Camino.
	BtnDer2 = BotonDir(RutaBtn); BtnDer2.flip()		# Botón Derecha   Para Elección de Camino. ===
	BtnIzq3 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Bosque. 
	BtnDer3 = BotonDir(RutaBtn); BtnDer3.flip()		# Botón Derecha   Para Elección de Bosque. ===
	BtnIzq4 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Lava.
	BtnDer4 = BotonDir(RutaBtn); BtnDer4.flip()		# Botón Derecha   Para Elección de Lava. =====
	BtnIzq5 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Agua.
	BtnDer5 = BotonDir(RutaBtn); BtnDer5.flip()		# Botón Derecha   Para Elección de Agua. =====
	BtnIzq6 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Arena.
	BtnDer6 = BotonDir(RutaBtn); BtnDer6.flip()		# Botón Derecha   Para Elección de Arena. ====
	BtnIzq7 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Montaña.
	BtnDer7 = BotonDir(RutaBtn); BtnDer7.flip()		# Botón Derecha   Para Elección de Montaña. ==
	BtnIzq8 = BotonDir(RutaBtn)						# Botón Izquierda Para Elección de Nieve.
	BtnDer8 = BotonDir(RutaBtn); BtnDer8.flip()		# Botón Derecha   Para Elección de Nieve. ====
	
	BtnPagIzq = BotonDir(RutaBtn)						# Botón Derecho Para Cambiar de Página en la Selección de Terrenos.
	BtnPagDer = BotonDir(RutaBtn); BtnPagDer.flip()		# Botón Izquierdo Para Cambiar de Página en la Selección de Terrenos.
	
	BtnTipoBusquedaIzq = BotonDir(RutaBtn)								# Botón Derecho Para Cambiar la Selección del Tipo de Busqueda.
	BtnTipoBusquedaDer = BotonDir(RutaBtn); BtnTipoBusquedaDer.flip()	# Botón Izquierdo Para Cambiar la Selección del Tipo de Busqueda.
	
	seleccionPers1 = None		# Para Saber Si El Personaje 1 Fue Seleccionado.
	seleccionPers2 = None		# Para Saber Si El Personaje 2 Fue Seleccionado.
	seleccionPers3 = None		# Para Saber Si El Personaje 3 Fue Seleccionado.
	seleccionPers4 = None		# Para Saber Si El Personaje 4 Fue Seleccionado.
	seleccionPers5 = None		# Para Saber Si El Personaje 5 Fue Seleccionado.
	seleccionPers6 = None		# Para Saber Si El Personaje 6 Fue Seleccionado.
	seleccionPers7 = None		# Para Saber Si El Personaje 7 Fue Seleccionado.
	seleccionPers8 = None		# Para Saber Si El Personaje 8 Fue Seleccionado.
	seleccionPers9 = None		# Para Saber Si El Personaje 9 Fue Seleccionado.
	seleccionPers10 = None		# Para Saber Si El Personaje 10 Fue Seleccionado.
	seleccionPers11 = None		# Para Saber Si El Personaje 11 Fue Seleccionado.
	seleccionPers12 = None		# Para Saber Si El Personaje 12 Fue Seleccionado.
	
	Cuadro1  = Personaje("img/Personajes/Hombre.png")		# Miniatura Para Personaje Hombre.
	Cuadro2  = Personaje("img/Personajes/Gato.png")			# Miniatura Para Personaje Gato.
	Cuadro3  = Personaje("img/Personajes/Lobo.png")			# Miniatura Para Personaje Lobo.
	Cuadro4  = Personaje("img/Personajes/CatBug.png")		# Miniatura Para Personaje CatBug.
	Cuadro5  = Personaje("img/Personajes/Pez.png")			# Miniatura Para Personaje Pez.
	Cuadro6  = Personaje("img/Personajes/Caricatura.png")	# Miniatura Para Personaje Caricatura.
	Cuadro7  = Personaje("img/Personajes/Mujer.png")		# Miniatura Para Personaje Mujer.
	Cuadro8  = Personaje("img/Personajes/Pizza.png")		# Miniatura Para Personaje Pizza.
	Cuadro9  = Personaje("img/Personajes/Mono.jpg")			# Miniatura Para Personaje Mono.
	Cuadro10 = Personaje("img/Personajes/Pulpo.png")		# Miniatura Para Personaje Pulpo.
	Cuadro11 = Personaje("img/Personajes/Fantasma.png")		# Miniatura Para Personaje Fantasma.
	Cuadro12 = Personaje("img/Personajes/Peleador.gif")		# Miniatura Para Personaje Peleador.
	
	Cuadro5.flip()		# Acomodamos Al Personaje Mirando a Derecha.
	Cuadro5.setDireccion('R')
	Cuadro9.flip()		# Acomodamos Al Personaje Mirando a Derecha.
	Cuadro9.setDireccion('R')
	Cuadro12.flip()		# Acomodamos Al Personaje Mirando a Derecha.
	Cuadro12.setDireccion('R')
	
	SelectPerson = False
	NombrePersonaje = ['Hombre','Gato','Lobo','CatBug','Pez','Caricatura','Mujer','Pizza','Mono','Pulpo','Fantasma','Peleador']	# Lista de Personajes.
	
	# Rutas de Imagenes de los Personajes:
	RutaPersonaje = {
					'Hombre':		"img/Personajes/Hombre.png",
					'Gato':			"img/Personajes/Gato.png",
					'Lobo':			"img/Personajes/Lobo.png",
					'CatBug':		"img/Personajes/CatBug.png",
					'Pez':			"img/Personajes/Pez.png",
					'Caricatura':	"img/Personajes/Caricatura.png",
					'Mujer':		"img/Personajes/Mujer.png",
					'Pizza':		"img/Personajes/Pizza.png",
					'Mono':			"img/Personajes/Mono.jpg",
					'Pulpo':		"img/Personajes/Pulpo.png",
					'Fantasma':		"img/Personajes/Fantasma.png",
					'Peleador':		"img/Personajes/Peleador.gif"
					}
	
	# Diccionario Con Objetos Para Mapa:
	Objetos = {'Personaje':personaje, 'Pared':bloque1, 'Camino':bloque3, 'Bosque':bloque4,
			   'Lava':bloque5, 'Agua':bloque6, 'Arena':bloque7, 'Montaña':bloque8, 'Nieve':bloque9}
	
	# Diccionario Con Objetos Para Miniaturas:
	Objetos10 = {'Personaje':personaje, 'Pared':bloque11, 'Camino':bloque13, 'Bosque':bloque14, 'Lava':bloque15,
				 'Agua':bloque16, 'Arena':bloque17, 'Montaña':bloque18, 'Nieve':bloque19}
	
	# Variables que marcan si hay errores al seleccionar Terrenos, una variable para cada uno.
	Er1 = False
	Er2 = False
	Er3 = False
	Er4 = False
	Er5 = False
	Er6 = False
	Er7 = False
	
	#===================================================================
	
	# Booleanos Para Saber Si Los Botones Fueron Presionados:
	Btn1Pressed = False
	Btn2Pressed = False
	Btn3Pressed = False
	Btn4Pressed = False
	
	#===================================================================
	
	# Sonidos:
	
	Clic1 = pygame.mixer.Sound("Sonidos/Kwahmah-Click.wav")		# Sonido Clic Izquierdo.
	Clic2 = pygame.mixer.Sound("Sonidos/Clic15.wav")			# Sonido Clic Derecho.
	ClicSet = pygame.mixer.Sound("Sonidos/Clic3.wav")			# Sonido Al Escribir Un Caracter En La Sección Se Costos.
	ClicUndo = pygame.mixer.Sound("Sonidos/Clic14.wav")			# Sonido Al Borrar Un Caracter De La Sección Se Costos.
	
	Sucess = pygame.mixer.Sound("Sonidos/Level Up.wav")			# Sonido Al Cargar Un Mapa Exitosamente.
	Victoria = pygame.mixer.Sound("Sonidos/Victoria.wav")		# Sonido De Victoria Cuando El Personaje Llega Al Estado Final.
	
	Sucess.set_volume(.3)			# Reduce Su Volumen al 30%.
	Victoria.set_volume(.3)			# Reduce Su Volumen al 30%.
	
	# Lista de Objetos de Sonidos Para El Fondo Del Juego al Iniciar.
	MusicFondos = [
					pygame.mixer.Sound("Sonidos/Memz Pretty Pluck Sound.wav"),
					pygame.mixer.Sound("Sonidos/Setuniman - Little Pleasures.wav"),
					pygame.mixer.Sound("Sonidos/Errinerung - Debussy.wav"),
					# ~ pygame.mixer.Sound("Sonidos/Tim-Kahn - Cedellia.wav"),
					pygame.mixer.Sound("Sonidos/Tim-Kahn - Sigj.wav")
				  ]
	
	MusicFondo1 = pygame.mixer.Sound("Sonidos/Memz Guitar.wav")				# Musica de Fondo Para El Menu.
	MusicFondo2 = MusicFondos[random.randint(0,len(MusicFondos)-1)]			# Musica de Fondo Para El Mapa (Al Iniciar la Partida).	Se Obtiene uno al Azar de la lista.			
	
	#===================================================================
	
	Victory = False					# Si Es True Muestra el Sonido de Victoria (Cuando Se Llega al Punto de Final.
	ArbolRaiz = None				# Variable Para Almacenar el Objeto Raiz del Arbol.
	
	BtnMutePressed = False			# Botón Para Poner Mute en False Por Defecto.
	BtnMaskPressed = True			# Botón Para Poner Enmascaramiento en True Por Defecto.
	BtnMostrarArbol = False			# Botón Para Mostrar El Árbol Generado en False Por Defecto.
	BtnOrdenExpansion = False		# Botón Para Mostrar La Selección del Orden De Expansión de Nodos.
	BtnRepetirNodos = False			# Botón Para Selección de Repetición o No de Nodos.
	BtnTipoBusqueda = 'A Estrella'		# Botón Para Selección del Tipo de Busqueda {Manual, Backtracking, A* (A Estrella)}.
	
	ContDir = 0
	
	# Botón Para Mute y Enmascaramiento True/False, On/Off:
	btnON  = Boton("img/Botones/BtnOn.png")			# Objeto Botón ON
	btnOFF = Boton("img/Botones/BtnOff.png")		# Objeto Botón OFF
	
	# Objetos Flecha.
	FlechaIzq = Flecha("img/Botones/Flecha.png")
	FlechaAba = Flecha("img/Botones/Flecha.png");	FlechaAba.rotate(90)
	FlechaDer = Flecha("img/Botones/Flecha.png");	FlechaDer.rotate(180)
	FlechaArr = Flecha("img/Botones/Flecha.png");	FlechaArr.rotate(270)
	
	FlechaIzq.resize(20,20)
	FlechaAba.resize(20,20)
	FlechaDer.resize(20,20)
	FlechaArr.resize(20,20)
	
	MoveX = 0
	MoveY = 0
	XX1 = 0
	YY1 = 0
	
	ListaBT = []
	ContFPS = 0
	
	#===================================================================
	
	MusicFondo1.play(-1)			# Se Ejecuta La Música de Fondo Para el Menu. (El -1 indica que se repita de forma en Búcle).
	
	# ~ pygame.mixer.music.play(-1)
	
	#===================================================================
	
	# Inicio Del Juego:
	while game_over is False:
		
		#=====================================================================================================
		#=====================================================================================================
		#=====================================================================================================
		
		# Chequeo Constante de Eventos del Teclado:
		events = pygame.event.get()
		
		for evento in events:
			
			if evento.type == pygame.QUIT: game_over = True		# Si Se Presiona El Botón Cerrar, Cerrara El Juego.
			
			elif evento.type == pygame.KEYDOWN:		# Manipulación del Teclado.
				
				# Si Ya Fue Cargado El Tablero, Se Presionó El Botón 'Comenzar' y El Estado Inicial y Final Son Distintos, Podra Moverse El Personaje.
				if Cargar and Iniciar and seleccion != PuntoDestino and not BtnMostrarArbol:
					
					if TipoBusqueda == 0:
						
						if   evento.key == pygame.K_LEFT  or evento.key == pygame.K_a:	seleccion = obtenerPosicion(XPOS, YPOS, 'L', seleccion, personaje, ArbolRaiz)	# Tecla Izquierda. Mueve Personaje.
						elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:	seleccion = obtenerPosicion(XPOS, YPOS, 'R', seleccion, personaje, ArbolRaiz)	# Tecla Derecha. Mueve Personaje.
						elif evento.key == pygame.K_UP    or evento.key == pygame.K_w:	seleccion = obtenerPosicion(XPOS, YPOS, 'U', seleccion, personaje, ArbolRaiz)	# Tecla Arriba. Mueve Personaje.
						elif evento.key == pygame.K_DOWN  or evento.key == pygame.K_s:	seleccion = obtenerPosicion(XPOS, YPOS, 'D', seleccion, personaje, ArbolRaiz)	# Tecla Abajo. Mueve Personaje.
						
						# ~ Arbol.ImprimirArbol(ArbolRaiz)		# Imprime El Arbol Con Estructura de Carpetas en La Ventana de Comandos
						
					elif TipoBusqueda == 2:
						
						seleccion = AEstrella(XPOS, YPOS, seleccion, ArbolRaiz)
						
				if BtnMostrarArbol:
					
					if   evento.key == pygame.K_LEFT  or evento.key == pygame.K_a:	MoveX += 15
					elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:	MoveX -= 15
					elif evento.key == pygame.K_UP    or evento.key == pygame.K_w:	MoveY += 15
					elif evento.key == pygame.K_DOWN  or evento.key == pygame.K_s:	MoveY -= 15
					
				if evento.key == pygame.K_ESCAPE: game_over = True		# Tecla ESC Cierra el Juego.
				
				#=======================================================
				
				if NumPlayer != None:
					
					TextInput1 = Costos[NombrePersonaje[NumPlayer]][0]
					TextInput2 = Costos[NombrePersonaje[NumPlayer]][1]
					TextInput3 = Costos[NombrePersonaje[NumPlayer]][2]
					TextInput4 = Costos[NombrePersonaje[NumPlayer]][3]
					TextInput5 = Costos[NombrePersonaje[NumPlayer]][4]
					TextInput6 = Costos[NombrePersonaje[NumPlayer]][5]
					TextInput7 = Costos[NombrePersonaje[NumPlayer]][6]
					TextInput8 = Costos[NombrePersonaje[NumPlayer]][7]
				
				if evento.key == pygame.K_BACKSPACE or evento.key == pygame.K_DELETE:
					
					ClicUndo.play()
					
					if   Costo1: TextInput1 = TextInput1[:-1]
					elif Costo2: TextInput2 = TextInput2[:-1]
					elif Costo3: TextInput3 = TextInput3[:-1]
					elif Costo4: TextInput4 = TextInput4[:-1]
					elif Costo5: TextInput5 = TextInput5[:-1]
					elif Costo6: TextInput6 = TextInput6[:-1]
					elif Costo7: TextInput7 = TextInput7[:-1]
					elif Costo8: TextInput8 = TextInput8[:-1]
					
				elif evento.key == pygame.K_PERIOD or evento.key == pygame.K_KP_PERIOD:
					
					ClicSet.play()
					
					if Costo1:
						if TextInput1 == '': TextInput1 += '0'
						if not '.' in TextInput1: TextInput1 += '.'
					elif Costo2:
						if TextInput2 == '': TextInput2 += '0'
						if not '.' in TextInput2: TextInput2 += '.'
					elif Costo3:
						if TextInput3 == '': TextInput3 += '0'
						if not '.' in TextInput3: TextInput3 += '.'
					elif Costo4:
						if TextInput4 == '': TextInput4 += '0'
						if not '.' in TextInput4: TextInput4 += '.'
					elif Costo5:
						if TextInput5 == '': TextInput5 += '0'
						if not '.' in TextInput5: TextInput5 += '.'
					elif Costo6:
						if TextInput6 == '': TextInput6 += '0'
						if not '.' in TextInput6: TextInput6 += '.'
					elif Costo7:
						if TextInput7 == '': TextInput7 += '0'
						if not '.' in TextInput7: TextInput7 += '.'
					elif Costo8:
						if TextInput8 == '': TextInput8 += '0'
						if not '.' in TextInput8: TextInput8 += '.'
				
				#=============================================================================================================================================
				# Reducimos el Nombre de las Variables Por Comodidad xD
				TI1, TI2, TI3, TI4 = TextInput1, TextInput2, TextInput3, TextInput4
				TI5, TI6, TI7, TI8 = TextInput5, TextInput6, TextInput7, TextInput8
				C1, C2, C3, C4 = Costo1, Costo2, Costo3, Costo4 
				C5, C6, C7, C8 = Costo5, Costo6, Costo7, Costo8 
				
				# Se Agrega a la Cadena Correspondiente del TextInput Seleccionado, el Número Presionado.
				if   evento.key == pygame.K_0 or evento.key == pygame.K_KP0: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('0', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_1 or evento.key == pygame.K_KP1: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('1', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_2 or evento.key == pygame.K_KP2: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('2', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_3 or evento.key == pygame.K_KP3: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('3', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_4 or evento.key == pygame.K_KP4: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('4', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_5 or evento.key == pygame.K_KP5: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('5', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_6 or evento.key == pygame.K_KP6: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('6', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_7 or evento.key == pygame.K_KP7: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('7', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_8 or evento.key == pygame.K_KP8: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('8', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				elif evento.key == pygame.K_9 or evento.key == pygame.K_KP9: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('9', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8); ClicSet.play()
				
				# Pasamos El Valor Correspondiente A Su Variable Oroginal 
				TextInput1, TextInput2, TextInput3, TextInput4 = TI1, TI2, TI3, TI4
				TextInput5, TextInput6, TextInput7, TextInput8 = TI5, TI6, TI7, TI8
				
				# Actualizamos los Datos de los Costos.
				if NumPlayer != None:
					Costos[NombrePersonaje[NumPlayer]][0] = TextInput1
					Costos[NombrePersonaje[NumPlayer]][1] = TextInput2
					Costos[NombrePersonaje[NumPlayer]][2] = TextInput3
					Costos[NombrePersonaje[NumPlayer]][3] = TextInput4
					Costos[NombrePersonaje[NumPlayer]][4] = TextInput5
					Costos[NombrePersonaje[NumPlayer]][5] = TextInput6
					Costos[NombrePersonaje[NumPlayer]][6] = TextInput7
					Costos[NombrePersonaje[NumPlayer]][7] = TextInput8
				
				#=============================================================================================================================================
				
				#~ elif evento.key == pygame.K_f:		# Tecla F pondra Pantalla Completa o Normal.
					
					#~ if FULL == False:	
						#~ screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
						#~ FULL = True
					#~ else:
						#~ screen = pygame.display.set_mode(DIMENCIONES)
						#~ FULL = False
				
				if evento.key == pygame.K_c:	# Presiona Botón 1 (Cargar Mapa).
					
					Clic1.play()
					
					Btn1Pressed = True
					CargarMapa = True
					Error2 = False
					CadenaError2 = ''
					
				if not BtnMostrarArbol:
					
					if Cargar: 			# Si se cargo ya el Mapa.
						
						if evento.key == pygame.K_RETURN:	# Presiona Botón 2 (Comenzar).
							if not Iniciar:
								
								Clic1.play()
								Btn2Pressed = True
							
						if evento.key == pygame.K_r:	# Presiona Botón 3 (Reiniciar).
							if Iniciar:
								
								Clic1.play()
								Btn3Pressed = True
							
						if evento.key == pygame.K_p:	# Presiona Botón 4 (Seleccionar Personaje).
							if Iniciar:
								
								Clic1.play()
								Btn4Pressed = True
							
						if evento.key == pygame.K_LEFT:		# Presiona Botón de Página Anterior (En Selección de Terrenos).
							if not Iniciar and not BtnMostrarArbol:
								
								Clic1.play()
								Pagina1 = True
							
						if evento.key == pygame.K_RIGHT:	# Presiona Botón de Página Siguiente (En Selección de Terrenos).
							if not Iniciar and not BtnMostrarArbol:
								
								Clic1.play()
								Pagina1 = False
							
			elif evento.type == pygame.KEYUP:
				
				if BtnMostrarArbol:
					
					if   evento.key == pygame.K_LEFT  or evento.key == pygame.K_a:	MoveX = 0
					elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:	MoveX = 0
					elif evento.key == pygame.K_UP    or evento.key == pygame.K_w:	MoveY = 0
					elif evento.key == pygame.K_DOWN  or evento.key == pygame.K_s:	MoveY = 0
							
				if evento.key == pygame.K_m:
					
					if BtnMutePressed:
						Clic2.play()
						BtnMutePressed = False
					else:
						Clic1.play()
						BtnMutePressed = True
				
				if evento.key == pygame.K_o:
					
					if BtnMaskPressed:
						Clic2.play()
						BtnMaskPressed = False
					else:
						Clic1.play()
						BtnMaskPressed = True
				
				if evento.key == pygame.K_v:
					
					if Iniciar:
						
						if BtnMostrarArbol:
							Clic2.play()
							BtnMostrarArbol = False
						else:
							Clic1.play()
							BtnMostrarArbol = True
							XX1 = 0
							YY1 = 0
				
				if not BtnMostrarArbol:
					
					if Cargar and not Iniciar:
						
						if evento.key == pygame.K_e:
							
							if BtnOrdenExpansion:
								Clic2.play()
								BtnOrdenExpansion = False
							else:
								Clic1.play()
								BtnOrdenExpansion = True
					
					if evento.key == pygame.K_c:
						
						xMatrixy, xLisy, xXPOS, xYPOS, xPOS = TODOArchivo()		# Obtenemos Valores desde la Función Temporalmente.
						
						if Error:		# Si Hubo Error.
						
							Error2 = False
						
						if xMatrixy == None:	# Si los Valores Se Encuentran En Null (None aqui en python) significa que hubo un error.
							
							if Cargar == False: pass		# Si el Valor era False se mantiene.
							else: Cargar = True				# Si el Valor Era None cambia a True.
							CargarMapa = False				# Se Cancela el Cargar el Mapa.
						
						else:	# Si la Matriz tiene informacion, Todo Estuvo Correcto y Validado.
							
							Sucess.play()
							
							MusicFondo1.stop()
							MusicFondo1.play(-1)
							MusicFondo2.stop()
							
							SELECT = []			 	# Se Reinicia La Variable Global SELECT, que guarda el Recorrido para imprimirlo en la Matriz. 
							SelectEstados = False	# Permite Saber Si se Permite Selecciona el Estado Inicial y Final.
							Pagina1 = True		 	# Se Vuelve a Posicionar la Página 1 en la Seleccion de Terrenos para el Mapa.
							DibujarInfo = False  	# Al Cargar Un Nuevo Mapa, Se Deja de Mostrar La Información de Seleccion.
							Iniciar = False		 	# Aun no se permite Iniciar La Partida.
							Cargar = True		 	# Se Dibuja El Mapa.
							SelectPerson = True		# Permite Seleccionar Algun Personaje.
							
							# Se Crean Nuevos Objetos Bloque para el nuevo Mapa.
							bloque1 = Bloque("img/Texturas/Pared.jpg")		# Objeto Pared.
							bloque3 = Bloque("img/Texturas/Camino.jpg")		# Objeto Camino.
							bloque4 = Bloque("img/Texturas/Bosque.jpg")		# Objeto Bosque.
							bloque5 = Bloque("img/Texturas/Lava.jpg")		# Objeto Lava.
							bloque6 = Bloque("img/Texturas/Agua.jpg")		# Objeto Agua.
							bloque7 = Bloque("img/Texturas/Arena.jpg")		# Objeto Arena.
							bloque8 = Bloque("img/Texturas/Montania.jpg")	# Objeto Montaña.
							bloque9 = Bloque("img/Texturas/Nieve.jpg")		# Objeto Nieve.
							
							# Se Pasan los valores Temporales a los Originales.
							Matrixy = xMatrixy
							Lisy = ['-1']				# Se Reinicia la Lista con el Primer Elemento, el -1 para la Selección de Terrenos.
							Lisy = Lisy + xLisy			# Se le añaden todos los Valores.
							
							# Se Reinician Las Variables Globales (Pared, Camino, Bosque, Lava, Agua, Arena, Montaña, Nieve) en 0.
							# Se Reinician Las Variables De Posición Para la Selección de Terrenos en 0.
							Pared   = LisyPos1 = 0
							Camino  = LisyPos2 = 0
							Bosque  = LisyPos3 = 0
							Lava    = LisyPos4 = 0
							Agua    = LisyPos5 = 0
							Arena   = LisyPos6 = 0
							Montaña = LisyPos7 = 0
							Nieve	= LisyPos8 = 0
							
							# Obtenemos El Ancho y Alto del Mapa, Para Cargar La Matriz Correctamente.
							XPOS = xXPOS		# Valor de las Letras.
							YPOS = xYPOS		# Valor de las Numeros.
							POS = xPOS			# Obtenemos Cual es el Mas grande de Los 2.
							
							Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia el Enmascaramiento del Mapa.
							
							puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)	# Se Indica El Punto de Inicio Para Dibujar La Matriz.
							
							# Se Reinicia el Diccionario Objetos con los Nuevos Objetos Generados.
							Objetos = {'Pared':bloque1,	'Camino':bloque3,	'Bosque': bloque4,	'Lava': bloque5,
									   'Agua': bloque6,	'Arena': bloque7,	'Montaña':bloque8,	'Nieve':bloque9}
							
							Movimientos  = 0
							CostoTotal	 = 0
							PuntoInicio	 = None		# Se Inicializa la Variable Global PuntoInicio en None.
							PuntoDestino = None		# Se Inicializa la Variable Global PuntoDestino en None.
							NumPlayer	 = None		# Se Inicializa la Variable personaje en None.
							CargarMapa	 = False	# Indíca que El Botón Cargar Mapa Dejo de ser Apretado.
							Error		 = False	# Indíca Que No Hay Error.
					
					if Cargar: 			# Si se cargo ya el Mapa.
						
						if evento.key == pygame.K_RETURN:
							
							if Btn2Pressed and not Error2:		# Si el Botón 2 (Comenzar) Fue Presionado.
								
								if NumPlayer == None:		# Si el Botón 2 Fue Presionado Pero No se ha seleccionado Personaje Marcara Error.
									
									Error = True
									CadenaError = 'Selecciona Un Personaje.'
									Iniciar = False
								
								elif PuntoInicio == None:
									
									Error = True
									CadenaError = 'Selecciona un Estado Inicial.'
								  
								elif PuntoDestino == None:
									
									Error = True
									CadenaError = 'Selecciona un Estado Final.'
								  
								else:			# Si Se Selecciono Un Personaje, Se Iniciará.
									
									Iniciar = True	# Inicia El Juego.
									Victory = True
									
									MusicFondo2.stop()
									MusicFondo2 = MusicFondos[random.randint(0,len(MusicFondos)-1)]
									MusicFondo1.stop()
									MusicFondo2.play(-1)
									
									seleccion = PuntoInicio
									
									personaje = Personaje(RutaPersonaje[NombrePersonaje[NumPlayer]]) # Se Crea el Objeto Personaje de la clase (Personaje),
																							  # Pasandole La Ruta de la Imagen Que se encuentra en el Diccionario (RutaPersonaje),
																							  # Que corresponda al Nombre de Personaje de la lista (NombrePersonaje)
																							  # Que este en la posición del Numero de Personaje Elegido (NumPlayer)
									
									if NumPlayer == 4 or NumPlayer == 8 or NumPlayer == 11:	
										
										personaje.flip()				# Acomodamos Al Personaje Mirando a Derecha.
										personaje.setDireccion('R')
										
									Objetos['Personaje'] = personaje		# Se Guarda el Objeto Personaje en el Diccionario.
									SelectPerson = False					# Ya No Permite Seleccionar otro Personaje hasta Presionar el Botón 4 (Seleccionar Personaje)
									
									for val in VALORES:
										if val[0] == PuntoInicio: CostoTotal += float(val[3])
											
									Movimientos += 1
									SELECT.append((seleccion, [Movimientos]))
									
									if TipoBusqueda == 0:
										
										ArbolRaiz = Arbol.Raiz(seleccion)
										PosLetra = LETRAS.index(seleccion[0])
										x, y = PosLetra, seleccion[1]
										AgregarAlArbol(ArbolRaiz, 'N/A', seleccion, x, y, YPOS, XPOS)
										# ~ Arbol.ImprimirArbol(ArbolRaiz)
										
									if TipoBusqueda == 1:
										
										#===============================================
										PadreSeleccion = seleccion
										ListaBT = []
										ListaHijos = []
										Pila = [(PuntoInicio, [])]
										ArbolRaiz = Arbol.Raiz(seleccion)
										
										#================================================================================
										XTemp = LETRAS.index(seleccion[0])
										YTemp = seleccion[1]
										
										UpTemp    = [LETRAS[XTemp], YTemp-1]
										RightTemp = [LETRAS[XTemp+1], YTemp]
										DownTemp  = [LETRAS[XTemp], YTemp+1]
										LeftTemp  = [LETRAS[XTemp-1], YTemp]
										
										ListaTemp = [UpTemp, RightTemp, DownTemp, LeftTemp]
										
										# Se Le agrega a lista de Hijos sus Hijos (Solo las Coordenadas).
										for x in VALORES:
											if x[0] == ListaTemp[Direcciones.index(1)] and x[3] != '':
												Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(1)]); break
										for x in VALORES:
											if x[0] == ListaTemp[Direcciones.index(2)] and x[3] != '':
												Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(2)]); break
										for x in VALORES:
											if x[0] == ListaTemp[Direcciones.index(3)] and x[3] != '':
												Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(3)]); break
										for x in VALORES:
											if x[0] == ListaTemp[Direcciones.index(4)] and x[3] != '':
												Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(4)]); break
										
										Arbol.AgregarIniFin(ArbolRaiz, seleccion, True)				# Se Indica que es el Nodo Inicial.
										Arbol.AgregarEstado(ArbolRaiz, seleccion, 'Cerrado')		# Si el Nodo es Visitado, Es Cerrado.
										Arbol.AgregarPadre(ArbolRaiz, seleccion, 'N/A')				# Se le agrega al Nodo Actual cual es su Padre.
										Arbol.AgregarOrden(ArbolRaiz, seleccion, Movimientos)		# Se Agrega La Lista Con El Orden De Visitas.
										#================================================================================
										
										seleccion = Backtracking(XPOS, YPOS, seleccion, ArbolRaiz, 'N/A')
										# ~ Arbol.ImprimirArbol(ArbolRaiz)
										#===============================================
									
							elif Btn2Pressed and Error2:		# Si el Botón 2 (Comenzar) Fue Presionado y Ocurrio un Error.
								
								CadenaError2 = 'Bloques Aún No Asignados.'
								
							
						if evento.key == pygame.K_r:
							
							if Btn3Pressed: # Si Se Presionó el Botón 3 (Reiniciar).
								
								MusicFondo2.stop()
								MusicFondo2 = MusicFondos[random.randint(0,len(MusicFondos)-1)]
								MusicFondo2.play(-1)
								
								Victory = True
								Error = False
								CadenaError = ''
								
								Movimientos = 1
								CostoTotal = 0
								
								seleccion = PuntoInicio
								
								SELECT = []
								SELECT.append((seleccion, [Movimientos]))
								
								Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia el Enmascaramiento del Mapa.
								
								for val in VALORES:
									if val[0] == PuntoInicio: CostoTotal += float(val[3])
								
								if TipoBusqueda == 0:
									
									ArbolRaiz = Arbol.Raiz(seleccion)
									PosLetra = LETRAS.index(seleccion[0])
									x, y = PosLetra, seleccion[1]
									AgregarAlArbol(ArbolRaiz, 'N/A', seleccion, x, y, YPOS, XPOS)
									# ~ Arbol.ImprimirArbol(ArbolRaiz)
									
								if TipoBusqueda == 1:
									
									#===============================================
									PadreSeleccion = seleccion
									ListaBT = []
									ListaHijos = []
									Pila = [(PuntoInicio, [])]
									ArbolRaiz = Arbol.Raiz(seleccion)
									
									#================================================================================
									XTemp = LETRAS.index(seleccion[0])
									YTemp = seleccion[1]
									
									UpTemp    = [LETRAS[XTemp], YTemp-1]
									RightTemp = [LETRAS[XTemp+1], YTemp]
									DownTemp  = [LETRAS[XTemp], YTemp+1]
									LeftTemp  = [LETRAS[XTemp-1], YTemp]
									
									ListaTemp = [UpTemp, RightTemp, DownTemp, LeftTemp]
									
									# Se Le agrega a lista de Hijos sus Hijos (Solo las Coordenadas).
									for x in VALORES:
										if x[0] == ListaTemp[Direcciones.index(1)] and x[3] != '':
											Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(1)]); break
									for x in VALORES:
										if x[0] == ListaTemp[Direcciones.index(2)] and x[3] != '':
											Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(2)]); break
									for x in VALORES:
										if x[0] == ListaTemp[Direcciones.index(3)] and x[3] != '':
											Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(3)]); break
									for x in VALORES:
										if x[0] == ListaTemp[Direcciones.index(4)] and x[3] != '':
											Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(4)]); break
									
									Arbol.AgregarIniFin(ArbolRaiz, seleccion, True)				# Se Indica que es el Nodo Inicial.
									Arbol.AgregarEstado(ArbolRaiz, seleccion, 'Cerrado')		# Si el Nodo es Visitado, Es Cerrado.
									Arbol.AgregarPadre(ArbolRaiz, seleccion, 'N/A')				# Se le agrega al Nodo Actual cual es su Padre.
									Arbol.AgregarOrden(ArbolRaiz, seleccion, Movimientos)		# Se Agrega La Lista Con El Orden De Visitas.
									#================================================================================
									
									seleccion = Backtracking(XPOS, YPOS, seleccion, ArbolRaiz, 'N/A')
									# ~ Arbol.ImprimirArbol(ArbolRaiz)
									#===============================================
								
						if evento.key == pygame.K_p:
							
							if Btn4Pressed: # Si Se Presionó el Botón 3 (Seleccionar Personaje).
								
								MusicFondo1.stop()
								MusicFondo1.play(-1)
								MusicFondo2.stop()
								
								Error = False
								CadenaError = ''
								
								Movimientos = 0
								CostoTotal = 0
								
								SELECT = []
								Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia el Enmascaramiento del Mapa.
								
								DibujarInfo = False
								SelectPerson = True
								Iniciar = False
								Cargar = True
								
				
				Btn1Pressed = False			# Indica Que El Botón 'Cargar Mapa' Ya No esta Siendo Presionado. 
				Btn2Pressed = False			# Indica Que El Botón 'Comenzar' Ya No esta Siendo Presionado. 
				Btn3Pressed = False			# Indica Que El Botón 'Reiniciar' Ya No esta Siendo Presionado. 
				Btn4Pressed = False			# Indica Que El Botón 'Seleccionar Personaje' Ya No esta Siendo Presionado. 
				SelTemp = ['P',16]				# La Selección Temporal se manda a un valor jamas cargado en el mapa. (16, 16)
												# Para que deje de mostrarse la selección con el Puntero.
			
			#~ elif evento.type == pygame.JOYBUTTONDOWN
			
			elif evento.type == pygame.MOUSEBUTTONDOWN: #============================== Al Mantener Presionado Cualquier Botón del Mouse. ==============================
				
				# Si se Presiono el Clic Derecho del Mouse (Botón 3) y La Variable Global 'DibujarInfo' esta en True entonces se cambia a false.
				# Dejara de mostrar la Información del Bloque Seleccionado con el Mouse.
				if evento.button == 3:
					
					Clic2.play()		# Reproduce Sonido Del Clic Derecho.
					
					if Cargar and Iniciar:
						if DibujarInfo: DibujarInfo = False
					
					if Cargar and not Iniciar and SelectEstados:
						
						xD = 0
						
						DibujarInfoXY = True
						Pos = pygame.mouse.get_pos()					# Obtiene una Tupla con los Valores X y Y del Mouse, en Pixeles.
						DibujarInfoX, DibujarInfoY = Pos[0], Pos[1]		# Posición X y Y del Mouse por separado, Coordenadas por Pixeles.
						
						SelInfoTemp = obtenerPosicionClic(XPOS, YPOS, Pos, dimension, puntoInicio, seleccion)		# Función Que crea una selección Temporal
						
						SelTemp = seleccion								# Selección temporal, para mostrar el cuadro seleccionado con el mouse.
						SelTemp = obtenerPosicionClic(XPOS, YPOS, Pos, dimension, puntoInicio, SelTemp)		# Función Que crea una selección Temporal
						
				else:
					
					Clic1.play()		# Reproduce Sonido Del Clic Izquierdo.
					
					# Si se Presionó cualquier otro Botón del Mouse...
					pos = pygame.mouse.get_pos()	# Obtiene una Tupla con los Valores X y Y del Mouse, en Pixeles.
					
					xr, yr = pos[0], pos[1]		# Posición X y Y del Mouse por separado, Coordenadas por Pixeles.
					
					if Iniciar:
						
						if BtnMostrarArbol:
							MoveX, MoveY = 0, 0
							if (xr >= 1055) and (xr <= 1095) and (yr >= 582) and (yr <= 602): BtnMostrarArbol = False 
						else:
							if (xr >= 1050) and (xr <= 1100) and (yr >= 582) and (yr <= 602): BtnMostrarArbol = True
					
					if BtnMutePressed:
						if (xr >= 65) and (xr <= 105) and (yr >= 582) and (yr <= 602): BtnMutePressed = False
					else:
						if (xr >= 60) and (xr <= 110) and (yr >= 582) and (yr <= 602): BtnMutePressed = True
					
					if BtnMaskPressed:
						if (xr >= 205) and (xr <= 245) and (yr >= 582) and (yr <= 602): BtnMaskPressed = False
					else:
						if (xr >= 200) and (xr <= 250) and (yr >= 582) and (yr <= 602): BtnMaskPressed = True
					
					if not BtnMostrarArbol:
						
						# Cooredenadas Botón 1 (Cargar Mapa):
						if (xr >= 927) and (xr <= 1077) and (yr >= 24) and (yr <= 56):
							
							Btn1Pressed = True
							CargarMapa = True
							Error2 = False
							CadenaError2 = ''
						
						if Cargar: 			# Si se cargo ya el Mapa.
							
							pygame.mouse.set_visible(False)	# Hacemos Invisible Temporalmente el Cursor del Mouse.
							
							if not Iniciar:
								
								if BtnOrdenExpansion:
									
									if (xr >= 485) and (xr <= 525) and (yr >= 582) and (yr <= 602): BtnOrdenExpansion = False
									
									# Clics En Las Flechas
									#===========================================================================
									if (xr >= 55)  and (xr <= 75)  and (yr >= 100) and (yr <= 120):		# Flecha Arriba. 
										
										while True:
											
											if not ContDir in Direcciones: Direcciones[0] = ContDir; break
											else: ContDir += 1
											ContDir %= 5
											if ContDir == 0: Direcciones[0] = ContDir; break
											
									if (xr >= 95)  and (xr <= 115) and (yr >= 100) and (yr <= 120):		# Flecha Derecha.
										
										while True:
											
											if not ContDir in Direcciones: Direcciones[1] = ContDir; break
											else: ContDir += 1
											ContDir %= 5
											if ContDir == 0: Direcciones[1] = ContDir; break
											
									if (xr >= 135) and (xr <= 155) and (yr >= 100) and (yr <= 120):		# Flecha Abajo.
										
										while True:
											
											if not ContDir in Direcciones: Direcciones[2] = ContDir; break
											else: ContDir += 1
											ContDir %= 5
											if ContDir == 0: Direcciones[2] = ContDir; break
											
									if (xr >= 175) and (xr <= 195) and (yr >= 100) and (yr <= 120):		# Flecha Izquierda.
										
										while True:
											
											if not ContDir in Direcciones: Direcciones[3] = ContDir; break
											else: ContDir += 1
											ContDir %= 5
											if ContDir == 0: Direcciones[3] = ContDir; break
									
									if BtnRepetirNodos:
										if (xr >= 155) and (xr <= 195) and (yr >= 220) and (yr <= 240): BtnRepetirNodos = False
									else:
										if (xr >= 150) and (xr <= 200) and (yr >= 220) and (yr <= 240): BtnRepetirNodos = True
										
									if (xr >= 30) and (xr <= 55) and (yr >= 277) and (yr <= 297):
										if BtnTipoBusqueda == 'Backtracking': TipoBusqueda = 0; BtnTipoBusqueda = 'Normal'
										elif BtnTipoBusqueda == 'A Estrella': TipoBusqueda = 1; BtnTipoBusqueda = 'Backtracking'
										
									elif (xr >= 185) and (xr <= 210) and (yr >= 277) and (yr <= 297):
										if BtnTipoBusqueda == 'Normal': TipoBusqueda = 1; BtnTipoBusqueda = 'Backtracking'
										elif BtnTipoBusqueda == 'Backtracking': TipoBusqueda = 2; BtnTipoBusqueda = 'A Estrella'
										
									#===========================================================================
								else:
									if (xr >= 480) and (xr <= 530) and (yr >= 582) and (yr <= 602): BtnOrdenExpansion = True
							
							if NumPlayer != None:
								if Pagina1:
									Y = 205
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo1 = True
									else: Costo1 = False
									Y += 70
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo2 = True
									else: Costo2 = False
									Y += 70
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo3 = True
									else: Costo3 = False
									Y += 70
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo4 = True
									else: Costo4 = False
									Y += 70
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo5 = True
									else: Costo5 = False
								else:
									Y = 205
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo6 = True
									else: Costo6 = False
									Y += 70
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo7 = True
									else: Costo7 = False
									Y += 70
									if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20) and NumPlayer != None: Costo8 = True
									else: Costo8 = False
							else:
								Error = True
								CadenaError = 'Selecciona Un Personaje.'
							
							if SelectEstados:
								
								SelTemp = seleccion				# Selección temporal, para mostrar el cuadro seleccionado con el mouse.
								SelTemp = obtenerPosicionClic(XPOS, YPOS, pos, dimension, puntoInicio, SelTemp)		# Función Que crea una selección Temporal
							
							#===========================================================================
							
							if (xr >= 80)   and (xr <= 180)  and (yr >= 325) and (yr <= 360) and Iniciar: Btn3Pressed = True
							if (xr >= 70)   and (xr <= 190)  and (yr >= 355) and (yr <= 410) and Iniciar: Btn4Pressed = True
							
							if (xr >= 950)  and (xr <= 1050) and (yr >= 110) and (yr <= 135): Btn2Pressed = True
							if (xr >= 1050) and (xr <= 1075) and (yr >= 550) and (yr <= 570):
								
								if Pagina1: Pagina1 = False
								else: Pagina1 = True
						
							# ================= Cooredenadas Botón Izquierda y Derecha =================
							
							X = 1006; Y = 228
							
							if NumPlayer != None:
								
								CadenaError = ''
								CadenaError2 = ''
								
								LisyPos1,LisyPos2,LisyPos3,LisyPos4,LisyPos5,LisyPos6,LisyPos7,LisyPos8 = BotonesFlechas(X,Y,xr,yr,Lisy,LisyPos1,LisyPos2,LisyPos3,LisyPos4,LisyPos5,LisyPos6,LisyPos7,LisyPos8)
							else:
								Error = True
								CadenaError = 'Selecciona Un Personaje'
							#=====================================================================================
							
							# Coordenadas Recuadros Personajes 1, 2 y 3 respectivamente:
							if SelectPerson == True:
								
								Y = 339
								if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers1 = True; Error = False
								elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers2 = True; Error = False
								elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers3 = True; Error = False
								
								Y += 60
								if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers4 = True; Error = False
								elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers5 = True; Error = False
								elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers6 = True; Error = False
								
								Y += 60
								if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers7 = True; Error = False
								elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers8 = True; Error = False
								elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers9 = True; Error = False
								
								Y += 60
								if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers10 = True; Error = False
								elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers11 = True; Error = False
								elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers12 = True; Error = False
						
							#=====================================================================================
						
						#=====================================================================================
				
			elif evento.type == pygame.MOUSEBUTTONUP: #============================== Al Dejar de Presionar Cualquier Botón del Mouse. ==============================
				
				if Btn4Pressed: # Si Se Presionó el Botón 3 (Seleccionar Personaje).
					
					MusicFondo1.stop()
					MusicFondo1.play(-1)
					MusicFondo2.stop()
					
					Error = False
					CadenaError = ''
					
					Movimientos = 0
					CostoTotal = 0
					
					SELECT = []
					Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia el Enmascaramiento del Mapa.
					
					DibujarInfo = False
					SelectPerson = True
					Iniciar = False
					Cargar = True
					
				if Btn3Pressed: # Si Se Presionó el Botón 3 (Reiniciar).
					
					MusicFondo2.stop()
					MusicFondo2 = MusicFondos[random.randint(0,len(MusicFondos)-1)]
					MusicFondo2.play(-1)
					
					Victory = True
					Error = False
					CadenaError = ''
					
					Movimientos = 1
					CostoTotal = 0
					
					seleccion = PuntoInicio
					
					SELECT = []
					SELECT.append((seleccion, [Movimientos]))
					
					Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia el Enmascaramiento del Mapa.
					
					for val in VALORES:
						if val[0] == PuntoInicio: CostoTotal += float(val[3])
					
					if TipoBusqueda == 0:
						
						ArbolRaiz = Arbol.Raiz(seleccion)
						PosLetra = LETRAS.index(seleccion[0])
						x, y = PosLetra, seleccion[1]
						AgregarAlArbol(ArbolRaiz, 'N/A', seleccion, x, y, YPOS, XPOS)
						# ~ Arbol.ImprimirArbol(ArbolRaiz)
					
					elif TipoBusqueda == 1:
						
						#===============================================
						PadreSeleccion = seleccion
						ListaBT = []
						ListaHijos = []
						Pila = [(PuntoInicio, [])]
						ArbolRaiz = Arbol.Raiz(seleccion)
						
						#================================================================================
						XTemp = LETRAS.index(seleccion[0])
						YTemp = seleccion[1]
						
						UpTemp    = [LETRAS[XTemp], YTemp-1]
						RightTemp = [LETRAS[XTemp+1], YTemp]
						DownTemp  = [LETRAS[XTemp], YTemp+1]
						LeftTemp  = [LETRAS[XTemp-1], YTemp]
						
						ListaTemp = [UpTemp, RightTemp, DownTemp, LeftTemp]
						
						# Se Le agrega a lista de Hijos sus Hijos (Solo las Coordenadas).
						for x in VALORES:
							if x[0] == ListaTemp[Direcciones.index(1)] and x[3] != '':
								Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(1)]); break
						for x in VALORES:
							if x[0] == ListaTemp[Direcciones.index(2)] and x[3] != '':
								Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(2)]); break
						for x in VALORES:
							if x[0] == ListaTemp[Direcciones.index(3)] and x[3] != '':
								Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(3)]); break
						for x in VALORES:
							if x[0] == ListaTemp[Direcciones.index(4)] and x[3] != '':
								Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(4)]); break
						
						Arbol.AgregarIniFin(ArbolRaiz, seleccion, True)				# Se Indica que es el Nodo Inicial.
						Arbol.AgregarEstado(ArbolRaiz, seleccion, 'Cerrado')		# Si el Nodo es Visitado, Es Cerrado.
						Arbol.AgregarPadre(ArbolRaiz, seleccion, 'N/A')				# Se le agrega al Nodo Actual cual es su Padre.
						Arbol.AgregarOrden(ArbolRaiz, seleccion, Movimientos)		# Se Agrega La Lista Con El Orden De Visitas.
						#================================================================================
						
						seleccion = Backtracking(XPOS, YPOS, seleccion, ArbolRaiz, 'N/A')
						# ~ Arbol.ImprimirArbol(ArbolRaiz)
						#===============================================
					
				if Btn2Pressed and not Error2:		# Si el Botón 2 (Comenzar) Fue Presionado.
					
					if NumPlayer == None:		# Si el Botón 2 Fue Presionado Pero No se ha seleccionado Personaje Marcara Error.
						
						Error = True
						CadenaError = 'Selecciona Un Personaje.'
						Iniciar = False
					
					elif PuntoInicio == None:
						
						Error = True
						CadenaError = 'Selecciona un Estado Inicial.'
					  
					elif PuntoDestino == None:
						
						Error = True
						CadenaError = 'Selecciona un Estado Final.'
					
					elif 0 in Direcciones:
						
						Error = True
						CadenaError = 'Elige un Orden de Expansión.'
					
					else:			# Si Se Selecciono Un Personaje, Se Iniciará.
						
						Iniciar = True	# Inicia El Juego.
						Victory = True
						
						MusicFondo2.stop()
						MusicFondo2 = MusicFondos[random.randint(0,len(MusicFondos)-1)]
						MusicFondo1.stop()
						MusicFondo2.play(-1)
						
						seleccion = PuntoInicio
						
						personaje = Personaje(RutaPersonaje[NombrePersonaje[NumPlayer]]) # Se Crea el Objeto Personaje de la clase (Personaje),
																				  # Pasandole La Ruta de la Imagen Que se encuentra en el Diccionario (RutaPersonaje),
																				  # Que corresponda al Nombre de Personaje de la lista (NombrePersonaje)
																				  # Que este en la posición del Numero de Personaje Elegido (NumPlayer)
						
						if NumPlayer == 4 or NumPlayer == 8 or NumPlayer == 11:	
							
							personaje.flip()				# Acomodamos Al Personaje Mirando a Derecha.
							personaje.setDireccion('R')
							
						Objetos['Personaje'] = personaje		# Se Guarda el Objeto Personaje en el Diccionario.
						SelectPerson = False					# Ya No Permite Seleccionar otro Personaje hasta Presionar el Botón 4 (Seleccionar Personaje)
						
						for val in VALORES:
							if val[0] == PuntoInicio: CostoTotal += float(val[3])
								
						Movimientos += 1
						SELECT.append((seleccion, [Movimientos]))
						
						if TipoBusqueda == 0:
							
							ArbolRaiz = Arbol.Raiz(seleccion)
							PosLetra = LETRAS.index(seleccion[0])
							x, y = PosLetra, seleccion[1]
							AgregarAlArbol(ArbolRaiz, 'N/A', seleccion, x, y, YPOS, XPOS)
							# ~ Arbol.ImprimirArbol(ArbolRaiz)
						
						elif TipoBusqueda == 1:
							
							#===============================================
							PadreSeleccion = seleccion
							ListaBT = []
							ListaHijos = []
							Pila = [(PuntoInicio, [])]
							ArbolRaiz = Arbol.Raiz(seleccion)
							
							#================================================================================
							XTemp = LETRAS.index(seleccion[0])
							YTemp = seleccion[1]
							
							UpTemp    = [LETRAS[XTemp], YTemp-1]
							RightTemp = [LETRAS[XTemp+1], YTemp]
							DownTemp  = [LETRAS[XTemp], YTemp+1]
							LeftTemp  = [LETRAS[XTemp-1], YTemp]
							
							ListaTemp = [UpTemp, RightTemp, DownTemp, LeftTemp]
							
							# Se Le agrega a lista de Hijos sus Hijos (Solo las Coordenadas).
							for x in VALORES:
								if x[0] == ListaTemp[Direcciones.index(1)] and x[3] != '':
									Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(1)]); break
							for x in VALORES:
								if x[0] == ListaTemp[Direcciones.index(2)] and x[3] != '':
									Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(2)]); break
							for x in VALORES:
								if x[0] == ListaTemp[Direcciones.index(3)] and x[3] != '':
									Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(3)]); break
							for x in VALORES:
								if x[0] == ListaTemp[Direcciones.index(4)] and x[3] != '':
									Arbol.AgregarHijos(ArbolRaiz, seleccion, ListaTemp[Direcciones.index(4)]); break
							
							Arbol.AgregarIniFin(ArbolRaiz, seleccion, True)			# Se Indica que es el Nodo Inicial.
							Arbol.AgregarEstado(ArbolRaiz, seleccion, 'Cerrado')	# Si el Nodo es Visitado, Es Cerrado.
							#================================================================================
							
							seleccion = Backtracking(XPOS, YPOS, seleccion, ArbolRaiz, 'N/A')
							# ~ Arbol.ImprimirArbol(ArbolRaiz)
							#===============================================
						
						
				elif Btn2Pressed and Error2:		# Si el Botón 2 (Comenzar) Fue Presionado y Ocurrio un Error.
					
					CadenaError2 = 'Bloques Aún No Asignados.'
					
				elif CargarMapa:	# Si el Botón 1 Fue Seleccionado.
					
					xMatrixy, xLisy, xXPOS, xYPOS, xPOS = TODOArchivo()		# Obtenemos Valores desde la Función Temporalmente.
					
					if Error:		# Si Hubo Error.
					
						Error2 = False
					
					if xMatrixy == None:	# Si los Valores Se Encuentran En Null (None aqui en python) significa que hubo un error.
						
						if Cargar == False: pass		# Si el Valor era False se mantiene.
						else: Cargar = True				# Si el Valor Era None cambia a True.
						CargarMapa = False				# Se Cancela el Cargar el Mapa.
					
					else:	# Si la Matriz tiene informacion, Todo Estuvo Correcto y Validado.
						
						Sucess.play()
						
						MusicFondo1.stop()
						MusicFondo1.play(-1)
						MusicFondo2.stop()
						
						SELECT = []			 	# Se Reinicia La Variable Global SELECT, que guarda el Recorrido para imprimirlo en la Matriz. 
						SelectEstados = False	# Permite Saber Si se Permite Selecciona el Estado Inicial y Final.
						Pagina1 = True		 	# Se Vuelve a Posicionar la Página 1 en la Seleccion de Terrenos para el Mapa.
						DibujarInfo = False  	# Al Cargar Un Nuevo Mapa, Se Deja de Mostrar La Información de Seleccion.
						Iniciar = False		 	# Aun no se permite Iniciar La Partida.
						Cargar = True		 	# Se Dibuja El Mapa.
						SelectPerson = True		# Permite Seleccionar Algun Personaje.
						
						# Se Crean Nuevos Objetos Bloque para el nuevo Mapa.
						bloque1 = Bloque("img/Texturas/Pared.jpg")		# Objeto Pared.
						bloque3 = Bloque("img/Texturas/Camino.jpg")		# Objeto Camino.
						bloque4 = Bloque("img/Texturas/Bosque.jpg")		# Objeto Bosque.
						bloque5 = Bloque("img/Texturas/Lava.jpg")		# Objeto Lava.
						bloque6 = Bloque("img/Texturas/Agua.jpg")		# Objeto Agua.
						bloque7 = Bloque("img/Texturas/Arena.jpg")		# Objeto Arena.
						bloque8 = Bloque("img/Texturas/Montania.jpg")	# Objeto Montaña.
						bloque9 = Bloque("img/Texturas/Nieve.jpg")		# Objeto Nieve.
						
						# Se Pasan los valores Temporales a los Originales.
						Matrixy = xMatrixy
						Lisy = ['-1']				# Se Reinicia la Lista con el Primer Elemento, el -1 para la Selección de Terrenos.
						Lisy = Lisy + xLisy			# Se le añaden todos los Valores.
						
						# Se Reinician Las Variables Globales (Pared, Camino, Bosque, Lava, Agua, Arena, Montaña, Nieve) en 0.
						# Se Reinician Las Variables De Posición Para la Selección de Terrenos en 0.
						Pared   = LisyPos1 = 0
						Camino  = LisyPos2 = 0
						Bosque  = LisyPos3 = 0
						Lava    = LisyPos4 = 0
						Agua    = LisyPos5 = 0
						Arena   = LisyPos6 = 0
						Montaña = LisyPos7 = 0
						Nieve	= LisyPos8 = 0
						
						# Obtenemos El Ancho y Alto del Mapa, Para Cargar La Matriz Correctamente.
						XPOS = xXPOS		# Valor de las Letras.
						YPOS = xYPOS		# Valor de las Numeros.
						POS = xPOS			# Obtenemos Cual es el Mas grande de Los 2.
						
						Mask = [ [ False for x in range(XPOS) ] for x in range(YPOS) ]		# Se Reinicia el Enmascaramiento del Mapa.
						
						puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)	# Se Indica El Punto de Inicio Para Dibujar La Matriz.
						
						# Se Reinicia el Diccionario Objetos con los Nuevos Objetos Generados.
						Objetos = {'Pared':bloque1,	'Camino':bloque3,	'Bosque': bloque4,	'Lava': bloque5,
								   'Agua': bloque6,	'Arena': bloque7,	'Montaña':bloque8,	'Nieve':bloque9}
						
						Movimientos  = 0
						CostoTotal	 = 0
						PuntoInicio	 = None		# Se Inicializa la Variable Global PuntoInicio en None.
						PuntoDestino = None		# Se Inicializa la Variable Global PuntoDestino en None.
						NumPlayer	 = None		# Se Inicializa la Variable personaje en None.
						CargarMapa	 = False	# Indíca que El Botón Cargar Mapa Dejo de ser Apretado.
						Error		 = False	# Indíca Que No Hay Error.
				
				Btn1Pressed = False			# Indica Que El Botón 'Cargar Mapa' Ya No esta Siendo Presionado. 
				Btn2Pressed = False			# Indica Que El Botón 'Comenzar' Ya No esta Siendo Presionado. 
				Btn3Pressed = False			# Indica Que El Botón 'Reiniciar' Ya No esta Siendo Presionado. 
				Btn4Pressed = False			# Indica Que El Botón 'Seleccionar Personaje' Ya No esta Siendo Presionado. 
				
				pygame.mouse.set_visible(True)	# Se Hace de Nuevo Visible El Cursor Del Mouse.
				SelTemp = ['P',16]				# La Selección Temporal se manda a un valor jamas cargado en el mapa. (16, 16)
												# Para que deje de mostrarse la selección con el Puntero.
		
		
		
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		
		
		screen.blit(BGimg, (0, 0))	# Se Carga La Imagen De Fondo.
		
		
		#===============================================================================================================================
		#======================================== Sección Derecha ======================================================================
		#===============================================================================================================================
		
		
		
		# Mismas Imagenes pero con diferente Color, Para el Botón 1 (Cargar Mapa).
		boton1.resize(150, 50)		# Se Ajusta el Tamanio para el boton1.
		boton2.resize(150, 50)		# Se Ajusta el Tamanio para el boton2.
		
		if Btn1Pressed == False: screen.blit(boton1.image, (927, 15))		# Si el Botón 1 No Ha Sido Presionado, se Mostrara el objeto boton1
		else: screen.blit(boton2.image, (927, 15))							# Si no, se mostrara el objeto boton2 mientras este presionado el Boton.
		
		# Dibuja El Texto en El Boton. Los 2 Textos Son el Mismo, Dan el Efecto de Profundidad.
		dibujarTexto(screen, 'Cargar Mapa',	[937, 25], Fuentes['Wendy 30'], COLOR['Naranja'])
		dibujarTexto(screen, 'Cargar Mapa', [938, 26], Fuentes['Wendy 30'], COLOR['Naranja'])
		dibujarTexto(screen, 'Cargar Mapa', [939, 27], Fuentes['Wendy 30'], COLOR['Amarillo'])
		
		#======================================================================================
		if Error:	# Si Ocurrio Un Error, Esta Sección Es La Que se Encargara de Mostrarlo.
			
			if Error2 and CadenaError2 != '':
				# Dibuja El Texto en Pantalla. Ambos Son El Mismo, Pero 1 Pixel de diferencia uno del otro, da efecto de profundidad.
				dibujarTexto(screen, CadenaError2, [900, 69], Fuentes['Droid 15'], COLOR['Naranja'])
				dibujarTexto(screen, CadenaError2, [901, 70], Fuentes['Droid 15'], COLOR['Rojo'])
				CadenaError = ''
				Error = False
			else:
				# Dibuja El Texto en Pantalla. Ambos Son El Mismo, Pero 1 Pixel de diferencia uno del otro, da efecto de profundidad.
				dibujarTexto(screen, CadenaError, [900, 69], Fuentes['Droid 15'], COLOR['Naranja'])
				dibujarTexto(screen, CadenaError, [901, 70], Fuentes['Droid 15'], COLOR['Rojo'])
				CadenaError2 = ''
				Error2 = False
				
		elif Error2:
			
			# Dibuja El Texto en Pantalla. Ambos Son El Mismo, Pero 1 Pixel de diferencia uno del otro, da efecto de profundidad.
			dibujarTexto(screen, CadenaError2, [900, 69], Fuentes['Droid 15'], COLOR['Naranja'])
			dibujarTexto(screen, CadenaError2, [901, 70], Fuentes['Droid 15'], COLOR['Rojo'])
			CadenaError = ''
			Error = False
		
		#======================================================================================
		
		# Dibuja Recuadro Derecha.
		pygame.draw.rect(screen, COLOR['Gris'],   [900, 100,  200, 480], 0)
		pygame.draw.rect(screen, COLOR['Gris'],   [900, 100,  200, 480], 3)
		
			# Dibuja la Sección para 'Asignar Valores a Terrenos'.
		
		if Cargar and Iniciar == False:		# Si Ya Se Cargo el Mapa y Aun no se ha iniciado el Juego con el Botón 'Comenzar':
			
			botonPers1.resize(100,35)
			botonPers2.resize(100,35)
			
			if Btn2Pressed == False: screen.blit(botonPers1.image, (950,105))
			else: screen.blit(botonPers2.image, (950,105))
			
			dibujarTexto(screen, 'Comenzar', [960, 111], Fuentes['Wendy 25'], COLOR['Negro'])
			dibujarTexto(screen, 'Comenzar', [961, 112], Fuentes['Wendy 25'], COLOR['Purpura'])
			
			#==========================================================================================================================
			
			dibujarTexto(screen, 'Asignar Valores', [909, 139], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Asignar Valores', [910, 140], Fuentes['Droid 20'], COLOR['Morado'])
			
			dibujarTexto(screen, 'Personaje: ', [909, 159], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Personaje:', [910, 160], Fuentes['Droid 20'], COLOR['Morado'])
			
			if NumPlayer == None:	# Si Aun No Se Ha Seleccionado Un Personaje.
				
				dibujarTexto(screen, 'Ninguno', [1009, 159], Fuentes['Droid 20'], COLOR['Azul'])
				dibujarTexto(screen, 'Ninguno', [1010, 160], Fuentes['Droid 20'], COLOR['Negro'])
				
			else:			# Si ya fue Seleccionado.
				
				dibujarTexto(screen, NombrePersonaje[NumPlayer], [1009, 159], Fuentes['Droid 20'], COLOR['Azul'])
				dibujarTexto(screen, NombrePersonaje[NumPlayer], [1010, 160], Fuentes['Droid 20'], COLOR['Negro'])
			
			
			if LisyPos2 in [LisyPos1] and LisyPos2 != 0: 
				Er1 = True
			else: Er1 = False
			if LisyPos3 in [LisyPos1, LisyPos2] and LisyPos3 != 0:
				Er2 = True
			else: Er2 = False
			if LisyPos4 in [LisyPos1, LisyPos2, LisyPos3] and LisyPos4 != 0:
				Er3 = True
			else: Er3 = False
			if LisyPos5 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4] and LisyPos5 != 0:
				Er4 = True
			else: Er4 = False
			if LisyPos6 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5] and LisyPos6 != 0:
				Er5 = True
			else: Er5 = False
			if LisyPos7 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6] and LisyPos7 != 0:
				Er6 = True
			else: Er6 = False
			if LisyPos8 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6, LisyPos7] and LisyPos8 != 0:
				Er7 = True
			else: Er7 = False

			if Pagina1:
				
					# Bloque 1:	============================================
				
				Y = 190
				DibujarMiniaturaTextura(screen, Costo1, 0, Objetos10, BtnIzq1, BtnDer1, 910, Y, 'Pared', Lisy, LisyPos1, Fuentes)
				
					# Bloque 2:	============================================
				
				Y += 70
				if LisyPos2 in [LisyPos1] and LisyPos2 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo2, 1, Objetos10, BtnIzq2, BtnDer2, 910, Y, 'Camino', Lisy, LisyPos2, Fuentes, True)
					
				else: DibujarMiniaturaTextura(screen, Costo2, 1, Objetos10, BtnIzq2, BtnDer2, 910, Y, 'Camino', Lisy, LisyPos2, Fuentes)
				
					# Bloque 3:	============================================
				
				Y += 70
				if LisyPos3 in [LisyPos1, LisyPos2] and LisyPos3 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo3, 2, Objetos10, BtnIzq3, BtnDer3, 910, Y, 'Bosque', Lisy, LisyPos3, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo3, 2, Objetos10, BtnIzq3, BtnDer3, 910, Y, 'Bosque', Lisy, LisyPos3, Fuentes)
				
					# Bloque 4:	============================================
				
				Y += 70
				if LisyPos4 in [LisyPos1, LisyPos2, LisyPos3] and LisyPos4 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo4, 3, Objetos10, BtnIzq4, BtnDer4, 910, Y, 'Lava', Lisy, LisyPos4, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo4, 3, Objetos10, BtnIzq4, BtnDer4, 910, Y, 'Lava', Lisy, LisyPos4, Fuentes)
				
					# Bloque 5:	============================================
				
				Y += 70
				if LisyPos5 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4] and LisyPos5 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo5, 4, Objetos10, BtnIzq5, BtnDer5, 910, Y, 'Agua', Lisy, LisyPos5, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo5, 4, Objetos10, BtnIzq5, BtnDer5, 910, Y, 'Agua', Lisy, LisyPos5, Fuentes)
				
			else:
					# Bloque 6:	============================================
				
				Y = 190
				if LisyPos6 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5] and LisyPos6 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava, Agua)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo6, 5, Objetos10, BtnIzq6, BtnDer6, 910, Y, 'Arena', Lisy, LisyPos6, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo6, 5, Objetos10, BtnIzq6, BtnDer6, 910, Y, 'Arena', Lisy, LisyPos6, Fuentes)
				
					# Bloque 7:	============================================
				
				Y += 70
				if LisyPos7 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6] and LisyPos7 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava, Agua, Arena)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo7, 6, Objetos10, BtnIzq7, BtnDer7, 910, Y, 'Montaña', Lisy, LisyPos7, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo7, 6, Objetos10, BtnIzq7, BtnDer7, 910, Y, 'Montaña', Lisy, LisyPos7, Fuentes)
				
					# Bloque 8:	============================================
				
				Y += 70
				if LisyPos8 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6, LisyPos7] and LisyPos8 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava, Agua, Arena, Montaña)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo8, 7, Objetos10, BtnIzq8, BtnDer8, 910, Y, 'Nieve', Lisy, LisyPos8, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo8, 7, Objetos10, BtnIzq8, BtnDer8, 910, Y, 'Nieve', Lisy, LisyPos8, Fuentes)
				
			#==========================================================================================================================
			
			# Asigna Los Valores a las Variables Globales Siguientes:
			Pared   = LisyPos1
			Camino  = LisyPos2
			Bosque  = LisyPos3
			Lava    = LisyPos4
			Agua    = LisyPos5
			Arena   = LisyPos6
			Montaña = LisyPos7
			Nieve	= LisyPos8
			
			# Marcando Errores:
			if Er1 or Er2 or Er3 or Er4 or Er5 or Er6 or Er7:
				
				# Si Aun No se Han Elegido Todos Los Bloques se Pondran Punto Inicial y Final en None.
				SelectEstados = False
				PuntoInicio = None
				PuntoDestino = None
				
				Error2 = True
				CadenaError2 = 'Hay Bloques Repetidos.'
			
			else:
				
				ConTer = 0
				
				if Pared   > 0 and Pared   < len(Lisy): ConTer += 1
				if Camino  > 0 and Camino  < len(Lisy): ConTer += 1
				if Bosque  > 0 and Bosque  < len(Lisy): ConTer += 1
				if Lava    > 0 and Lava    < len(Lisy): ConTer += 1
				if Agua    > 0 and Agua    < len(Lisy): ConTer += 1
				if Arena   > 0 and Arena   < len(Lisy): ConTer += 1
				if Montaña > 0 and Montaña < len(Lisy): ConTer += 1
				if Nieve   > 0 and Nieve   < len(Lisy): ConTer += 1
				
				if ConTer == len(Lisy)-1:
					
					SelectEstados = True	# Permite Seleccionar Punto Inicio y Destino
					
					Error2 = False
					CadenaError2 = ''
				else:
					
					SelectEstados = False	# Permite Seleccionar Punto Inicio y Destino
					
					if not Error2:
						Error2 = True
						CadenaError2 = ''
						
			
			if Pagina1:		# Si Se esta Posicionado en la Página 1 de Selección de Terrenos, Dibujará los primeros 5 Terrenos.
				
				# Mostrará Botón para Seleccionar la Página Siguiente.
				dibujarTexto(screen, 'Página Siguiente', [930, 550], Fuentes['Droid 15'], COLOR['Negro'])
				BtnPagDer.resize(25,20)
				screen.blit(BtnPagDer.image, (1050, 550))
				
			else:			# Si no, Muestra El Resto.
				
				# Mostrará Botón para Seleccionar la Página Anterior.
				dibujarTexto(screen, 'Página Anterior', [930, 550], Fuentes['Droid 15'], COLOR['Negro'])
				BtnPagIzq.resize(25,20)
				screen.blit(BtnPagIzq.image, (1050, 550))
		
		#===============================================================
		
		if DibujarInfo: DibujarInformacionClic(screen, Fuentes, SelTemp)
		
		#===============================================================
		
		if Iniciar:
			
			dibujarTexto(screen, 'Busqueda: ', [920, 460], Fuentes['Droid 16'], COLOR['Verde Claro'])
			dibujarTexto(screen, 'Busqueda: ', [921, 461], Fuentes['Droid 16'], COLOR['Verde'])
			
			if BtnTipoBusqueda == 'Normal':
				
				dibujarTexto(screen, 'Manual', [1002, 460], Fuentes['Droid 16'], COLOR['Azul Claro'])
				dibujarTexto(screen, 'Manual', [1003, 461], Fuentes['Droid 16'], COLOR['Azul'])
				
			elif BtnTipoBusqueda == 'Backtracking':
				
				dibujarTexto(screen, 'Backtracking', [1002, 460], Fuentes['Droid 16'], COLOR['Azul Claro'])
				dibujarTexto(screen, 'Backtracking', [1003, 461], Fuentes['Droid 16'], COLOR['Azul'])
				
			elif BtnTipoBusqueda == 'A Estrella':
				
				dibujarTexto(screen, 'A* (Estrella)', [1002, 460], Fuentes['Droid 16'], COLOR['Azul Claro'])
				dibujarTexto(screen, 'A* (Estrella)', [1003, 461], Fuentes['Droid 16'], COLOR['Azul'])
				
			Flechas = [FlechaArr, FlechaDer, FlechaAba, FlechaIzq]
			
			dibujarTexto(screen, 'Orden de Expansión', [920, 500], Fuentes['Droid 16'], COLOR['Negro'])
			dibujarTexto(screen, 'Orden de Expansión', [921, 501], Fuentes['Droid 16'], COLOR['Azul'])
			
			screen.blit(Flechas[Direcciones.index(1)].image, (920, 540))
			screen.blit(Flechas[Direcciones.index(2)].image, (960, 540))
			screen.blit(Flechas[Direcciones.index(3)].image, (1000, 540))
			screen.blit(Flechas[Direcciones.index(4)].image, (1040, 540))
		
		
		
		#===============================================================================================================================
		#======================================== Sección Central ======================================================================
		#===============================================================================================================================
		
		
		
		pygame.draw.rect(screen, COLOR['Fondo'], [puntoInicio[0], puntoInicio[1], dimension*XPOS, dimension*YPOS], 0)
		
		# Si Cargar es Igual a True entonces Dibujara El Mapa.
		if Cargar: dibujarMapa(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, Fuentes, SelTemp, Matrixy, Lisy, Objetos, BtnMaskPressed)
		
		if Cargar and not Iniciar and DibujarInfoXY and SelectEstados and SelInfoTemp != ['P',16]:
			
			xD += 1
			pygame.draw.rect(screen, COLOR['Gris Claro'], [DibujarInfoX, DibujarInfoY, 62, 35], 0)
			
			dibujarTexto(screen, 'Posición: ' + str(SelInfoTemp[0]) + ', ' + str(SelInfoTemp[1]), [DibujarInfoX+2, DibujarInfoY+1], Fuentes['Droid 10'], COLOR['Azul Claro'])
			dibujarTexto(screen, 'Posición: ' + str(SelInfoTemp[0]) + ', ' + str(SelInfoTemp[1]), [DibujarInfoX+3, DibujarInfoY+2], Fuentes['Droid 10'], COLOR['Azul'])
			
			for val in VALORES:
				if val[0] == SelInfoTemp:
					
					dibujarTexto(screen, 'Tipo: ' + str(val[2]), [DibujarInfoX+2, DibujarInfoY+11], Fuentes['Droid 10'], COLOR['Azul Claro'])
					dibujarTexto(screen, 'Tipo: ' + str(val[2]), [DibujarInfoX+3, DibujarInfoY+12], Fuentes['Droid 10'], COLOR['Azul'])
					
					if val[3] == '':
						dibujarTexto(screen, 'Costo: N/A', [DibujarInfoX+2, DibujarInfoY+21], Fuentes['Droid 10'], COLOR['Azul Claro'])
						dibujarTexto(screen, 'Costo: N/A', [DibujarInfoX+3, DibujarInfoY+22], Fuentes['Droid 10'], COLOR['Azul'])
					else:
						dibujarTexto(screen, 'Costo: ' + str(val[3]), [DibujarInfoX+2, DibujarInfoY+21], Fuentes['Droid 10'], COLOR['Azul Claro'])
						dibujarTexto(screen, 'Costo: ' + str(val[3]), [DibujarInfoX+3, DibujarInfoY+22], Fuentes['Droid 10'], COLOR['Azul'])
					
					break
			
			if xD == 30:	# Si ya Pasaron .5 Segundos (30 Frames) entonces dejara de mostrarse la información.
				
				DibujarInfoXY = False
				xD = 0
			
		else: xD = 0
		
		
		
		#=================================================================================================================================
		#======================================== Sección Izquierda ======================================================================
		#=================================================================================================================================
		
		
		
		# Dibuja El Rectangulo Para la Sección Izquierda.
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,   240, 30],   0)
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,   240, 30],   3)
		pygame.draw.rect(screen, COLOR['Gris'],   [10, 40,   240, 540],  0)
		pygame.draw.rect(screen, COLOR['Gris'],   [10, 40,   240, 540],  3)
		pygame.draw.line(screen, COLOR['Negro'],  [9,  40], [250,  40],  3)
		
		dibujarTexto(screen, 'Informacion', [69, 11],  Fuentes['Wendy 30'], COLOR['Verde'])
		dibujarTexto(screen, 'Informacion', [70, 12],  Fuentes['Wendy 30'], COLOR['Verde Claro'])
		
					#===============================================================
		
					# Dibuja La Sección de 'Informacion':
		
		dibujarTexto(screen, 'Personaje: ', [15, 54], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Personaje: ', [16, 55], Fuentes['Droid 20'], COLOR['Azul'])
		
		if NumPlayer == None:	# Si Aun No Se Ha Seleccionado Un Personaje.
			
			dibujarTexto(screen, 'Seleccionar', [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen, 'Seleccionar', [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:			# Si ya fue Seleccionado.
			
			dibujarTexto(screen,  NombrePersonaje[NumPlayer], [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen,  NombrePersonaje[NumPlayer], [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
		
		dibujarTexto(screen, 'Posición Actual: ', [14, 95],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Posición Actual: ', [15, 96],  Fuentes['Droid 20'], COLOR['Azul'])
		
		if seleccion == None:		# Si Aun no hay nada en la Variable global seleccion, Dibuja 'Ninguna'.
			
			dibujarTexto(screen,  'Ninguna', [162, 95], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen,  'Ninguna', [163, 96], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:						# De lo contrario, Dibuja la Posición actual del Personaje.
			
			if Iniciar:		# Si se inicio el Juego
				dibujarTexto(screen, str(seleccion[0])+', '+str(seleccion[1]), [162, 95], Fuentes['Droid 20'], COLOR['Verde'])
				dibujarTexto(screen, str(seleccion[0])+', '+str(seleccion[1]), [163, 96], Fuentes['Droid 20'], COLOR['Negro'])
			else:			# Si no...
				dibujarTexto(screen,  'Ninguna', [162, 95], Fuentes['Droid 20'], COLOR['Verde'])
				dibujarTexto(screen,  'Ninguna', [163, 96], Fuentes['Droid 20'], COLOR['Negro'])
				
		
		Temp = 'Ninguno'			# Variable Temporal Que Imprime el Nombre del Terreno Actual.
		for x in VALORES:			# Se Obtienen los Valores De cada Terreno en La Matriz.
			if x[0] == seleccion: 	# Si La Posición Del Valor en X es Igual a la Selección Actual (Posición del Jugador).
				Temp = x[2]			# Dibuja El Nombre Del Terreno en esa Posicion.
		
		dibujarTexto(screen, 'Terreno Actual: ', [14, 125],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Terreno Actual: ', [15, 126],  Fuentes['Droid 20'], COLOR['Azul'])
		
		if Iniciar and Temp != 'Ninguno':
			
			dibujarTexto(screen, str(Temp),		  	 [162, 125], Fuentes['Droid 20'], COLOR['Azul'])
			dibujarTexto(screen, str(Temp),		  	 [163, 126], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:
			
			dibujarTexto(screen, 'Ninguno',		  	 [162, 125], Fuentes['Droid 20'], COLOR['Azul'])
			dibujarTexto(screen, 'Ninguno',		  	 [163, 126], Fuentes['Droid 20'], COLOR['Negro'])
			
		
		dibujarTexto(screen, 'Estado Inicial: ', [14, 165], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Estado Inicial: ', [15, 166], Fuentes['Droid 20'], COLOR['Azul'])
		
		if PuntoInicio == None:		# Si Aun no hay nada en la Variable Global PuntoInicio, Dibuja 'Ninguno'.
			
			dibujarTexto(screen,  'Ninguno', [162, 165], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen,  'Ninguno', [163, 166], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:	# De lo contrario, Dibuja la Posición Inicio del Personaje.
			
			dibujarTexto(screen, str(PuntoInicio[0])+', '+str(PuntoInicio[1]), [162, 165], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen, str(PuntoInicio[0])+', '+str(PuntoInicio[1]), [163, 166], Fuentes['Droid 20'], COLOR['Negro'])
		
		
		dibujarTexto(screen, 'Estado Final: ', [14, 195], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Estado Final: ', [15, 196], Fuentes['Droid 20'], COLOR['Azul'])
		
		if PuntoDestino == None:	# Si Aun no hay nada en la Variable Global PuntoDestino, Dibuja 'Ninguno'.
			
			dibujarTexto(screen,  'Ninguno', [162, 195], Fuentes['Droid 20'], COLOR['Azul'])
			dibujarTexto(screen,  'Ninguno', [163, 196], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:	# De lo contrario, Dibuja la Posición Destino del Personaje.
			
			dibujarTexto(screen, str(PuntoDestino[0])+', '+str(PuntoDestino[1]), [162, 195], Fuentes['Droid 20'], COLOR['Azul'])
			dibujarTexto(screen, str(PuntoDestino[0])+', '+str(PuntoDestino[1]), [163, 196], Fuentes['Droid 20'], COLOR['Negro'])
		
		
		dibujarTexto(screen, 'Total de Visitas: ', [14, 235], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Total de Visitas: ', [15, 236], Fuentes['Droid 20'], COLOR['Azul'])
		
		if PuntoDestino == None:	# Si Aun no hay nada en la Variable Global PuntoDestino, Dibuja 'Ninguno'.
			
			dibujarTexto(screen,  '0', [162, 235], Fuentes['Droid 20'], COLOR['Rojo'])
			dibujarTexto(screen,  '0', [163, 236], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:	# De lo contrario, Dibuja la Posición Destino del Personaje.
			
			dibujarTexto(screen, str(Movimientos), [162, 235], Fuentes['Droid 20'], COLOR['Rojo'])
			dibujarTexto(screen, str(Movimientos), [163, 236], Fuentes['Droid 20'], COLOR['Negro'])
		
		dibujarTexto(screen, 'Costo Total: ', [14, 265], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Costo Total: ', [15, 266], Fuentes['Droid 20'], COLOR['Azul'])
		
		dibujarTexto(screen,  str(round(CostoTotal,2)), [162, 265], Fuentes['Droid 20'], COLOR['Rojo'])
		dibujarTexto(screen,  str(round(CostoTotal,2)), [163, 266], Fuentes['Droid 20'], COLOR['Negro'])
		
		Y = 305
		pygame.draw.line(screen, COLOR['Negro'],  [9, Y], [260,  Y], 3)
		
					#===============================================================
					# Dibuja La Sección 'Selección de Personaje':
		
		if SelectPerson:
			
			Y += 5
			dibujarTexto(screen, 'Seleccionar Personaje', [27, Y-1], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Seleccionar Personaje', [28, Y], Fuentes['Droid 20'], COLOR['Morado'])
			
			# Cambia el Tamaño de Las Miniaturas de los personajes en 50x50 pixeles.
			Cuadro1.resize(50,50)
			Cuadro2.resize(50,50)
			Cuadro3.resize(50,50)
			Cuadro4.resize(50,50)
			Cuadro5.resize(50,50)
			Cuadro6.resize(50,50)
			Cuadro7.resize(50,50)
			Cuadro8.resize(50,50)
			Cuadro9.resize(50,50)
			Cuadro10.resize(50,50)
			Cuadro11.resize(50,50)
			Cuadro12.resize(50,50)
			
			Y += 30
			# Dibuja recuadros Blancos con Margen Negro en donde iran las Miniaturas.
			pygame.draw.rect(screen, COLOR['Blanco'], [28,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [28,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [98,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [98,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [168, Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [168, Y-2, 54, 54], 2)
			
			# Se Colocan Las Miniaturas.
			screen.blit(Cuadro1.image, (30,  Y))
			screen.blit(Cuadro2.image, (100, Y))
			screen.blit(Cuadro3.image, (170, Y))
			
			if seleccionPers1:		# Si El Personaje 1 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [30,  Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers1 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 0						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers2:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers2 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 1						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers3:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers3 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 2						# Se Asigna a NumPlayer el Numero De Personaje.
			
			Y += 60
			pygame.draw.rect(screen, COLOR['Blanco'], [28,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [28,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [98,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [98,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [168, Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [168, Y-2, 54, 54], 2)
			
			# Se Colocan Las Miniaturas.
			screen.blit(Cuadro4.image, (30,  Y))
			screen.blit(Cuadro5.image, (100, Y))
			screen.blit(Cuadro6.image, (170, Y))
			
			if seleccionPers4:		# Si El Personaje 1 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [30,  Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers4 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 3						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers5:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers5 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 4						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers6:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers6 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 5					# Se Asigna a NumPlayer el Numero De Personaje.
			
			Y += 60
			pygame.draw.rect(screen, COLOR['Blanco'], [28,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [28,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [98,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [98,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [168, Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [168, Y-2, 54, 54], 2)
			
			# Se Colocan Las Miniaturas.
			screen.blit(Cuadro7.image, (30,  Y))
			screen.blit(Cuadro8.image, (100, Y))
			screen.blit(Cuadro9.image, (170, Y))
			
			if seleccionPers7:		# Si El Personaje 1 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [30,  Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers7 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 6						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers8:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers8 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 7						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers9:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers9 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 8					# Se Asigna a NumPlayer el Numero De Personaje.
			
			Y += 60
			pygame.draw.rect(screen, COLOR['Blanco'], [28,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [28,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [98,  Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [98,  Y-2, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Blanco'], [168, Y-2, 54, 54], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [168, Y-2, 54, 54], 2)
			
			# Se Colocan Las Miniaturas.
			screen.blit(Cuadro10.image, (30,  Y))
			screen.blit(Cuadro11.image, (100, Y))
			screen.blit(Cuadro12.image, (170, Y))
			
			if seleccionPers10:		# Si El Personaje 1 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [30,  Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers10 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 9						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers11:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers11 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 10						# Se Asigna a NumPlayer el Numero De Personaje.
				
			elif seleccionPers12:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers12 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NumPlayer = 11					# Se Asigna a NumPlayer el Numero De Personaje.
			
			Y += 70
			pygame.draw.line(screen, COLOR['Negro'],  [9, Y], [250,  Y], 3)
		
		if Iniciar and SelectPerson == False:
			
			btnReiniciar1.resize(100,35)
			btnReiniciar2.resize(100,35)
			btnSelect1.resize(120,55)
			btnSelect2.resize(120,55)
			
			if Btn3Pressed == False: screen.blit(btnReiniciar1.image, (80, 325))
			else: screen.blit(btnReiniciar2.image, (80, 325))
			
			if Btn4Pressed == False: screen.blit(btnSelect1.image, (70, 355))
			else: screen.blit(btnSelect2.image, (70, 355))
			
			dibujarTexto(screen, 'Reiniciar', [94, 331], Fuentes['Wendy 25'], COLOR['Negro'])
			dibujarTexto(screen, 'Reiniciar', [95, 332], Fuentes['Wendy 25'], COLOR['Morado'])
			
			dibujarTexto(screen, 'Seleccionar', [78, 364], Fuentes['Wendy 25'], COLOR['Negro'])
			dibujarTexto(screen, 'Seleccionar', [79, 365], Fuentes['Wendy 25'], COLOR['Morado'])
			dibujarTexto(screen, ' Personaje',  [78, 379], Fuentes['Wendy 25'], COLOR['Negro'])
			dibujarTexto(screen, ' Personaje',  [79, 380], Fuentes['Wendy 25'], COLOR['Morado'])
			
			if seleccion == PuntoDestino:
				
				dibujarTexto(screen, 'Mapa Finalizado!', [16, 449], Fuentes['Droid 30'], COLOR['Negro'])
				dibujarTexto(screen, 'Mapa Finalizado!', [17, 450], Fuentes['Droid 30'], COLOR['Rojo'])
				
				if Victory:
					
					Victoria.play()
					Victory = False
		
		
		
		#===================================================================================================
		#======================================== Sección Baja =============================================
		#===================================================================================================
		
		
		
		if BtnMostrarArbol:
			
			Niveles = Arbol.ContadorDeNivel(ArbolRaiz)[0] * 120
			Nodos = Arbol.ContadorDeNodos(ArbolRaiz) * 120
			
			if XX1 > 150:
				if MoveX == -15: XX1 += MoveX
			elif XX1 < Niveles*-1:
				if MoveX == 15: XX1 += MoveX
			else: XX1 += MoveX
			
			if YY1 > 150:
				if MoveY == -15: YY1 += MoveY
			elif YY1 < Nodos*-1:
				if MoveY == 15: YY1 += MoveY
			else: YY1 += MoveY
			
			PX, PY = 20, 20
			
			pygame.draw.rect(screen, COLOR['Fondo'], [ 0, 0, DIMENCIONES[0], DIMENCIONES[1] ], 0)
			
			MostrarArbol(ArbolRaiz, screen, PX+XX1, PY+YY1, 100, 100, Fuentes)
		
		dibujarTexto(screen, 'Mute', [9, 582], Fuentes['Droid 18'], COLOR['Verde Claro'])
		dibujarTexto(screen, 'Mute', [10, 583], Fuentes['Droid 18'], COLOR['Verde'])
		
		dibujarTexto(screen, 'Ocultar', [134, 582], Fuentes['Droid 18'], COLOR['Verde Claro'])
		dibujarTexto(screen, 'Ocultar', [135, 583], Fuentes['Droid 18'], COLOR['Verde'])
		
		if Cargar and not Iniciar:
			dibujarTexto(screen, 'Orden Expansión', [330, 582], Fuentes['Droid 18'], COLOR['Verde Claro'])
			dibujarTexto(screen, 'Orden Expansión', [331, 583], Fuentes['Droid 18'], COLOR['Verde'])
		
		if Iniciar:
			dibujarTexto(screen, 'Ver Árbol', [964, 582], Fuentes['Droid 18'], COLOR['Verde Claro'])
			dibujarTexto(screen, 'Ver Árbol', [965, 583], Fuentes['Droid 18'], COLOR['Verde'])
		
		btnON.resize(40,20)
		btnOFF.resize(50,20)
		
		if BtnMutePressed:
			screen.blit(btnON.image, (65, 582))
			MusicFondo1.set_volume(0)
			MusicFondo2.set_volume(0)
		else:
			screen.blit(btnOFF.image, (60, 582))
			MusicFondo1.set_volume(1)
			MusicFondo2.set_volume(1)
		
		if BtnMaskPressed: screen.blit(btnON.image, (205, 582))
		else: screen.blit(btnOFF.image, (200, 582))
		
		if Cargar and not Iniciar:
			
			if BtnOrdenExpansion:
				
				screen.blit(btnON.image, (485, 582))
				
				# Dibuja El Rectangulo Para la Sección Izquierda.
				pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,   240,  30], 0)
				pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,   240,  30], 3)
				pygame.draw.rect(screen, COLOR['Blanco'], [10, 40,   240, 265], 0)
				pygame.draw.line(screen, COLOR['Negro'],  [9,  40], [250,  40], 3)
				pygame.draw.line(screen, COLOR['Negro'],  [9, 305], [250, 305], 3)
				
				dibujarTexto(screen, 'Orden de Expansion', [33, 11], Fuentes['Wendy 30'], COLOR['Verde'])
				dibujarTexto(screen, 'Orden de Expansion', [34, 12], Fuentes['Wendy 30'], COLOR['Verde Claro'])
				
				dibujarTexto(screen, 'Selecciona Las Flechas', [49, 61], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, 'Selecciona Las Flechas', [50, 62], Fuentes['Droid 15'], COLOR['Verde Claro'])
				
				dibujarTexto(screen, 'Cambia El Orden Dando Clic', [29, 161], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, 'Cambia El Orden Dando Clic', [30, 162], Fuentes['Droid 15'], COLOR['Verde Claro'])
				dibujarTexto(screen, 'Izquierdo Sobre Las Flechas.', [29, 181], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, 'Izquierdo Sobre Las Flechas.', [30, 182], Fuentes['Droid 15'], COLOR['Verde Claro'])
				
				screen.blit(FlechaArr.image, (55, 100))
				screen.blit(FlechaDer.image, (95, 100))
				screen.blit(FlechaAba.image, (135, 100))
				screen.blit(FlechaIzq.image, (175, 100))
				
				dibujarTexto(screen, str(Direcciones[0]), [61, 129], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, str(Direcciones[0]), [62, 130], Fuentes['Droid 15'], COLOR['Verde Claro'])
				
				dibujarTexto(screen, str(Direcciones[1]), [101, 129], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, str(Direcciones[1]), [102, 130], Fuentes['Droid 15'], COLOR['Verde Claro'])
				
				dibujarTexto(screen, str(Direcciones[2]), [141, 129], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, str(Direcciones[2]), [142, 130], Fuentes['Droid 15'], COLOR['Verde Claro'])
				
				dibujarTexto(screen, str(Direcciones[3]), [181, 129], Fuentes['Droid 15'], COLOR['Verde'])
				dibujarTexto(screen, str(Direcciones[3]), [182, 130], Fuentes['Droid 15'], COLOR['Verde Claro'])
				
				dibujarTexto(screen, 'Repetir Nodos', [29, 220], Fuentes['Droid 18'], COLOR['Verde Claro'])
				dibujarTexto(screen, 'Repetir Nodos', [30, 221], Fuentes['Droid 18'], COLOR['Verde'])
				
				if BtnRepetirNodos:
					screen.blit(btnON.image, (155, 220))
					NoRepetir = False
				else:
					screen.blit(btnOFF.image, (150, 220))
					NoRepetir = True
				
				dibujarTexto(screen, 'Tipo de Búsqueda:', [29, 250], Fuentes['Droid 18'], COLOR['Verde Claro'])
				dibujarTexto(screen, 'Tipo de Búsqueda:', [30, 251], Fuentes['Droid 18'], COLOR['Verde'])
				
				BtnTipoBusquedaIzq.resize(25,20); screen.blit(BtnTipoBusquedaIzq.image, (30, 277))
				BtnTipoBusquedaDer.resize(25,20); screen.blit(BtnTipoBusquedaDer.image, (185, 277))
				
				if BtnTipoBusqueda == 'Normal':
					
					dibujarTexto(screen, 'Normal', [92, 275], Fuentes['Droid 18'], COLOR['Azul Claro'])
					dibujarTexto(screen, 'Normal', [93, 276], Fuentes['Droid 18'], COLOR['Azul'])
					
				elif BtnTipoBusqueda == 'Backtracking':
					
					dibujarTexto(screen, 'Backtracking', [70, 275], Fuentes['Droid 18'], COLOR['Azul Claro'])
					dibujarTexto(screen, 'Backtracking', [71, 276], Fuentes['Droid 18'], COLOR['Azul'])
					
				elif BtnTipoBusqueda == 'A Estrella':
					
					dibujarTexto(screen, 'A Estrella', [83, 275], Fuentes['Droid 18'], COLOR['Azul Claro'])
					dibujarTexto(screen, 'A Estrella', [84, 276], Fuentes['Droid 18'], COLOR['Azul'])
					
				
				
			else: screen.blit(btnOFF.image, (480, 582))
			
		else: BtnOrdenExpansion = False
		
		if Iniciar:
			if BtnMostrarArbol: screen.blit(btnON.image, (1055, 582))
			else: screen.blit(btnOFF.image, (1050, 582))
			
			#===========================================================
			#======================== Busquedas ========================
			#===========================================================
			
			if seleccion != PuntoDestino:
				
				if TipoBusqueda == 1 and not BtnMostrarArbol:
					
					if not PadreSeleccion in ListaBT: ListaBT.append(PadreSeleccion)
					
					if seleccion in ListaBT:
						Ind = ListaBT.index(seleccion) + 1
						ListaBT = ListaBT[:Ind]
					else:
						if not seleccion in ListaBT: ListaBT.append(seleccion)
					
					ContFPS += 1
					
					if ContFPS % 8 == 1:		# Imprime Cada 0.13 de Segundos, o Sea Cada 8 FPS (Frames Por Segundo)
						
						PadreSeleccion = seleccion
						
						seleccion = Backtracking(XPOS, YPOS, seleccion, ArbolRaiz)
					
					DibujarCaminoBacktracing(screen, XPOS, YPOS, dimension, puntoInicio, seleccion, ListaBT)
					
				# ~ elif TipoBusqueda == 2:
					
					# ~ seleccion = AEstrella(XPOS, YPOS, seleccion, personaje, ArbolRaiz)
				
			else:
				if not BtnMostrarArbol:
					
					ContFPS = 0
					if not seleccion in ListaBT: ListaBT.append(seleccion)
					DibujarCaminoBacktracing(screen, XPOS, YPOS, dimension, puntoInicio, PadreSeleccion, ListaBT)
			
			
		#===================================================================================================
		#===================================================================================================
		#===================================================================================================
		
		pygame.display.flip()		# Actualiza Los Datos En La Interfaz.
		
		clock.tick(60)
		
	pygame.quit()


#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================



if __name__ == "__main__":
	
	main()



