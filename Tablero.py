
# Version: 1.2.9

import pygame
import pygame_textinput
from pygame.locals import *
import explorer
import sys, os

COLOR  = {'Blanco':(255, 255, 255), 'Negro':(0,   0,   0),  'Gris Claro':(216, 216, 216), 'Rojo':(255, 0,   0),
		  'Verde':(4,   180, 4),    'Azul':(20,  80,  240), 'Azul Claro':(40,  210, 250), 'Gris':(189, 189, 189),
		  'Fondo':(24,  25,  30),   'Naranja':(255,120,0),  'Seleccion':(220, 200, 0),    'Amarillo':(255,255, 0),
		  'Morado':(76, 11, 95),    'Purpura':(56, 11, 97), 'Verde Claro':(0,   255, 0)
		 }

DIMENCIONES = (1120, 600)
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

VALORES = []
SELECT = []
POSBLANCO = []
POSAZUL = []

#===================================================================================================
#===================================================================================================
#===================================================================================================

#Clases 
 
class Personaje(pygame.sprite.Sprite, pygame.font.Font):
	
	def __init__(self, Nombre):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(Nombre, True)
		self.image = pygame.transform.flip(self.image, True, False)
		self.direccion = 'R'
		
	
	def resize(self, TX, TY):
		
		self.image = pygame.transform.scale(self.image, (TX, TY))
	
	def flip(self, TX, TY=False):
		
		self.image = pygame.transform.flip(self.image, TX, TY)
	
	def setDireccion(self, direccion): self.direccion = direccion
	
	def getDireccion(self): return self.direccion


class Bloque(pygame.sprite.Sprite, pygame.font.Font):
	
	def __init__(self, Nombre):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(Nombre, True)
	
	def resize(self, TX, TY):
		
		self.image = pygame.transform.scale(self.image, (TX, TY))


class Boton(pygame.sprite.Sprite, pygame.font.Font):
	
	def __init__(self, Nombre):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(Nombre, True)
	
	def resize(self, TX, TY):
		
		self.image = pygame.transform.scale(self.image, (TX, TY))


class BotonDir(pygame.sprite.Sprite, pygame.font.Font):
	
	def __init__(self, Nombre):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(Nombre, True)
	
	def resize(self, TX, TY):
		
		self.image = pygame.transform.scale(self.image, (TX, TY))
	
	def flip(self, TX, TY=False):
		
		self.image = pygame.transform.flip(self.image, TX, TY)
	

#===================================================================================================
#===================================================================================================
#===================================================================================================


