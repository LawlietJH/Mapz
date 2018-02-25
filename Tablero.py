import pygame
from pygame.locals import *
import explorer
import sys, os


BLANCO = (255, 255, 255)
NEGRO  = (0,   0,   0)

GRISC  = (216, 216, 216)
ROJO   = (255, 0,   0)
VERDE  = (0,   255, 0)

AZUL   = (20,  80,  240)
AZULL  = (40,  210, 250)
NARANJA = (255,255, 0)

SELECCIONA = (220, 200, 0)
GRIS   = (189, 189, 189)
FONDO  = (24,  25,  30)

COLOR  = {'Blanco':BLANCO, 'Negro':NEGRO,      'Gris Claro':GRISC, 'Rojo':ROJO,   'Verde':VERDE,
		  'Azul':AZUL,     'Azul Claro':AZULL, 'Gris':GRIS,        'Fondo':FONDO, 'Naranja':NARANJA,
		  'Seleccion':SELECCIONA
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


#===================================================================================================
#===================================================================================================
#===================================================================================================


def dibujarTablero(XPOS, YPOS, screen, dimension, p_inicio, tamanio_fuente, Fuentes, seleccion, SelTemp, Matriz, Lisy, Objetos):
	
	global SELECT, VALORES
	
	'''
	# Funcion que dibuja el tablero
	screen: 		referencia del lienzo donde dibujar
	dimension: 		tamanio de los rectangulos
	p_inicio: 		coordenadas del punto de inicio del tablero
	tamanio_fuente: tamanio de fuente segun el tablero
	fuente: 		Objeto fuente 
	seleccion: 		rectangulo seleccionado 
	'''
	
	VALORES = []
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]
			y = j * dimension + p_inicio[1]
			
			xp = (i+1) * dimension + p_inicio[0]
			yp = (j+1) * dimension + p_inicio[1]
			
			DistX = xp - x
			DistY = yp - y
			
			if Matriz[j][i] == Lisy[0]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[0], 'Pared'))
				
				Objetos[1].resize(DistX, DistY)
				bloque = Objetos[1]
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[1]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[1], 'Camino'))
				
				Objetos[3].resize(DistX, DistY)
				bloque = Objetos[3]
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[2]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Pasto'))
				
				Objetos[4].resize(DistX, DistY)
				bloque = Objetos[4]
				screen.blit(bloque.image, (x,y))
				
			else:
				
				VALORES.append(([LETRAS[i],j+1], 'N/A', 'N/A'))
				
				Objetos[2].resize(DistX, DistY)
				bloque = Objetos[2]
				screen.blit(bloque.image, (x,y))
				
			if seleccion[0] == LETRAS[i] and j == seleccion[1] - 1:
				
				if XPOS <= YPOS:
					
					Objetos[0].resize(DistX, DistY)
					personaje = Objetos[0]
					screen.blit(personaje.image, (x, y))
					
				else:
					
					Objetos[0].resize(DistX, DistY)
					personaje = Objetos[0]
					screen.blit(personaje.image, (x, y))
					
				# Si la coordenada no esta en la lista, se aniade al registro de Recorrido:
				if not seleccion in SELECT: SELECT.append(seleccion)
				
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1: pygame.draw.rect(screen, SELECCIONA, [x, y, dimension, dimension], 0)
			
			# Imprimir El Recorrido:
			if [LETRAS[i],j+1] in SELECT: dibujarTexto(screen, str(SELECT.index([LETRAS[i],j+1]) + 1), [x+1, y], Fuentes['Droid 15'], COLOR['Rojo'])
			
			# Dibuja Los Numeros En Y
			if i == 0: dibujarTexto(screen, str(j + 1), [p_inicio[0] - tamanio_fuente, j * dimension + p_inicio[1] + ((DistY // 2) - (tamanio_fuente//2))], Fuentes['Wendy 30'], COLOR['Azul'])
			
		# Dibuja Las Letras En X
		dibujarTexto(screen, LETRAS[i], [i * dimension + p_inicio[0] + ((DistX // 2) - 7), p_inicio[1] - tamanio_fuente], Fuentes['Wendy 30'], COLOR['Azul'])

#===================================================================================================

def dibujarTexto(screen, texto, posicion, fuentes, color):
	
	Texto = fuentes.render(texto, 1, color)
	screen.blit(Texto, posicion)

#===================================================================================================

def ajustarMedidas(POS, tamanio_fuente):
	
	if DIMENCIONES[1] < DIMENCIONES[0]:
		ancho = int((DIMENCIONES[1] - (tamanio_fuente * 2)) / POS)
		inicio = tamanio_fuente + 260, tamanio_fuente + 10
	else:
		ancho = int((DIMENCIONES[0] - (tamanio_fuente * 2)) / POS)
		inicio = tamanio_fuente + 10, tamanio_fuente + 10
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
		#~ print('\n\n\t Error! Nombre de Archivo No Fue Especificado.'); sys.exit(1)
	
	with open(Nombre, 'r') as Archivo: Cadena = Archivo.read()
	Archivo.close()
	
	return Cadena

#===================================================================================================

def ObtenerMatriz(Cadena):
	
	global Error, CadenaError
	
	if Cadena == '':
		
		CadenaError = '  Error! Archivo Vacio'
		Error = True
		return None
		#~ print('\n\n\t Error! Archvo Vacio.'); sys.exit(1)
	
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
		
		CadenaError = 'Cuadricula Minima: 2x2.'
		Error = True
		return None, None, None, None, None
		
	elif XPOS >= 16 or YPOS >= 16:
		
		CadenaError = 'Cuadricula Maxima: 15x15.'
		Error = True
		return None, None, None, None, None
	
	return Matrixy, Lisy, XPOS, YPOS, POS

#===================================================================================================


Error = False
CadenaError = ''

#===================================================================================================

def main():
	
	global Error, CadenaError
	
	XPOS = 1
	YPOS = 1
	POS  = (XPOS if XPOS > YPOS else YPOS)
	#~ Matrixy = None
	#~ Lisy = None
	#~ Objetos = None
	
	CargarMapa = None
	ElegirPers = False
	FULL = False
	Cargar = False
	
	NP = None
	seleccion = None
	seleccionPers1 = None
	seleccionPers2 = None
	seleccionPers3 = None
	SelTemp = ['P',16]
	NombrePersonaje = ['Hombre','Gato','Fantasma']
	
	pygame.init()
	
	screen = pygame.display.set_mode(DIMENCIONES)
	BGimg = load_image('img/fondo-negro.jpg')
	
	pygame.display.set_caption("Laberinto")
	game_over = False
	clock = pygame.time.Clock()
	tamanio_fuente = 30
	
	#===================================================================
	
	# Fuentes:
	
	Fuentes = {'Alice 40':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 40),
			   'Alice 35':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 35),
			   'Alice 30':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 30),
			   'Alice 25':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 25),
			   'Alice 20':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 20),
			   'Alice 15':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 15),
			   'Alice 10':pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 10),
			   'Wnedy 40':pygame.font.Font("fuentes/Wendy.ttf", 40),
			   'Wendy 35':pygame.font.Font("fuentes/Wendy.ttf", 35),
			   'Wendy 30':pygame.font.Font("fuentes/Wendy.ttf", 30),
			   'Wendy 25':pygame.font.Font("fuentes/Wendy.ttf", 25),
			   'Wendy 20':pygame.font.Font("fuentes/Wendy.ttf", 20),
			   'Wendy 15':pygame.font.Font("fuentes/Wendy.ttf", 15),
			   'Wendy 10':pygame.font.Font("fuentes/Wendy.ttf", 10),
			   'Droid 40':pygame.font.Font("fuentes/DroidSans.ttf", 40),
			   'Droid 35':pygame.font.Font("fuentes/DroidSans.ttf", 35),
			   'Droid 30':pygame.font.Font("fuentes/DroidSans.ttf", 30),
			   'Droid 25':pygame.font.Font("fuentes/DroidSans.ttf", 25),
			   'Droid 20':pygame.font.Font("fuentes/DroidSans.ttf", 20),
			   'Droid 15':pygame.font.Font("fuentes/DroidSans.ttf", 15),
			   'Droid 10':pygame.font.Font("fuentes/DroidSans.ttf", 10)
			   }
	
	#===================================================================
	
	puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
	
	# Objetos:
	
	#~ personaje = Personaje("img/SinRostro.png")
	#~ bloque1 = Bloque("img/Bloque1.png")
	#~ bloque2 = Bloque("img/N-A.jpg")
	#~ bloque3 = Bloque("img/piedra.jpg")
	#~ bloque4 = Bloque("img/pasto.jpg")
	boton1 = Boton("img/BotonRojo.png")
	boton2 = Boton("img/BotonNaranja.png")
	botonPers1 = Boton("img/BotonPurpura.png")
	botonPers2 = Boton("img/BotonAzul.png")
	
	Cuadro1 = Personaje("img/personaje.gif")
	Cuadro2 = Personaje("img/CatBug.png")
	Cuadro3 = Personaje("img/SinRostro.png")
	
	RutaPersonaje = {
				  'Hombre':"img/personaje.gif",
				  'Gato':"img/CatBug.png",
				  'Fantasma':"img/SinRostro.png"
				 }
	
	#~ Objetos = [personaje, bloque1, bloque2, bloque3, bloque4]
	
	#===================================================================
	
	# Botones:
	Btn1Pressed = False
	Btn2Pressed = False
	
	#===================================================================
	
	while game_over is False:
		
		#~ MousePos = pygame.mouse.get_pos()
		
		#=====================================================================================================
		#=====================================================================================================
		#=====================================================================================================
		
		for evento in pygame.event.get():
			
			#~ print(evento.type)
			
			if evento.type == pygame.QUIT: game_over = True
			
			elif evento.type == pygame.KEYDOWN:
				
				if Cargar:
					
					if   evento.key == pygame.K_LEFT:	seleccion = obtenerPosicion(XPOS, YPOS, 'L', seleccion, personaje)
					elif evento.key == pygame.K_RIGHT:	seleccion = obtenerPosicion(XPOS, YPOS, 'R', seleccion, personaje)
					elif evento.key == pygame.K_UP:		seleccion = obtenerPosicion(XPOS, YPOS, 'U', seleccion, personaje)
					elif evento.key == pygame.K_DOWN:	seleccion = obtenerPosicion(XPOS, YPOS, 'D', seleccion, personaje)
			
				if evento.key == pygame.K_ESCAPE: game_over = True
				
				elif evento.key == pygame.K_f:
					
					if FULL == False:
						screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
						FULL = True
					else:
						screen = pygame.display.set_mode(DIMENCIONES)
						FULL = False
			
			#~ elif evento.type == pygame.JOYBUTTONDOWN
			elif evento.type == pygame.MOUSEBUTTONDOWN:
				
				pos = pygame.mouse.get_pos()
				pygame.mouse.set_visible(False)
				SelTemp = seleccion
				
				SelTemp = obtenerPosicionClic(XPOS, YPOS, pos, dimension, puntoInicio, SelTemp)
				
				xr, yr = pos[0], pos[1]
				
				if (xr >= 900) and (xr <= 1050) and (yr >= 44) and (yr <= 80): Btn1Pressed = True; CargarMapa = True
				
				if ElegirPers:
					
					if   (xr >= 29)  and (xr <= 82)  and (yr >= 199) and (yr <= 252): seleccionPers1 = True
					elif (xr >= 99)  and (xr <= 152) and (yr >= 199) and (yr <= 252): seleccionPers2 = True
					elif (xr >= 169) and (xr <= 222) and (yr >= 199) and (yr <= 252): seleccionPers3 = True
				
				if NP == None:
					
					if (xr >= 140) and (xr <= 240) and (yr >= 45) and (yr <= 70): Btn2Pressed = True; ElegirPers = True
				
			elif evento.type == pygame.MOUSEBUTTONUP:
				
				#=======================================================
				
				if CargarMapa:
					
					xMatrixy, xLisy, xXPOS, xYPOS, xPOS = TODOArchivo()
					
					if xMatrixy == None:
						
						if Cargar == False: pass
						else: Cargar = True
						CargarMapa = False
					
					else:
						
						global SELECT
						SELECT = []
						
						Cargar = True
						try:
							personaje = Personaje(RutaPersonaje[NombrePersonaje[NP]])
							
							bloque1 = Bloque("img/Bloque1.png")
							bloque2 = Bloque("img/N-A.jpg")
							bloque3 = Bloque("img/camino.jpg")
							bloque4 = Bloque("img/pasto.jpg")
							
							Matrixy = xMatrixy
							Lisy = xLisy
							XPOS = xXPOS
							YPOS = xYPOS
							POS = xPOS
							
							puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
							Objetos = [personaje, bloque1, bloque2, bloque3, bloque4]
							seleccion = ['A', 1]
							CargarMapa = False
							Error = False
							
						except:
							
							if Cargar == True: Cargar = False
							CargarMapa = False
							
							Error = True
							CadenaError = 'Selecciona Un Personaje'
				
				#=======================================================
						
				if ElegirPers:
					
					if   seleccionPers1: seleccionPers1 = False
					elif seleccionPers2: seleccionPers2 = False
					elif seleccionPers3: seleccionPers3 = False
					
				#=======================================================
				
				Btn1Pressed = False
				Btn2Pressed = False
				
				pygame.mouse.set_visible(True)
				SelTemp = ['P',16]
		
		#=====================================================================================================
		#=====================================================================================================
		#=====================================================================================================
		
		screen.blit(BGimg, (0, 0))
		
		boton1.resize(150, 50)
		boton2.resize(150, 50)
		
		if Btn1Pressed == False: screen.blit(boton1.image, (900, 35))
		else: screen.blit(boton2.image, (900, 35))
		
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,  240, 580], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [10, 10,  240, 580], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [10, 40],[250,  40], 3)
		
		dibujarTexto(screen, 'Informacion',		  [70, 12],  Fuentes['Wendy 30'], COLOR['Verde'])
		dibujarTexto(screen, 'Personaje: ',		  [16, 50],  Fuentes['Wendy 20'], COLOR['Negro'])
		
		if NP == None:
			
			if Btn2Pressed == False:
				
				botonPers1.resize(100,25)
				screen.blit(botonPers1.image, (140, 45))
				
			elif Btn2Pressed and ElegirPers:
				
				botonPers2.resize(100,25)
				screen.blit(botonPers2.image, (140, 45))
			
			dibujarTexto(screen, 'Seleccionar', [150, 50], Fuentes['Wendy 20'], COLOR['Verde'])
			
		else: dibujarTexto(screen,  NombrePersonaje[NP], [150, 50], Fuentes['Wendy 20'], COLOR['Azul'])
		
		if ElegirPers:
			
			Cuadro1.resize(50,50)
			Cuadro2.resize(50,50)
			Cuadro3.resize(50,50)
			
			pygame.draw.rect(screen, COLOR['Negro'], [28, 198, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Negro'], [98, 198, 54, 54], 2)
			pygame.draw.rect(screen, COLOR['Negro'], [168, 198, 54, 54], 2)
			
			screen.blit(Cuadro1.image, (30, 200))
			screen.blit(Cuadro2.image, (100, 200))
			screen.blit(Cuadro3.image, (170, 200))
			
			if seleccionPers1:
				pygame.draw.rect(screen, COLOR['Seleccion'], [30,  200, 51, 51], 0)
				NP = 0
				ElegirPers = False
			elif seleccionPers2:
				pygame.draw.rect(screen, COLOR['Seleccion'], [100, 200, 51, 51], 0)
				NP = 1
				ElegirPers = False
			elif seleccionPers3:
				pygame.draw.rect(screen, COLOR['Seleccion'], [170, 200, 51, 51], 0)
				NP = 2
				ElegirPers = False
		
		dibujarTexto(screen, 'Posicion Actual: ', [16, 70],  Fuentes['Wendy 20'], COLOR['Negro'])
		dibujarTexto(screen,  str(seleccion),	  [150, 70], Fuentes['Wendy 20'], COLOR['Azul'])
		dibujarTexto(screen, 'Cargar Mapa',		  [912, 47], Fuentes['Wendy 30'], COLOR['Naranja'])
		
		Temp = None
		
		for x in VALORES:
			
			if x[0] == seleccion: Temp = x[2]
				 
		dibujarTexto(screen, 'Terreno Actual: ', [16, 90],  Fuentes['Wendy 20'], COLOR['Negro'])
		dibujarTexto(screen,  str(Temp),	  	 [150, 90], Fuentes['Wendy 20'], COLOR['Azul'])
		
		if Cargar: dibujarTablero(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, Fuentes, seleccion, SelTemp, Matrixy, Lisy, Objetos)
		
		if Error: dibujarTexto(screen, CadenaError, [900, 90], Fuentes['Droid 15'], COLOR['Rojo'])
			
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()


#=====================================================================================================
#=====================================================================================================
#=====================================================================================================

if __name__ == "__main__":
	
	main()


