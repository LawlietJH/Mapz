
# Versión: 1.4.5
# Python:  3.5.0

import pygame
from pygame.locals import *
import explorer
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


class Boton(pygame.sprite.Sprite, pygame.font.Font):	# Clase Para Botones ('Cargar Mapa' y 'Comenzar').
	
	def __init__(self, Nombre):		# Pasamos La Ruta de la Imagen a Cargar Como Bloque.
		
		pygame.sprite.Sprite.__init__(self)				# Hereda de la Clase Sprite de pygame.
		self.image = load_image(Nombre, True)			# Carga La Imagen Con la función load_image.
	
	def resize(self, TX, TY):		# Cambia el tamaño de la imagen para cargarla al programa con las medidas necesarias.
		
		self.image = pygame.transform.scale(self.image, (TX, TY))


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
def dibujarMapa(XPOS, YPOS, screen, dimension, p_inicio, tamanio_fuente, Fuentes, SelTemp, Matriz, Lisy, Objetos):
	
	global SELECT, VALORES, seleccion, PuntoInicio, PuntoDestino, DibujarInfo, InfoSelTemp, Error, CadenaError
	
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
				#~ VALORES.append(([LETRAS[i],j+1], Lisy[Pared], 'Pared', Pesos[Pared]))		# Pendiente!!! Agregar Lista de Pesos.
				VALORES.append(([LETRAS[i],j+1], Lisy[Pared], 'Pared', Costos[0]))							# Pendiente!!! Agregar Lista de Pesos.
				
				Objetos['Pared'].resize(DistX, DistY)
				bloque = Objetos['Pared']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Camino]:	# Dibuja el Bloque de Camino.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Camino], 'Camino', Costos[1]))
				
				Objetos['Camino'].resize(DistX, DistY)
				bloque = Objetos['Camino']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Bosque]:	# Dibuja el Bloque de Bosque.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Bosque], 'Bosque', Costos[2]))
				
				Objetos['Bosque'].resize(DistX, DistY)
				bloque = Objetos['Bosque']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Lava]:	# Dibuja el Bloque de Lava.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Lava], 'Lava', Costos[3]))
				
				Objetos['Lava'].resize(DistX, DistY)
				bloque = Objetos['Lava']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Agua]:	# Dibuja el Bloque de Agua.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Agua], 'Agua', Costos[4]))
				
				Objetos['Agua'].resize(DistX, DistY)
				bloque = Objetos['Agua']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Arena]:	# Dibuja el Bloque de Arena.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Arena], 'Arena', Costos[5]))
				
				Objetos['Arena'].resize(DistX, DistY)
				bloque = Objetos['Arena']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Montaña]:	# Dibuja el Bloque de Montaña.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Montaña], 'Montaña', Costos[6]))
				
				Objetos['Montaña'].resize(DistX, DistY)
				bloque = Objetos['Montaña']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Nieve]:	# Dibuja el Bloque de Nieve.
				
				# Agrega los Valores del Bloque en la Posición Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[Montaña], 'Nieve', Costos[7]))
				
				Objetos['Nieve'].resize(DistX, DistY)
				bloque = Objetos['Nieve']
				screen.blit(bloque.image, (x,y))
			
						
			# Dibuja Temporalmente La Selección con el Clic en el Mapa.
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1:
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [x, y, dimension, dimension], 0)
				
				if Iniciar:
					
					DibujarInfo = True
					InfoSelTemp = SelTemp
			
			# Imprime Letra I en Estdo Inicial e Imprimir Letra F Para el Estado Final.
			if   [LETRAS[i],j+1] == PuntoInicio:  dibujarTexto(screen, 'I', [x + (DistX-20), y + (DistY-30)], Fuentes['Droid 30'], COLOR['Rojo'])
			elif [LETRAS[i],j+1] == PuntoDestino: dibujarTexto(screen, 'F', [x + (DistX-20), y + (DistY-30)], Fuentes['Droid 30'], COLOR['Rojo'])
					
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
				
				if not Iniciar and SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1:
					
					if seleccion != SelTemp:
						
						if PuntoInicio == None: PuntoInicio = SelTemp
						elif PuntoDestino == None: PuntoDestino = SelTemp
						else:
							
							if PuntoInicio != None and PuntoDestino != None:
								PuntoInicio = SelTemp
								PuntoDestino = None
								
						seleccion = SelTemp
			
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