def dibujarMapa(XPOS, YPOS, screen, dimension, p_inicio, tamanio_fuente, Fuentes, seleccion, SelTemp, Matriz, Lisy, Objetos):
	
	global SELECT, VALORES
	
	'''
	# Funcion que dibuja el tablero
	XPOS:			Cantidad de Columnas (Letras)
	YPOS:			Cantidad de Fila (Numeros)
	screen: 		Objeto Principal, Referencia a la Vantana Para Dibujar en ella.
	dimension: 		Tamanio de Los Rectangulos. (Tamanio de los Terrenos en Pixeles)
	p_inicio: 		Coordenadas en Pixeles del Punto de Inicio del Mapa a Dibujar en La Ventana.
	tamanio_fuente: Tamanio de fuente para las letras y numeros de la matriz. (Margen)
	Fuentes: 		Diccionario con Fuentes de Letras.
	seleccion: 		Posicion del Personaje.
	SelTemp: 		Posicion de Seleccion Temporal Al Dar Clic.
	Matriz:			Matriz con los valores Cargados del Archivo.txt
	Lisy			Lista con los valores Ordenados y sin Repetir, Cargados del Archivo.txt
	Objetos:		Diccionario con los Objetos tipo Bloque Para Dibujarlos En La Pantalla, en su posicion correspondiente.
	'''
	
	VALORES = []
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]		# Se Obtiene La Posicion X en Pixeles, del Bloque Matriz[j][i]
			y = j * dimension + p_inicio[1]		# Se Obtiene La Posicion Y en Pixeles, del Bloque Matriz[j][i]
			
			xp = (i+1) * dimension + p_inicio[0]	# Se Obtiene La Posicion siguiente de X en Pixeles, del Bloque Matriz[j][i+1]
			yp = (j+1) * dimension + p_inicio[1]	# Se Obtiene La Posicion siguiente de Y en Pixeles, del Bloque Matriz[j+1][i]
			
			DistX = xp - x		# Se Calcula La Distancia en Pixeles en X desde la Posicion Matriz[i][j] hasta Matriz[i+1][j]
			DistY = yp - y		# Se Calcula La Distancia en Pixeles en Y desde la Posicion Matriz[i][j] hasta Matriz[i][j+1]
			
			if Matriz[j][i] == '-1':	# Dibuja el Bloque Vacio.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], 'N/A', 'N/A'))
				
				Objetos['N/A'].resize(DistX, DistY)
				bloque = Objetos['N/A']
				screen.blit(bloque.image, (x,y))
			
			elif Matriz[j][i] == Lisy[Pared]:	# Dibuja el Bloque de Pared.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[0], 'Pared'))
				
				Objetos['Pared'].resize(DistX, DistY)
				bloque = Objetos['Pared']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Camino]:	# Dibuja el Bloque de Camino.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[1], 'Camino'))
				
				Objetos['Camino'].resize(DistX, DistY)
				bloque = Objetos['Camino']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Pasto]:	# Dibuja el Bloque de Pasto.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Pasto'))
				
				Objetos['Pasto'].resize(DistX, DistY)
				bloque = Objetos['Pasto']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Lava]:	# Dibuja el Bloque de Lava.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Lava'))
				
				Objetos['Lava'].resize(DistX, DistY)
				bloque = Objetos['Lava']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Agua]:	# Dibuja el Bloque de Agua.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Agua'))
				
				Objetos['Agua'].resize(DistX, DistY)
				bloque = Objetos['Agua']
				screen.blit(bloque.image, (x,y))
				
			else:	# Dibuja el Bloque Vacio.
				
				# Agrega los Valores del Bloque en la Posicion Matriz[j][i] a la Lista Global 'VALORES'.
				VALORES.append(([LETRAS[i],j+1], 'N/A', 'N/A'))
				
				Objetos['N/A'].resize(DistX, DistY)
				bloque = Objetos['N/A']
				screen.blit(bloque.image, (x,y))
				
			if seleccion[0] == LETRAS[i] and j == seleccion[1] - 1 and Iniciar:
				
				# Dibuja el Personaje Seleccionado.
				Objetos['Personaje'].resize(DistX, DistY)
				personaje = Objetos['Personaje']
				screen.blit(personaje.image, (x, y))
				
				# Si la coordenada no esta en la lista, se aniade al registro de Recorrido:
				if not seleccion in SELECT: SELECT.append(seleccion)
				
			# Dibuja Temporalmente La Seleccion con el Clic en el Mapa.
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1: pygame.draw.rect(screen, COLOR['Seleccion'], [x, y, dimension, dimension], 0)
			
			# Imprimir El Recorrido:
			#~ if [LETRAS[i],j+1] in SELECT:
				
				#~ dibujarTexto(screen, str(SELECT.index([LETRAS[i],j+1]) + 1), [x+1, y], Fuentes['Droid 10'], COLOR['Rojo'])
			
			# Dibuja Los Numeros En Y
			if i == 0:
				
				dibujarTexto(screen, str(j + 1), 
				[p_inicio[0] - tamanio_fuente, j * dimension + p_inicio[1] + ((DistY // 2) - (tamanio_fuente//2))], 
				Fuentes['Alice 30'], 
				COLOR['Azul'])
			
		# Dibuja Las Letras En X
		dibujarTexto(screen, LETRAS[i], 
		[i * dimension + p_inicio[0] + ((DistX // 2) - 7), p_inicio[1] - tamanio_fuente], 
		Fuentes['Alice 30'], COLOR['Azul'])

#===================================================================================================

def dibujarTexto(screen, texto, posicion, fuentes, color):
	
	Texto = fuentes.render(texto, 1, color)
	screen.blit(Texto, posicion)

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
	
	PosLetra = LETRAS.index(Actual[0])
	
	x, y = PosLetra, Actual[1]
	
	if Dir == 'U':
		if   Actual[0] in LETRAS and Actual[1] == 1: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(2,YPOS+1)]:
			y -= 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[2] == 'Pared': pass
					else: Actual = [Actual[0],Actual[1]-1]
		
	elif Dir == 'D':
		if   Actual[0] in LETRAS and Actual[1] == YPOS: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(1,YPOS)]:
			y += 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[2] == 'Pared': pass
					else: Actual = [Actual[0],Actual[1]+1]
		
	elif Dir == 'L':
		
		if personaje.getDireccion() == 'R':
			
			personaje.flip(True)
			personaje.setDireccion('L')
			
		if   Actual[0] == LETRAS[0]  and Actual[1] in [x for x in range(1,YPOS+1)]:	pass
		elif Actual[0] in LETRAS[1:] and Actual[1] in [x for x in range(1,YPOS+1)]:
			x -= 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[2] == 'Pared': pass
					else: Actual = [LETRAS[PosLetra-1],Actual[1]]
		
	elif Dir == 'R':
		
		if personaje.getDireccion() == 'L':
			
			personaje.flip(True)
			personaje.setDireccion('R')
			
		if   Actual[0] == LETRAS[XPOS-1]   and Actual[1] in [x for x in range(1,YPOS+1)]: pass
		elif Actual[0] in LETRAS[0:XPOS-1] and Actual[1] in [x for x in range(1,YPOS+1)]:
			x += 1
			for z in VALORES:
				if z[0] == [LETRAS[x],y]:
					if z[2] == 'Pared': pass
					else: Actual = [LETRAS[PosLetra+1],Actual[1]]
	
	return Actual

#===================================================================================================

def AbrirArchivo():
	
	global Error, CadenaError
	
	Cadena = ''
	Nombre = explorer.GetFileName()
	
	if Nombre == None:
		
		CadenaError = 'Archivo No Especificado'
		Error = True
		return None
	
	with open(Nombre, 'r') as Archivo: Cadena = Archivo.read()
	Archivo.close()
	
	return Cadena

#===================================================================================================

def ObtenerMatriz(Cadena):
	
	global Error, CadenaError
	
	if Cadena == '':
		
		CadenaError = '    Error! Archivo Vacio'
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
		
		CadenaError = ' Archivo No Compatible'
		Error = True
		return None, None, None, None, None
		
	elif Matrixy == False:
		
		CadenaError = ' Archivo No Compatible'
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
		
		CadenaError = ' Cuadricula Minima: 2x2'
		Error = True
		return None, None, None, None, None
		
	elif XPOS >= 16 or YPOS >= 16:
		
		CadenaError = 'Cuadricula Maxima: 15x15'
		Error = True
		return None, None, None, None, None
	
	return Matrixy, Lisy, XPOS, YPOS, POS


def DibujarMiniaturaTextura(screen, Objetos, BtnIzq, BtnDer, X, Y, Nombre, List, LisyPosX, Fuentes, Repetido=False):
	
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
	dibujarTexto(screen, 'Valor: ', [X+40, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	
	# Dibuja Los Botones Izquierda y Derecha Para Cambiar Valores.
	BtnIzq.resize(25,20); screen.blit(BtnIzq.image, (X+96, Y+18))
	BtnDer.resize(25,20); screen.blit(BtnDer.image, (X+146, Y+18))
	
	# Dibuja El Numero De Terreno Que se Le Sera Asignado.
	if Repetido: dibujarTexto(screen, str(List[LisyPosX]), [X+125, Y+15], Fuentes['Droid 20'], COLOR['Rojo'])
	else: dibujarTexto(screen, str(List[LisyPosX]), [X+125, Y+15], Fuentes['Droid 20'], COLOR['Negro'])
	

def BotonesFlechas(X, Y, xr, yr, Lisy, LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5):
	
	# Miniatura Bloque Pared:
	if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
		if LisyPos1 > 0 and LisyPos1 < len(Lisy): LisyPos1 -= 1
	elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
		if LisyPos1 >= 0 and LisyPos1 < len(Lisy)-1: LisyPos1 += 1

	# Miniatura Bloque Camino:
	Y += 50
	if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
		if LisyPos2 > 0 and LisyPos2 < len(Lisy): LisyPos2 -= 1
	elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
		if LisyPos2 >= 0 and LisyPos2 < len(Lisy)-1: LisyPos2 += 1

	# Miniatua Bloque Pasto:
	Y += 50
	if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
		if LisyPos3 > 0 and LisyPos3 < len(Lisy): LisyPos3 -= 1
	elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
		if LisyPos3 >= 0 and LisyPos3 < len(Lisy)-1: LisyPos3 += 1

	# Miniatua Bloque Lava:
	Y += 50
	if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
		if LisyPos4 > 0 and LisyPos4 < len(Lisy): LisyPos4 -= 1
	elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
		if LisyPos4 >= 0 and LisyPos4 < len(Lisy)-1: LisyPos4 += 1

	# Miniatua Bloque Agua:
	Y += 50
	if (xr >= X) and (xr <= X+25) and (yr >= Y) and (yr <= Y+20):
		if LisyPos5 > 0 and LisyPos5 < len(Lisy): LisyPos5 -= 1
	elif (xr >= X+50) and (xr <= X+75) and (yr >= Y) and (yr <= Y+20):
		if LisyPos5 >= 0 and LisyPos5 < len(Lisy)-1: LisyPos5 += 1
	
	return LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5
	
	
#===================================================================================================


Error = False
CadenaError = ''

Iniciar = False

NA = 0
Pared = 0
Camino = 0
Pasto = 0
Lava = 0
Agua = 0


#===================================================================================================

def main():
	
	global Error, CadenaError, Iniciar, Pasto, Camino, Pared, Lava, Agua
	
	XPOS = 1			# Variable con la Cantidad de columnas en la Matriz, solo la Inicializamos, para modificar poseteriormente.
	YPOS = 1			# Lo Mismo Con La Anterior pero con Columnas.
	POS  = (XPOS if XPOS > YPOS else YPOS)		# Obtenemos Cual de los 2 es Mayor, para Manipular mejor la Matriz más adelante.
	
	Lisy = ['-1']		# Lista de Terrenos, -1 igual al Terreno Vacio
	LisyPos1 = 0		# Para Terreno Tipo Pared
	LisyPos2 = 0		# Para Terreno Tipo Camino
	LisyPos3 = 0		# Para Terreno Tipo Pasto
	LisyPos4 = 0		# Para Terreno Tipo Lava
	LisyPos5 = 0		# Para Terreno Tipo Agua
	
	CargarMapa = None		# Variable Booleana Para Hacer Validaciones al Cargar Mapa.
	CargarPers = False		# Variable Booleana Para Hacer Validaciones al Cargar Un Personaje.
	FULL = False			# Variable Booleana Para Hacer Pantalla Completa.
	Cargar = False			# Variable Booleana Para Hacer Validaciones al Dibujar El Tablero.
	
	NP = None					# Numero de Personaje, Posicionamineto en la Lista.
	seleccion = None			# Lista con Las Posiciones, ejemplo [ 'A', 1 ].
	seleccionPers1 = None		# Para Saber Si El Personaje 1 Fue Seleccionado.
	seleccionPers2 = None		# Para Saber Si El Personaje 2 Fue Seleccionado.
	seleccionPers3 = None		# Para Saber Si El Personaje 3 Fue Seleccionado.
	SelTemp = ['P',16]
	NombrePersonaje = ['Hombre','Gato','Fantasma']	# Lista de Personajes.
	
	pygame.init()				# Inicia El Juego.
	
	screen = pygame.display.set_mode(DIMENCIONES)	# Objeto Que Crea La Ventana.
	BGimg = load_image('img/fondo-negro.jpg')		# Carga el Fondo de la Ventana.
	
	pygame.display.set_caption("Laberinto")			# Titulo de la Ventana del Juego.
	game_over = False								# Variable Que Permite indicar si se termino el juego o no.
	clock = pygame.time.Clock()						# Obtiener El Tiempo para pasar la cantidad de FPS más adelante.
	tamanio_fuente = 30				# Constante, para hacer manipulacion del tamaño de algunas letras y en la matriz
									# para tener un margen correcto y otras cosas más.
	
	#~ textinput = pygame_textinput.TextInput()
	
	#===================================================================
	
	# Fuentes de Letra:
	
	Fuentes = {
			   'Alice 30':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 30),
			   'Wendy 30':pygame.font.Font("fuentes/Wendy.ttf", 30),
			   'Wendy 25':pygame.font.Font("fuentes/Wendy.ttf", 25),
			   'Droid 30':pygame.font.Font("fuentes/DroidSans.ttf", 30),
			   'Droid 20':pygame.font.Font("fuentes/DroidSans.ttf", 20),
			   'Droid 15':pygame.font.Font("fuentes/DroidSans.ttf", 15),
			   'Droid 10':pygame.font.Font("fuentes/DroidSans.ttf", 10)
			   }
	
	#===================================================================
	
	puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
	
	# Objetos:
	
	#Objetos Para El Mapa:
	personaje = None						# Inicializamos la variable objeto para el futuro personaje a elegir.
	bloque1 = Bloque("img/Bloque1.png")		# Objeto Pared.
	bloque2 = Bloque("img/N-A.jpg")			# Objeto Vacio.
	bloque3 = Bloque("img/camino.jpg")		# Objeto Camino.
	bloque4 = Bloque("img/pasto.jpg")		# Objeto Pasto.
	bloque5 = Bloque("img/Lava Cracks.jpg")	# Objeto Lava.
	bloque6 = Bloque("img/Agua.jpg")		# Objeto Agua.
	
	# Miniaturas para eleccion de Terrenos para el Mapa:
	bloque11 = Bloque("img/Bloque1.png")
	bloque12 = Bloque("img/N-A.jpg")
	bloque13 = Bloque("img/camino.jpg")
	bloque14 = Bloque("img/pasto.jpg")
	bloque15 = Bloque("img/Lava Cracks.jpg")
	bloque16 = Bloque("img/Agua.jpg")
	
	# Boton Cargar Mapa:
	boton1 = Boton("img/BotonRojo.png")
	boton2 = Boton("img/BotonNaranja.png")
	
	# Boton Comezar:
	botonPers1 = Boton("img/BotonPurpura.png")
	botonPers2 = Boton("img/BotonAzul.png")
	
	# Botones Con Flechas Izquierda y Derecha Para Eleccion de Terrenos.
	# La funcion flip() Invierte la Imagen en Espejo.  
	BtnIzq1 = BotonDir("img/BotonIzq.png")							# Boton Izquierda Para Eleccion de Pared.
	BtnDer1 = BotonDir("img/BotonIzq.png"); BtnDer1.flip(True)		# Boton Derecha   Para Eleccion de Pared. ====
	BtnIzq2 = BotonDir("img/BotonIzq.png")							# Boton Izquierda Para Eleccion de Camino.
	BtnDer2 = BotonDir("img/BotonIzq.png"); BtnDer2.flip(True)		# Boton Derecha   Para Eleccion de Camino. ===
	BtnIzq3 = BotonDir("img/BotonIzq.png")							# Boton Izquierda Para Eleccion de Pasto. 
	BtnDer3 = BotonDir("img/BotonIzq.png"); BtnDer3.flip(True)		# Boton Derecha   Para Eleccion de Pasto. ====
	BtnIzq4 = BotonDir("img/BotonIzq.png")							# Boton Izquierda Para Eleccion de Lava.
	BtnDer4 = BotonDir("img/BotonIzq.png"); BtnDer4.flip(True)		# Boton Derecha   Para Eleccion de Lava. =====
	BtnIzq5 = BotonDir("img/BotonIzq.png")							# Boton Izquierda Para Eleccion de Agua.
	BtnDer5 = BotonDir("img/BotonIzq.png"); BtnDer5.flip(True)		# Boton Derecha   Para Eleccion de Agua. =====
	
	Cuadro1 = Personaje("img/personaje.gif")	# Miniatura Para Personaje Hombre.
	Cuadro2 = Personaje("img/CatBug.png")		# Miniatura Para Personaje Gato.
	Cuadro3 = Personaje("img/SinRostro.png")	# Miniatura Para Personaje Fantasma.
	
	# Rutas de Imagenes de los Personajes:
	RutaPersonaje = {
					'Hombre':"img/personaje.gif",
					'Gato':"img/CatBug.png",
					'Fantasma':"img/SinRostro.png"
					}
	
	# Diccionario Con Objetos Para Mapa:
	Objetos = {'Personaje':personaje, 'Pared':bloque1, 'N/A':bloque2, 'Camino':bloque3, 'Pasto':bloque4,
			   'Lava':bloque5, 'Agua':bloque6}
	
	# Diccionario Con Objetos Para Miniaturas:
	Objetos10 = {'Personaje':personaje, 'Pared':bloque11, 'N/A':bloque12, 'Camino':bloque13, 'Pasto':bloque14,
				 'Lava':bloque15, 'Agua':bloque16}
	
	#===================================================================
	
	# Booleanos Para Saber Si Los Botones Fueron Presionados:
	Btn1Pressed = False
	Btn2Pressed = False
	
	#===================================================================
	
	# Inicio Del Juego:
	while game_over is False:
		
		#~ MousePos = pygame.mouse.get_pos()
		
		#=====================================================================================================
		#=====================================================================================================
		#=====================================================================================================
		
		# Chequeo Constante de Eventos del Teclado:
		for evento in pygame.event.get():
			
			#~ textinput.update(pygame.event.get())
		
			if evento.type == pygame.QUIT: game_over = True		# Si Se Presiona El Boton Cerrar, Cerrara El Juego.
			
			elif evento.type == pygame.KEYDOWN:		# Manipulacion del Teclado.
				
				if Cargar and Iniciar:		# Si Ya Fue Cargado El Tablero y Se PResiono Iniciar.
					
					if   evento.key == pygame.K_LEFT:	seleccion = obtenerPosicion(XPOS, YPOS, 'L', seleccion, personaje)	# Tecla Izquierda. Mueve Personaje.
					elif evento.key == pygame.K_RIGHT:	seleccion = obtenerPosicion(XPOS, YPOS, 'R', seleccion, personaje)	# Tecla Derecha. Mueve Personaje.
					elif evento.key == pygame.K_UP:		seleccion = obtenerPosicion(XPOS, YPOS, 'U', seleccion, personaje)	# Tecla Arriba. Mueve Personaje.
					elif evento.key == pygame.K_DOWN:	seleccion = obtenerPosicion(XPOS, YPOS, 'D', seleccion, personaje)	# Tecla Abajo. Mueve Personaje.
			
				if evento.key == pygame.K_ESCAPE: game_over = True		# Tecla ESC Cierra el Juego.
				
				#~ elif evento.key == pygame.K_f:		# Tecla F pondra Pantalla Completa o Normal.
					
					#~ if FULL == False:	
						#~ screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
						#~ FULL = True
					#~ else:
						#~ screen = pygame.display.set_mode(DIMENCIONES)
						#~ FULL = False
			
			#~ elif evento.type == pygame.JOYBUTTONDOWN
			elif evento.type == pygame.MOUSEBUTTONDOWN: #============================== Al Mantener Presionado Cualquier Boton del Mouse. ==============================
				
				pos = pygame.mouse.get_pos()	# Obtiene una Tupla con los Valores X y Y del Mouse, en Pixeles.
				pygame.mouse.set_visible(False)	# Hacemos Invisible Temporalmente el Cursor del Mouse.
				SelTemp = seleccion				# Seleccion temporal, para mostrar el cuadro seleccionado con el mouse.
				
				SelTemp = obtenerPosicionClic(XPOS, YPOS, pos, dimension, puntoInicio, SelTemp)		# Funcion Que crea una seleccion Temporal
				
				xr, yr = pos[0], pos[1]		# Posicion X y Y del Mouse por separado, Coordenadas por Pixeles.
				
				# Cooredenadas Boton 1:
				if (xr >= 927) and (xr <= 1077) and (yr >= 44) and (yr <= 80):  Btn1Pressed = True; CargarMapa = True
				
				# Cooredenadas Boton 2:
				if Cargar: 				# Solo Se Puede Presionar el Boton si se cargo ya el Mapa
					if (xr >= 950) and (xr <= 1050) and (yr >= 555) and (yr <= 580): Btn2Pressed = True
				
				# ================= Cooredenadas Boton Izquierda y Derecha =================
				
				if Cargar:		# Si se cargo el Mapa Permite Presionar los Botones de Flechas.
					
					X = 1006; Y = 168
					
					LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5 = BotonesFlechas(X, Y, xr, yr, Lisy, LisyPos1, LisyPos2, LisyPos3, LisyPos4, LisyPos5)
					
				#=====================================================================================
				
				# Coordenadas Recuadros Personajes 1, 2 y 3 respectivamente:
				if   (xr >= 29)  and (xr <= 82)  and (yr >= 199) and (yr <= 252): seleccionPers1 = True
				elif (xr >= 99)  and (xr <= 152) and (yr >= 199) and (yr <= 252): seleccionPers2 = True
				elif (xr >= 169) and (xr <= 222) and (yr >= 199) and (yr <= 252): seleccionPers3 = True
				
				
				
			elif evento.type == pygame.MOUSEBUTTONUP: #============================== Al Dejar de Presionar Cualquier Boton del Mouse. ==============================
				
				#=======================================================
				
				if Btn2Pressed:		# Si el Boton 2 Fue Presionado
					
					Iniciar = True	# Inicia El Juego.
					
				elif Btn1Pressed and NP == None:	# Si el Boton 1 Fue Presionado Pero No se ha seleccionado Personaje.
					
					Error = True
					CadenaError = 'Selecciona Un Personaje'
					CargarMapa = False
					
				elif CargarMapa:		# Si el Boton 1 Fue Seleccionado y Hay Personaje Seleccionado.
					
					xMatrixy, xLisy, xXPOS, xYPOS, xPOS = TODOArchivo()		# Obtenemos Valores desde la Funcion Temporalmente.
					
					if xMatrixy == None:		# Si los Valores Se Encuentran En Null (None aqui en python) significa que hubo un error.
						
						if Cargar == False: pass		# Si el Valor era False se mantiene.
						else: Cargar = True				# Si el Valor Era None cambia a True.
						CargarMapa = False				# Se Cancela el Cargar el Mapa.
					
					else:	# Si la Matriz tiene informacion, Todo Estuvo Correcto y Validado.
						
						global SELECT
						SELECT = []		# Se Reinicia La Variable Global SELECT, que guarda el Recorrido para imprimirlo en la Matriz. 
						
						Iniciar = False	# Aun no se permite Iniciar La Partida.
						Cargar = True	# Se Dibuja El Mapa.
						
						personaje = Personaje(RutaPersonaje[NombrePersonaje[NP]]) # Se Crea el Objeto Personaje de la clase (Personaje),
																				  # Pasandole La Ruta de la Imagen Que se encuentra en el Diccionario (RutaPersonaje),
																				  # Que corresponda al Nombre de Personaje de la lista (NombrePersonaje)
																				  # Que este en la posicion del Numero de Personaje Elegido (NP)
						
						# Se Crean Nuevos Objetos Bloque para el nuevo Mapa.
						bloque1 = Bloque("img/Bloque1.png")		# Objeto Pared.
						bloque2 = Bloque("img/N-A.jpg")			# Objeto Vacio.
						bloque3 = Bloque("img/camino.jpg")		# Objeto Camino.
						bloque4 = Bloque("img/pasto.jpg")		# Objeto Pasto.
						bloque5 = Bloque("img/Lava Cracks.jpg")	# Objeto Lava.
						bloque6 = Bloque("img/Agua.jpg")		# Objeto Agua.
						
						# Se Pasan los valores Temporales a los Originales.
						Matrixy = xMatrixy			
						Lisy = ['-1']
						Lisy = Lisy + xLisy
						
						# Se Reinician Las Variables Globales (Pared, Camino, Pasto, Lava, Agua) en 0
						# Se Reinician Las Variables De Posicion Para la Seleccion de Terrenos en 0
						Pared  = LisyPos1 = 0
						Camino = LisyPos2 = 0
						Pasto  = LisyPos3 = 0
						Lava   = LisyPos4 = 0
						Agua   = LisyPos5 = 0
						
						# Obtenemos El Ancho y Alto del Mapa, Para Cargar La Matriz Correctamente.
						XPOS = xXPOS		# Valor de las Letras.
						YPOS = xYPOS		# Valor de las Numeros.
						POS = xPOS			# Obtenemos Cual es el Mas grande de Los 2.
						
						puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)	# Se Indica El Punto de Inicio Para Dibujar La Matriz.
						
						# Se Reinicia el Diccionario Objetos con los Nuevos Objetos Generados.
						Objetos = {'Personaje':personaje, 'Pared':bloque1, 'N/A':bloque2, 'Camino':bloque3, 'Pasto':bloque4,
								   'Lava':bloque5, 'Agua':bloque6}
						
						seleccion = ['A', 1] 	# En esta Posicion Iniciara El Personaje Una Vez Cargado.
						CargarMapa = False		# Indica que El Boton Cargar Mapa Dejo de ser Apretado.
						Error = False			# Indica Que No Hay Error.
				
				#=======================================================
				
				Btn1Pressed = False			# Indica Que El Boton 'Cargar Mapa' Ya No esta Siendo Presionado. 
				Btn2Pressed = False			# Indica Que El Boton 'Comenzar' Ya No esta Siendo Presionado. 
				
				pygame.mouse.set_visible(True)		# Se Hace de Nuevo Visible El Cursor Del Mouse.
				SelTemp = ['P',16]			# La Seleccion Temporal se manda a un valor jamas cargado en el mapa. (16, 16)
											# Para que deje de mostrarse la seleccion con el Puntero.
		
		#=====================================================================================================
		#=====================================================================================================
		#=====================================================================================================
		
		screen.blit(BGimg, (0, 0))		# Se Carga La Imagen De Fondo.
		
		#======================================== Seccion Central ========================================
		
		if Cargar: # Si Cargar es Igual a True entonces Dibujara El Mapa.
			
			dibujarMapa(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, Fuentes, seleccion, SelTemp, Matrixy, Lisy, Objetos)
			
		else: # Si no, Dibujara solo un rectangulo en trasfondo para representar que ahi se dibujara el Mapa.
			
			pygame.draw.rect(screen, COLOR['Fondo'], [puntoInicio[0], puntoInicio[1], dimension, dimension], 0)
		
		#~ screen.blit(textinput.get_surface(), (700, 300))
		
		#======================================== Seccion Derecha ========================================
		
		# Mismas Imagenes pero con diferente Color, Para el Boton 1 (Cargar Mapa).
		boton1.resize(150, 50)		# Se Ajusta el Tamanio para el boton1.
		boton2.resize(150, 50)		# Se Ajusta el Tamanio para el boton2.
		
		if Btn1Pressed == False: screen.blit(boton1.image, (927, 35))		# Si el Boton 1 No Ha Sido Presionado, se Mostrara el objeto boton1
		else: screen.blit(boton2.image, (927, 35))							# Si no, se mostrara el objeto boton2 mientras este presionado el Boton.
		
		if Error:	# Si Ocurrio Un Error, Esta Seccion Es La Que se Encargara de Mostrarlo.
			
			# Dibuja El Texto en Pantalla. Ambos Son El Mismo, Pero 1 Pixel de diferencia uno del otro, da efecto de profundidad.
			dibujarTexto(screen, CadenaError, [920, 89], Fuentes['Droid 15'], COLOR['Naranja'])
			dibujarTexto(screen, CadenaError, [921, 90], Fuentes['Droid 15'], COLOR['Rojo'])
		
		# Dibuja El Texto en El Boton. Los 2 Textos Son el Mismo, Dan el Efecto de Profundidad.
		dibujarTexto(screen, 'Cargar Mapa',	[937, 45], Fuentes['Wendy 30'], COLOR['Naranja'])
		dibujarTexto(screen, 'Cargar Mapa', [938, 46], Fuentes['Wendy 30'], COLOR['Naranja'])
		dibujarTexto(screen, 'Cargar Mapa', [939, 47], Fuentes['Wendy 30'], COLOR['Amarillo'])
		
		# Dibuja Recuadro Derecha.
		pygame.draw.rect(screen, COLOR['Gris'],   [900, 120,  200, 460], 0)
		pygame.draw.rect(screen, COLOR['Gris'],   [900, 120,  200, 460], 3)
		
			# Dibuja la Seccion para 'Asignar Valores a Terrenos'.
		
		if Cargar and Iniciar == False:		# Si Ya Se Cargo el Mapa y Aun no se ha iniciado el Juego con el Boton 'Comenzar':
			
			#==========================================================================================================================
			
			dibujarTexto(screen, 'Asignar Valores', [909, 119], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Asignar Valores', [910, 120], Fuentes['Droid 20'], COLOR['Morado'])
		
				# Bloque 1:	============================================
			
			DibujarMiniaturaTextura(screen, Objetos10, BtnIzq1, BtnDer1, 910, 150, 'Pared', Lisy, LisyPos1, Fuentes)
		
				# Bloque 2:	============================================
			
			if LisyPos2 in [LisyPos1] and LisyPos2 != 0:		# Si El Valor Esta Repetido Con Sus Antecesores (Pared)
				
				# Dibuja La Asignacion En Rojo Por Estar Repetido El Valor.
				DibujarMiniaturaTextura(screen, Objetos10, BtnIzq2, BtnDer2, 910, 200, 'Camino', Lisy, LisyPos2, Fuentes, True)
			
			else: DibujarMiniaturaTextura(screen, Objetos10, BtnIzq2, BtnDer2, 910, 200, 'Camino', Lisy, LisyPos2, Fuentes)
			
				# Bloque 3:	============================================
			
			if LisyPos3 in [LisyPos1, LisyPos2] and LisyPos3 != 0:		# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino)
				
				# Dibuja La Asignacion En Rojo Por Estar Repetido El Valor.
				DibujarMiniaturaTextura(screen, Objetos10, BtnIzq3, BtnDer3, 910, 250, 'Pasto', Lisy, LisyPos3, Fuentes, True)
			
			else: DibujarMiniaturaTextura(screen, Objetos10, BtnIzq3, BtnDer3, 910, 250, 'Pasto', Lisy, LisyPos3, Fuentes)
			
				# Bloque 4:	============================================
			
			if LisyPos4 in [LisyPos1, LisyPos2, LisyPos3] and LisyPos4 != 0:	# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Pasto)
				
				# Dibuja La Asignacion En Rojo Por Estar Repetido El Valor.
				DibujarMiniaturaTextura(screen, Objetos10, BtnIzq4, BtnDer4, 910, 300, 'Lava', Lisy, LisyPos4, Fuentes, True)
			
			else: DibujarMiniaturaTextura(screen, Objetos10, BtnIzq4, BtnDer4, 910, 300, 'Lava', Lisy, LisyPos4, Fuentes)
			
				# Bloque 5:	============================================
			
			if LisyPos5 in [LisyPos1, LisyPos2, LisyPos3, LisyPos4] and LisyPos5 != 0:	# Si El Valor Esta Repetido Con Sus Antecesores (Pared, Camino, Pasto, Lava)
				
				# Dibuja La Asignacion En Rojo Por Estar Repetido El Valor.
				DibujarMiniaturaTextura(screen, Objetos10, BtnIzq5, BtnDer5, 910, 350, 'Agua', Lisy, LisyPos5, Fuentes, True)
			
			else: DibujarMiniaturaTextura(screen, Objetos10, BtnIzq5, BtnDer5, 910, 350, 'Agua', Lisy, LisyPos5, Fuentes)
			
			#==========================================================================================================================
			
			# Asigna Los Valores a las Variables Globales Siguientes:
			Pared  = LisyPos1
			Camino = LisyPos2
			Pasto  = LisyPos3
			Lava   = LisyPos4
			Agua   = LisyPos5
			
			botonPers1.resize(100,35)
			botonPers2.resize(100,35)
			
			if Btn2Pressed == False: screen.blit(botonPers1.image, (950,550))
			else: screen.blit(botonPers2.image, (950,550))
			
			dibujarTexto(screen, 'Comenzar', [960, 557], Fuentes['Wendy 25'], COLOR['Negro'])
			dibujarTexto(screen, 'Comenzar', [961, 558], Fuentes['Wendy 25'], COLOR['Purpura'])
			
		
		#======================================== Seccion Izquierda ========================================
		
		# Dibuja El Rectangulo Para la Seccion Izquierda.
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,  240, 30], 0)
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,  240, 30], 3)
		pygame.draw.rect(screen, COLOR['Gris'],   [10, 40,  240, 540], 0)
		pygame.draw.rect(screen, COLOR['Gris'],   [10, 40,  240, 540], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [9, 40],[250,  40], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [9, 155],[250,  155], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [9, 270],[250,  270], 3)
		
		dibujarTexto(screen, 'Informacion',		  [69, 11],  Fuentes['Wendy 30'], COLOR['Verde'])
		dibujarTexto(screen, 'Informacion',		  [70, 12],  Fuentes['Wendy 30'], COLOR['Verde Claro'])
		
					#===============================================================
		
					# Dibuja La Seccion de 'Informacion':
		
		dibujarTexto(screen, 'Personaje: ',		  [15, 54],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Personaje: ',		  [16, 55],  Fuentes['Droid 20'], COLOR['Azul'])
		
		if NP == None: # Si Aun No Se Ha Seleccionado Un Personaje.
			
			dibujarTexto(screen, 'Seleccionar', [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen, 'Seleccionar', [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
		
		else: # Si ya fue Seleccionado.
			
			dibujarTexto(screen,  NombrePersonaje[NP], [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen,  NombrePersonaje[NP], [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
		
		dibujarTexto(screen, 'Posición Actual: ', [14, 85],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Posición Actual: ', [15, 86],  Fuentes['Droid 20'], COLOR['Azul'])
		
		if seleccion == None: # Si Aun no hay nada en la Variable Seleccion, Dibuja 'Ninguna'.
			
			dibujarTexto(screen,  'Ninguna',	  [162, 85], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen,  'Ninguna',	  [163, 86], Fuentes['Droid 20'], COLOR['Negro'])
		
		else: # De lo contrario, Dibuja la Posicion actual del Personaje.
			
			dibujarTexto(screen,  str(seleccion[0])+', '+str(seleccion[1]),	  [162, 85], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen,  str(seleccion[0])+', '+str(seleccion[1]),	  [163, 86], Fuentes['Droid 20'], COLOR['Negro'])
		
		Temp = 'Ninguno'			# Variable Temporal Que Imprime el Nombre del Terreno Actual.
		for x in VALORES:			# Se Obtienen los Valores De cada Terreno en La Matriz.
			if x[0] == seleccion: 	# Si La Posicion Del Valor en X es Igual a la Seleccion Actual (Posicion del Jugador).
				Temp = x[2]			# Dibuja El Nombre Del Terreno en esa Posicion.
		
		dibujarTexto(screen, 'Terreno Actual: ', [14, 115],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Terreno Actual: ', [15, 116],  Fuentes['Droid 20'], COLOR['Azul'])
		dibujarTexto(screen,  str(Temp),	  	 [162, 115], Fuentes['Droid 20'], COLOR['Azul'])
		dibujarTexto(screen,  str(Temp),	  	 [163, 116], Fuentes['Droid 20'], COLOR['Negro'])
		
					#===============================================================
		
					# Dibuja La Seccion 'Seleccion de Personaje':
		
		dibujarTexto(screen, 'Seleccionar Personaje', [27, 169], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Seleccionar Personaje', [28, 170], Fuentes['Droid 20'], COLOR['Morado'])
		
		# Cambia el Tamaño de Las Miniaturas de los personajes en 50x50 pixeles.
		Cuadro1.resize(50,50)
		Cuadro2.resize(50,50)
		Cuadro3.resize(50,50)
		
		# Dibuja recuadros Blancos con Margen Negro en donde iran las Miniaturas.
		pygame.draw.rect(screen, COLOR['Blanco'], [28, 198, 54, 54], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [28, 198, 54, 54], 2)
		pygame.draw.rect(screen, COLOR['Blanco'], [98, 198, 54, 54], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [98, 198, 54, 54], 2)
		pygame.draw.rect(screen, COLOR['Blanco'], [168, 198, 54, 54], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [168, 198, 54, 54], 2)
		
		# Se Colocan Las Miniaturas.
		screen.blit(Cuadro1.image, (30, 200))
		screen.blit(Cuadro2.image, (100, 200))
		screen.blit(Cuadro3.image, (170, 200))
		
		if seleccionPers1:		# Si El Personaje 1 Fue Seleccionado
			
			pygame.draw.rect(screen, COLOR['Seleccion'], [30,  200, 51, 51], 0)		# Se Muestra el Recuadro de Seleccion (Color Amarillento) Temporalmente.
			#~ CargarPers = False
			seleccionPers1 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
			NP = 0						# Se Asigna a NP el Numero De Personaje.
			
		elif seleccionPers2:		# Si El Personaje 2 Fue Seleccionado
			
			pygame.draw.rect(screen, COLOR['Seleccion'], [100, 200, 51, 51], 0)		# Se Muestra el Recuadro de Seleccion (Color Amarillento) Temporalmente.
			#~ CargarPers = False
			seleccionPers2 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
			NP = 1						# Se Asigna a NP el Numero De Personaje.
			
		elif seleccionPers3:		# Si El Personaje 3 Fue Seleccionado
			
			pygame.draw.rect(screen, COLOR['Seleccion'], [170, 200, 51, 51], 0)		# Se Muestra el Recuadro de Seleccion (Color Amarillento) Temporalmente.
			#~ CargarPers = False
			seleccionPers3 = False		# No Volvera a entrar aqui hasta que se vuelva a seleccionar.
			NP = 2						# Se Asigna a NP el Numero De Personaje.
		
		#===================================================================================================
		
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()


#=====================================================================================================
#=====================================================================================================
#=====================================================================================================

if __name__ == "__main__":
	
	main()