def DibujarInformacionClic(screen, Fuentes, SelTemp):
	
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
				dibujarTexto(screen, str(X[3]), [989, PosY-1], Fuentes['Droid 15'], COLOR['Verde Claro'])
				dibujarTexto(screen, str(X[3]), [990, PosY], Fuentes['Droid 15'], COLOR['Verde'])
			
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

def dibujarTexto(screen, texto, posicion, fuente, color):
	
	Texto = fuente.render(texto, 1, color)		# Se Pasa El Texto Con La Fuente Especificada.
	screen.blit(Texto, posicion)				# Se Dibuja En Pantalla El Texto en la Posición Indicada.

#===================================================================================================

def ajustarMedidas(POS, tamanio_fuente):
	
	# Para Imprimir La Matriz:
	MargenX = 300
	MargenY = 10
	
	ancho = int((DIMENCIONES[1] - (tamanio_fuente * 2)) / POS)
	inicio = tamanio_fuente + MargenX, tamanio_fuente + MargenY
	
	return [inicio, ancho]

#===================================================================================================

def obtenerPosicionClic(XPOS, YPOS, mouse, dimension, p_inicio, actual):
	
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

#===================================================================================================

def obtenerPosicion(XPOS, YPOS, Dir, Actual, personaje):
	
	global SELECT, Movimientos, CostoTotal
	
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
						
						break
		
	elif Dir == 'D':
		if   Actual[0] in LETRAS and Actual[1] == YPOS: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(1,YPOS)]:
			y += 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[3] == '': pass
					else:
						
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
						
						break
		
	return Actual

#===================================================================================================

def AbrirArchivo():
	
	global Error, CadenaError
	
	Cadena = ''
	Nombre = explorer.GetFileName()
	
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
	if TextInput == '': dibujarTexto(screen, 'N/A', [X+100, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	else: dibujarTexto(screen, TextInput, [X+100, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	
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
			if len(TI1.split('.')[1]) == 2: pass
			else: TI1 += Add
		else:
			if len(TI1.split('.')[0]) == 4: pass
			else: TI1 += Add
	elif C2:
		if '.' in TI2:
			if len(TI2.split('.')[1]) == 2: pass
			else: TI2 += Add
		else:
			if len(TI2.split('.')[0]) == 4: pass
			else: TI2 += Add
	elif C3:
		if '.' in TI3:
			if len(TI3.split('.')[1]) == 2: pass
			else: TI3 += Add
		else:
			if len(TI3.split('.')[0]) == 4: pass
			else: TI3 += Add
	elif C4:
		if '.' in TI4:
			if len(TI4.split('.')[1]) == 2: pass
			else: TI4 += Add
		else:
			if len(TI4.split('.')[0]) == 4: pass
			else: TI4 += Add
	elif C5:
		if '.' in TI5:
			if len(TI5.split('.')[1]) == 2: pass
			else: TI5 += Add
		else:
			if len(TI5.split('.')[0]) == 4: pass
			else: TI5 += Add
	elif C6:
		if '.' in TI6:
			if len(TI6.split('.')[1]) == 2: pass
			else: TI6 += Add
		else:
			if len(TI6.split('.')[0]) == 4: pass
			else: TI6 += Add
	elif C7:
		if '.' in TI7:
			if len(TI7.split('.')[1]) == 2: pass
			else: TI7 += Add
		else:
			if len(TI7.split('.')[0]) == 4: pass
			else: TI7 += Add
	elif C8:
		if '.' in TI8:
			if len(TI8.split('.')[1]) == 2: pass
			else: TI8 += Add
		else:
			if len(TI8.split('.')[0]) == 4: pass
			else: TI8 += Add
	
	return TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8

#===================================================================================================
#===================================== Declaraciones Globales ======================================
#===================================================================================================

# Constantes Globales: =================================================

COLOR  = {'Blanco':(255, 255, 255), 'Negro':(0,   0,   0),  'Gris Claro':(216, 216, 216), 'Rojo':(255, 0,   0),
		  'Verde':(4,   180, 4),    'Azul':(20,  80,  240), 'Azul Claro':(40,  210, 250), 'Gris':(189, 189, 189),
		  'Fondo':(24,  25,  30),   'Naranja':(255,120,0),  'Seleccion':(220, 200, 0),    'Amarillo':(255,255, 0),
		  'Morado':(76, 11, 95),    'Purpura':(56, 11, 97), 'Verde Claro':(0,   255, 0),  'Rojo Claro':(255, 50, 50)
		 }	# Diccionario de Colores.

DIMENCIONES = (1120, 600)		# Tamaño de La Ventana, Ancho (1120) y Alto (600).
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']	# Letras Para La Matriz.

VALORES   = []		# Lista de Valores para Los Terrenos y Mostrar su Informacion.
SELECT    = []		# Lista de Seleccionados, Contendra: Posiciones Visitadas, Número de Visita.

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
Costos = []				# Lista de los Costos de Cada Tipo de Terreno.
CostoTotal = 0			# Suma Costos en cada Movimiento.
Movimientos = 1

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

#===================================================================================================
#============================================== Main ===============================================
#===================================================================================================

def main():
	
	global SELECT, Movimientos, DibujarInfo, Pagina1, SelectEstados
	global seleccion, PuntoInicio, PuntoDestino, Iniciar, Costos, CostoTotal
	global Error, Error2, CadenaError, CadenaError2
	global Bosque, Camino, Pared, Lava, Agua, Arena, Montaña, Nieve
	
	XPOS = 1			# Variable con la Cantidad de columnas en la Matriz, solo la Inicializamos, para modificar poseteriormente.
	YPOS = 1			# Lo Mismo Con La Anterior pero con Columnas.
	POS  = (XPOS if XPOS > YPOS else YPOS)		# Obtenemos Cual de los 2 es Mayor, para Manipular mejor la Matriz más adelante.
	
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
	
	NP = None					# Numero de Personaje, Posicionamineto en la Lista.
	seleccion = None			# Lista con Las Posiciones, ejemplo [ 'A', 1 ].
	PuntoInicio = None			# Posición de Inicio, ejemplo [ 'A', 1 ].
	SelTemp = ['P',16]			# Selección Temporal.
	
	pygame.init()				# Inicia El Juego.
	
	screen = pygame.display.set_mode(DIMENCIONES)	# Objeto Que Crea La Ventana.
	BGimg = load_image('img/fondo-negro.jpg')		# Carga el Fondo de la Ventana.
	
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
	
	# Incializamos La Lista de Costos Por Terreno
	Costos = [TextInput1, TextInput2, TextInput3, TextInput4, TextInput5, TextInput6, TextInput7, TextInput8]
	
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
			   'Wendy 30':pygame.font.Font("fuentes/Wendy.ttf", 30),
			   'Wendy 25':pygame.font.Font("fuentes/Wendy.ttf", 25),
			   'Droid 30':pygame.font.Font("fuentes/DroidSans.ttf", 30),
			   'Droid 25':pygame.font.Font("fuentes/DroidSans.ttf", 25),
			   'Droid 20':pygame.font.Font("fuentes/DroidSans.ttf", 20),
			   'Droid 15':pygame.font.Font("fuentes/DroidSans.ttf", 15),
			   'Droid 10':pygame.font.Font("fuentes/DroidSans.ttf", 10),
			   'Droid 8':pygame.font.Font("fuentes/DroidSans.ttf", 8),
			   'Droid 7':pygame.font.Font("fuentes/DroidSans.ttf", 7),
			   'Droid 6':pygame.font.Font("fuentes/DroidSans.ttf", 6)
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
	bloque13 = Bloque("img/Texturas/camino.jpg")
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
	botonPers1 = Boton("img/Botones/BotonPurpura.png")
	botonPers2 = Boton("img/Botones/BotonAzul.png")
	
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
	
	NombrePersonaje = ['Hombre','Gato','Lobo','CatBug','Pez','Caricatura','Mujer','Pizza','Mono','Pulpo','Fantasma','Peleador']	# Lista de Personajes.
	
	# Rutas de Imagenes de los Personajes:
	RutaPersonaje = {
					'Hombre':"img/Personajes/Hombre.png",
					'Gato':"img/Personajes/Gato.png",
					'Lobo':"img/Personajes/Lobo.png",
					'CatBug':"img/Personajes/CatBug.png",
					'Pez':"img/Personajes/Pez.png",
					'Caricatura':"img/Personajes/Caricatura.png",
					'Mujer':"img/Personajes/Mujer.png",
					'Pizza':"img/Personajes/Pizza.png",
					'Mono':"img/Personajes/Mono.jpg",
					'Pulpo':"img/Personajes/Pulpo.png",
					'Fantasma':"img/Personajes/Fantasma.png",
					'Peleador':"img/Personajes/Peleador.gif"
					}
	
	# Diccionario Con Objetos Para Mapa:
	Objetos = {'Personaje':personaje, 'Pared':bloque1, 'Camino':bloque3, 'Bosque':bloque4,
			   'Lava':bloque5, 'Agua':bloque6, 'Arena':bloque7, 'Montaña':bloque8, 'Nieve':bloque9}
	
	# Diccionario Con Objetos Para Miniaturas:
	Objetos10 = {'Personaje':personaje, 'Pared':bloque11, 'Camino':bloque13, 'Bosque':bloque14, 'Lava':bloque15,
				 'Agua':bloque16, 'Arena':bloque17, 'Montaña':bloque18, 'Nieve':bloque19}
	
	Input = None
	
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
				if Cargar and Iniciar and seleccion != PuntoDestino:
					
					if   evento.key == pygame.K_LEFT:	seleccion = obtenerPosicion(XPOS, YPOS, 'L', seleccion, personaje)	# Tecla Izquierda. Mueve Personaje.
					elif evento.key == pygame.K_RIGHT:	seleccion = obtenerPosicion(XPOS, YPOS, 'R', seleccion, personaje)	# Tecla Derecha. Mueve Personaje.
					elif evento.key == pygame.K_UP:		seleccion = obtenerPosicion(XPOS, YPOS, 'U', seleccion, personaje)	# Tecla Arriba. Mueve Personaje.
					elif evento.key == pygame.K_DOWN:	seleccion = obtenerPosicion(XPOS, YPOS, 'D', seleccion, personaje)	# Tecla Abajo. Mueve Personaje.
				
				if evento.key == pygame.K_ESCAPE: game_over = True		# Tecla ESC Cierra el Juego.
				
				#======================================================
				if evento.key == pygame.K_BACKSPACE:
					
					if Costo1: TextInput1 = TextInput1[:-1]
					elif Costo2: TextInput2 = TextInput2[:-1]
					elif Costo3: TextInput3 = TextInput3[:-1]
					elif Costo4: TextInput4 = TextInput4[:-1]
					elif Costo5: TextInput5 = TextInput5[:-1]
					elif Costo6: TextInput6 = TextInput6[:-1]
					elif Costo7: TextInput7 = TextInput7[:-1]
					elif Costo8: TextInput8 = TextInput8[:-1]
					
				elif evento.key == pygame.K_PERIOD:
					
					if Costo1:
						if not '.' in TextInput1:
							print(True)
							TextInput1 += '.'
					elif Costo2:
						if not '.' in TextInput2: TextInput2 += '.0'
					elif Costo3:
						if not '.' in TextInput3: TextInput3 += '.0'
					elif Costo4:
						if not '.' in TextInput4: TextInput4 += '.0'
					elif Costo5:
						if not '.' in TextInput5: TextInput5 += '.0'
					elif Costo6:
						if not '.' in TextInput6: TextInput6 += '.0'
					elif Costo7:
						if not '.' in TextInput7: TextInput7 += '.0'
					elif Costo8:
						if not '.' in TextInput8: TextInput8 += '.0'
				
				#=============================================================================================================================================
				# Reducimos el Nombre de las Variables Por Comodidad xD
				TI1, TI2, TI3, TI4 = TextInput1, TextInput2, TextInput3, TextInput4
				TI5, TI6, TI7, TI8 = TextInput5, TextInput6, TextInput7, TextInput8
				C1, C2, C3, C4 = Costo1, Costo2, Costo3, Costo4 
				C5, C6, C7, C8 = Costo5, Costo6, Costo7, Costo8 
				
				# Se Agrega a la Cadena Correspondiente del TextInput Seleccionado, el Número Presionado.
				if   evento.key == pygame.K_0: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('0', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_1: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('1', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_2: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('2', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_3: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('3', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_4: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('4', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_5: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('5', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_6: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('6', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_7: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('7', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_8: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('8', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				elif evento.key == pygame.K_9: TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8 = InputAdd('9', C1, C2, C3, C4, C5, C6, C7, C8, TI1, TI2, TI3, TI4, TI5, TI6, TI7, TI8)
				
				# Pasamos El Valor Correspondiente A Su Variable Oroginal 
				TextInput1, TextInput2, TextInput3, TextInput4 = TI1, TI2, TI3, TI4
				TextInput5, TextInput6, TextInput7, TextInput8 = TI5, TI6, TI7, TI8
				
				# Actualizamos los Datos de los Costos.
				Costos[0] = TextInput1
				Costos[1] = TextInput2
				Costos[2] = TextInput3
				Costos[3] = TextInput4
				Costos[4] = TextInput5
				Costos[5] = TextInput6
				Costos[6] = TextInput7
				Costos[7] = TextInput8
				
				#=============================================================================================================================================
				
				#~ elif evento.key == pygame.K_f:		# Tecla F pondra Pantalla Completa o Normal.
					
					#~ if FULL == False:	
						#~ screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
						#~ FULL = True
					#~ else:
						#~ screen = pygame.display.set_mode(DIMENCIONES)
						#~ FULL = False
			
			#~ elif evento.type == pygame.JOYBUTTONDOWN
			elif evento.type == pygame.MOUSEBUTTONDOWN: #============================== Al Mantener Presionado Cualquier Botón del Mouse. ==============================
				
				# Si se Presiono el Clic Derecho del Mouse (Botón 3) y La Variable Global 'DibujarInfo' esta en True entonces se cambia a false.
				# Dejara de mostrar la Información del Bloque Seleccionado con el Mouse.
				if evento.button == 3 and DibujarInfo: DibujarInfo = False
				else:
					# Si se Presionó cualquier otro Botón del Mouse...
					pos = pygame.mouse.get_pos()	# Obtiene una Tupla con los Valores X y Y del Mouse, en Pixeles.
					
					xr, yr = pos[0], pos[1]		# Posición X y Y del Mouse por separado, Coordenadas por Pixeles.
					
					# Cooredenadas Botón 1 (Cargar Mapa):
					if (xr >= 927) and (xr <= 1077) and (yr >= 24) and (yr <= 56):
						
						Btn1Pressed = True
						CargarMapa = True
						Error2 = False
						CadenaError2 = ''
					
					if Cargar: 			# Si se cargo ya el Mapa.
						
						pygame.mouse.set_visible(False)	# Hacemos Invisible Temporalmente el Cursor del Mouse.
						
						if Pagina1:
							Y = 205
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo1 = True
							else: Costo1 = False
							Y += 70
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo2 = True
							else: Costo2 = False
							Y += 70
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo3 = True
							else: Costo3 = False
							Y += 70
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo4 = True
							else: Costo4 = False
							Y += 70
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo5 = True
							else: Costo5 = False
						else:
							Y = 205
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo6 = True
							else: Costo6 = False
							Y += 70
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo7 = True
							else: Costo7 = False
							Y += 70
							if (xr >= 1010) and (xr <= 1090) and (yr >= Y) and (yr <= Y+20): Costo8 = True
							else: Costo8 = False
						
						if SelectEstados:
							
							SelTemp = seleccion				# Selección temporal, para mostrar el cuadro seleccionado con el mouse.
							SelTemp = obtenerPosicionClic(XPOS, YPOS, pos, dimension, puntoInicio, SelTemp)		# Función Que crea una selección Temporal
						
						#===========================================================================
						
						if (xr >= 950) and (xr <= 1050) and (yr >= 110) and (yr <= 135): Btn2Pressed = True
						if (xr >= 1050) and (xr <= 1075) and (yr >= 550) and (yr <= 570):
							
							if Pagina1: Pagina1 = False
							else: Pagina1 = True
					
						# ================= Cooredenadas Botón Izquierda y Derecha =================
						
						X = 1006; Y = 228
						
						CadenaError = ''
						CadenaError2 = ''
						
						LisyPos1,LisyPos2,LisyPos3,LisyPos4,LisyPos5,LisyPos6,LisyPos7,LisyPos8 = BotonesFlechas(X,Y,xr,yr,Lisy,LisyPos1,LisyPos2,LisyPos3,LisyPos4,LisyPos5,LisyPos6,LisyPos7,LisyPos8)
						
						#=====================================================================================
						
						# Coordenadas Recuadros Personajes 1, 2 y 3 respectivamente:
						Y = 339
						if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers1 = True
						elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers2 = True
						elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers3 = True
						
						Y += 60
						if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers4 = True
						elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers5 = True
						elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers6 = True
						
						Y += 60
						if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers7 = True
						elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers8 = True
						elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers9 = True
						
						Y += 60
						if   (xr >= 29)  and (xr <= 82)  and (yr >= Y) and (yr <= Y+53): seleccionPers10 = True
						elif (xr >= 99)  and (xr <= 152) and (yr >= Y) and (yr <= Y+53): seleccionPers11 = True
						elif (xr >= 169) and (xr <= 222) and (yr >= Y) and (yr <= Y+53): seleccionPers12 = True
					
						#=====================================================================================
				
			elif evento.type == pygame.MOUSEBUTTONUP: #============================== Al Dejar de Presionar Cualquier Botón del Mouse. ==============================
				
				if Btn2Pressed and not Error2:		# Si el Botón 2 (Comenzar) Fue Presionado.
					
					if NP == None:		# Si el Botón 2 Fue Presionado Pero No se ha seleccionado Personaje Marcara Error.
						
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
						seleccion = PuntoInicio
						
						personaje = Personaje(RutaPersonaje[NombrePersonaje[NP]]) # Se Crea el Objeto Personaje de la clase (Personaje),
																				  # Pasandole La Ruta de la Imagen Que se encuentra en el Diccionario (RutaPersonaje),
																				  # Que corresponda al Nombre de Personaje de la lista (NombrePersonaje)
																				  # Que este en la posición del Numero de Personaje Elegido (NP)
						
						if NP == 4 or NP == 8 or NP == 11:	
							
							personaje.flip()				# Acomodamos Al Personaje Mirando a Derecha.
							personaje.setDireccion('R')
							
						Objetos['Personaje'] = personaje		# Se Guarda el Objeto Personaje en el Diccionario.
						
						for val in VALORES:
							if val[0] == PuntoInicio: CostoTotal += float(val[3])
								
						Movimientos += 1
						SELECT.append((seleccion, [Movimientos]))
						
				elif Btn2Pressed and Error2:		# Si el Botón 2 (Comenzar) Fue Presionado y Ocurrio un Error.
					
					CadenaError2 = 'Bloques Aún No Asignados.'
					
				elif CargarMapa:	# Si el Botón 1 Fue Seleccionado y Hay Personaje Seleccionado.
					
					xMatrixy, xLisy, xXPOS, xYPOS, xPOS = TODOArchivo()		# Obtenemos Valores desde la Función Temporalmente.
					
					if Error:		# Si Hubo Error.
					
						Error2 = False
					
					if xMatrixy == None:	# Si los Valores Se Encuentran En Null (None aqui en python) significa que hubo un error.
						
						if Cargar == False: pass		# Si el Valor era False se mantiene.
						else: Cargar = True				# Si el Valor Era None cambia a True.
						CargarMapa = False				# Se Cancela el Cargar el Mapa.
					
					else:	# Si la Matriz tiene informacion, Todo Estuvo Correcto y Validado.
						
						SELECT = []			 	# Se Reinicia La Variable Global SELECT, que guarda el Recorrido para imprimirlo en la Matriz. 
						SelectEstados = False	# Permite Saber Si se Permite Selecciona el Estado Inicial y Final.
						Pagina1 = True		 	# Se Vuelve a Posicionar la Página 1 en la Seleccion de Terrenos para el Mapa.
						DibujarInfo = False  	# Al Cargar Un Nuevo Mapa, Se Deja de Mostrar La Información de Seleccion.
						Iniciar = False		 	# Aun no se permite Iniciar La Partida.
						Cargar = True		 	# Se Dibuja El Mapa.
						
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
						
						puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)	# Se Indica El Punto de Inicio Para Dibujar La Matriz.
						
						# Se Reinicia el Diccionario Objetos con los Nuevos Objetos Generados.
						Objetos = {'Pared':bloque1, 'Camino':bloque3, 'Bosque':bloque4, 'Lava':bloque5, 
								   'Agua':bloque6, 'Arena':bloque7, 'Montaña':bloque8,  'Nieve':bloque9}
						
						Movimientos  = 0
						CostoTotal	 = 0
						PuntoInicio	 = None		# Se Inicializa la Variable Global PuntoInicio en None.
						PuntoDestino = None		# Se Inicializa la Variable Global PuntoDestino en None.
						NP			 = None		# Se Inicializa la Variable personaje en None.
						CargarMapa	 = False	# Indíca que El Botón Cargar Mapa Dejo de ser Apretado.
						Error		 = False	# Indíca Que No Hay Error.
				
				Btn1Pressed = False			# Indica Que El Botón 'Cargar Mapa' Ya No esta Siendo Presionado. 
				Btn2Pressed = False			# Indica Que El Botón 'Comenzar' Ya No esta Siendo Presionado. 
				
				pygame.mouse.set_visible(True)	# Se Hace de Nuevo Visible El Cursor Del Mouse.
				SelTemp = ['P',16]				# La Selección Temporal se manda a un valor jamas cargado en el mapa. (16, 16)
												# Para que deje de mostrarse la selección con el Puntero.
		
		
		
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		#=====================================================================================================================================================
		
		
		screen.blit(BGimg, (0, 0))	# Se Carga La Imagen De Fondo.
		
		
		#===============================================================================================================================
		#======================================== Sección Central ======================================================================
		#===============================================================================================================================
		
		
		
		pygame.draw.rect(screen, COLOR['Fondo'], [puntoInicio[0], puntoInicio[1], dimension*XPOS, dimension*YPOS], 0)
		
		# Si Cargar es Igual a True entonces Dibujara El Mapa.
		if Cargar: dibujarMapa(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, Fuentes, SelTemp, Matrixy, Lisy, Objetos)
		
		
		
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
			
			if NP == None:	# Si Aun No Se Ha Seleccionado Un Personaje.
				
				dibujarTexto(screen, 'Ninguno', [1009, 159], Fuentes['Droid 20'], COLOR['Azul'])
				dibujarTexto(screen, 'Ninguno', [1010, 160], Fuentes['Droid 20'], COLOR['Negro'])
				
			else:			# Si ya fue Seleccionado.
				
				dibujarTexto(screen, NombrePersonaje[NP], [1009, 159], Fuentes['Droid 20'], COLOR['Azul'])
				dibujarTexto(screen, NombrePersonaje[NP], [1010, 160], Fuentes['Droid 20'], COLOR['Negro'])
			
			
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
				
				DibujarMiniaturaTextura(screen, Costo1, TextInput1, Objetos10, BtnIzq1, BtnDer1, 910, Y, 'Pared', Lisy, LisyPos1, Fuentes)
				
					# Bloque 2:	============================================
				
				Y += 70
				
				if LisyPos2 in [LisyPos1] and LisyPos2 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo2, TextInput2, Objetos10, BtnIzq2, BtnDer2, 910, Y, 'Camino', Lisy, LisyPos2, Fuentes, True)
					
				else: DibujarMiniaturaTextura(screen, Costo2, TextInput2, Objetos10, BtnIzq2, BtnDer2, 910, Y, 'Camino', Lisy, LisyPos2, Fuentes)
				
					# Bloque 3:	============================================
				
				Y += 70
				
				if LisyPos3 in [LisyPos1, LisyPos2] and LisyPos3 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo3, TextInput3, Objetos10, BtnIzq3, BtnDer3, 910, Y, 'Bosque', Lisy, LisyPos3, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo3, TextInput3, Objetos10, BtnIzq3, BtnDer3, 910, Y, 'Bosque', Lisy, LisyPos3, Fuentes)
				
					# Bloque 4:	============================================
				
				Y += 70
				
				if LisyPos4 in [LisyPos1, LisyPos2, LisyPos3] and LisyPos4 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo4, TextInput4, Objetos10, BtnIzq4, BtnDer4, 910, Y, 'Lava', Lisy, LisyPos4, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo4, TextInput4, Objetos10, BtnIzq4, BtnDer4, 910, Y, 'Lava', Lisy, LisyPos4, Fuentes)
				
					# Bloque 5:	============================================
				
				Y += 70
				
				if LisyPos5 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4] and LisyPos5 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo5, TextInput5, Objetos10, BtnIzq5, BtnDer5, 910, Y, 'Agua', Lisy, LisyPos5, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo5, TextInput5, Objetos10, BtnIzq5, BtnDer5, 910, Y, 'Agua', Lisy, LisyPos5, Fuentes)
				
			else:
					# Bloque 6:	============================================
				
				Y = 190
				
				if LisyPos6 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5] and LisyPos6 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava, Agua)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo6, TextInput6, Objetos10, BtnIzq6, BtnDer6, 910, Y, 'Arena', Lisy, LisyPos6, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo6, TextInput6, Objetos10, BtnIzq6, BtnDer6, 910, Y, 'Arena', Lisy, LisyPos6, Fuentes)
				
					# Bloque 7:	============================================
				
				Y += 70
				
				if LisyPos7 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6] and LisyPos7 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava, Agua, Arena)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo7, TextInput7, Objetos10, BtnIzq7, BtnDer7, 910, Y, 'Montaña', Lisy, LisyPos7, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo7, TextInput7, Objetos10, BtnIzq7, BtnDer7, 910, Y, 'Montaña', Lisy, LisyPos7, Fuentes)
				
					# Bloque 8:	============================================
				
				Y += 70
				
				if LisyPos8 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5, LisyPos6, LisyPos7] and LisyPos8 != 0:
					# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Bosque, Lava, Agua, Arena, Montaña)
					
					# Dibuja La Asignación En Rojo Por Estar Repetido El Valor.
					DibujarMiniaturaTextura(screen, Costo8, TextInput8, Objetos10, BtnIzq8, BtnDer8, 910, Y, 'Nieve', Lisy, LisyPos8, Fuentes, True)
				
				else: DibujarMiniaturaTextura(screen, Costo8, TextInput8, Objetos10, BtnIzq8, BtnDer8, 910, Y, 'Nieve', Lisy, LisyPos8, Fuentes)
				
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
		
		if NP == None:	# Si Aun No Se Ha Seleccionado Un Personaje.
			
			dibujarTexto(screen, 'Seleccionar', [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen, 'Seleccionar', [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
			
		else:			# Si ya fue Seleccionado.
			
			dibujarTexto(screen,  NombrePersonaje[NP], [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen,  NombrePersonaje[NP], [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
		
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
		
		if Cargar and not Iniciar:
			
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
				NP = 0						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers2:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers2 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 1						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers3:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers3 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 2						# Se Asigna a NP el Numero De Personaje.
			
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
				NP = 3						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers5:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers5 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 4						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers6:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers6 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 5					# Se Asigna a NP el Numero De Personaje.
			
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
				NP = 6						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers8:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers8 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 7						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers9:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers9 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 8					# Se Asigna a NP el Numero De Personaje.
			
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
				NP = 9						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers11:		# Si El Personaje 2 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers11 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 10						# Se Asigna a NP el Numero De Personaje.
				
			elif seleccionPers12:		# Si El Personaje 3 Fue Seleccionado
				
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, Y, 51, 51], 0)		# Se Muestra el Recuadro de Selección (Color Amarillento) Temporalmente.
				
				seleccionPers12 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
				NP = 11					# Se Asigna a NP el Numero De Personaje.
			
			Y += 70
			pygame.draw.line(screen, COLOR['Negro'],  [9, Y], [250,  Y], 3)
			
		if seleccion == PuntoDestino and Iniciar:
			
			Y += 100
			dibujarTexto(screen, 'Mapa Finalizado!', [16, Y-1], Fuentes['Droid 30'], COLOR['Negro'])
			dibujarTexto(screen, 'Mapa Finalizado!', [17, Y],   Fuentes['Droid 30'], COLOR['Rojo'])
			
		#===================================================================================================
		
		pygame.display.flip()		# Actualiza Los Datos En La Interfaz.
		
		clock.tick(60)
		
	pygame.quit()


#=============================================================================================================================================================
#=============================================================================================================================================================
#=============================================================================================================================================================



if __name__ == "__main__":
	
	main()


