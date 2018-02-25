
# Version: 1.2.5
import pygame
from pygame.locals import *
import explorer
import sys, os


BLANCO = (255, 255, 255)
NEGRO  = (0,   0,   0)

GRISC  = (216, 216, 216)
ROJO   = (255, 0,   0)
VERDE  = (4,   180, 4)
VERDEC  = (0,   255, 0)

AZUL   = (20,  80,  240)
AZULL  = (40,  210, 250)
AMARILLO = (255,255, 0)

NARANJA = (255,120,0)
MORADO = (76, 11, 95)
PURPURA = (56, 11, 97)

SELECCIONA = (220, 200, 0)
GRIS   = (189, 189, 189)
FONDO  = (24,  25,  30)

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
			
			if Matriz[j][i] == '-1':
				
				VALORES.append(([LETRAS[i],j+1], 'N/A', 'N/A'))
				
				Objetos['N/A'].resize(DistX, DistY)
				bloque = Objetos['N/A']
				screen.blit(bloque.image, (x,y))
			
			elif Matriz[j][i] == Lisy[Pared]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[0], 'Pared'))
				
				Objetos['Pared'].resize(DistX, DistY)
				bloque = Objetos['Pared']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Camino]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[1], 'Camino'))
				
				Objetos['Camino'].resize(DistX, DistY)
				bloque = Objetos['Camino']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Pasto]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Pasto'))
				
				Objetos['Pasto'].resize(DistX, DistY)
				bloque = Objetos['Pasto']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Lava]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Lava'))
				
				Objetos['Lava'].resize(DistX, DistY)
				bloque = Objetos['Lava']
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[Agua]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Agua'))
				
				Objetos['Agua'].resize(DistX, DistY)
				bloque = Objetos['Agua']
				screen.blit(bloque.image, (x,y))
				
			else:
				
				VALORES.append(([LETRAS[i],j+1], 'N/A', 'N/A'))
				
				Objetos['N/A'].resize(DistX, DistY)
				bloque = Objetos['N/A']
				screen.blit(bloque.image, (x,y))
				
			if seleccion[0] == LETRAS[i] and j == seleccion[1] - 1:
				
				if XPOS <= YPOS:
					
					Objetos['Personaje'].resize(DistX, DistY)
					personaje = Objetos['Personaje']
					screen.blit(personaje.image, (x, y))
					
				else:
					
					Objetos['Personaje'].resize(DistX, DistY)
					personaje = Objetos['Personaje']
					screen.blit(personaje.image, (x, y))
					
				# Si la coordenada no esta en la lista, se aniade al registro de Recorrido:
				if not seleccion in SELECT: SELECT.append(seleccion)
				
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1: pygame.draw.rect(screen, SELECCIONA, [x, y, dimension, dimension], 0)
			
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

#===================================================================================================


Error = False
CadenaError = ''

NA = 0
Pared = 0
Camino = 0
Pasto = 0
Lava = 0
Agua = 0


#===================================================================================================

def main():
	
	global Error, CadenaError
	
	XPOS = 1
	YPOS = 1
	POS  = (XPOS if XPOS > YPOS else YPOS)
	
	Lisy = ['-1']
	LisyPos1 = 0
	LisyPos2 = 0
	LisyPos3 = 0
	LisyPos4 = 0
	LisyPos5 = 0
	
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
	
	personaje = None
	bloque1 = Bloque("img/Bloque1.png")
	bloque2 = Bloque("img/N-A.jpg")
	bloque3 = Bloque("img/camino.jpg")
	bloque4 = Bloque("img/pasto.jpg")
	bloque5 = Bloque("img/Lava Cracks.jpg")
	bloque6 = Bloque("img/Agua.jpg")
	
	bloque11 = Bloque("img/Bloque1.png")
	bloque12 = Bloque("img/N-A.jpg")
	bloque13 = Bloque("img/camino.jpg")
	bloque14 = Bloque("img/pasto.jpg")
	bloque15 = Bloque("img/Lava Cracks.jpg")
	bloque16 = Bloque("img/Agua.jpg")
	
	boton1 = Boton("img/BotonRojo.png")
	boton2 = Boton("img/BotonNaranja.png")
	#~ botonPers1 = Boton("img/BotonPurpura.png")
	#~ botonPers2 = Boton("img/BotonAzul.png")
	
	BtnIzq1 = BotonDir("img/BotonIzq.png")
	BtnDer1 = BotonDir("img/BotonIzq.png")
	BtnDer1.flip(True)
	BtnIzq2 = BotonDir("img/BotonIzq.png")
	BtnDer2 = BotonDir("img/BotonIzq.png")
	BtnDer2.flip(True)
	BtnIzq3 = BotonDir("img/BotonIzq.png")
	BtnDer3 = BotonDir("img/BotonIzq.png")
	BtnDer3.flip(True)
	BtnIzq4 = BotonDir("img/BotonIzq.png")
	BtnDer4 = BotonDir("img/BotonIzq.png")
	BtnDer4.flip(True)
	BtnIzq5 = BotonDir("img/BotonIzq.png")
	BtnDer5 = BotonDir("img/BotonIzq.png")
	BtnDer5.flip(True)
	
	Cuadro1 = Personaje("img/personaje.gif")
	Cuadro2 = Personaje("img/CatBug.png")
	Cuadro3 = Personaje("img/SinRostro.png")
	
	RutaPersonaje = {
					'Hombre':"img/personaje.gif",
					'Gato':"img/CatBug.png",
					'Fantasma':"img/SinRostro.png"
					}
	
	Objetos = {'Personaje':personaje, 'Pared':bloque1, 'N/A':bloque2, 'Camino':bloque3, 'Pasto':bloque4,
			   'Lava':bloque5, 'Agua':bloque6}
	Objetos10 = {'Personaje':personaje, 'Pared':bloque11, 'N/A':bloque12, 'Camino':bloque13, 'Pasto':bloque14,
				 'Lava':bloque15, 'Agua':bloque16}
	
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
				
				# Cooredenadas Boton 1:
				if (xr >= 927) and (xr <= 1077) and (yr >= 44) and (yr <= 80): Btn1Pressed = True; CargarMapa = True
				
				# ======= Cooredenadas Boton Izquierda y Derecha =======
				
				if Cargar:
					
					# Bloque Pared:
					if (xr >= 111) and (xr <= 136) and (yr >= 338) and (yr <= 358):
						if LisyPos1 > 0 and LisyPos1 < len(Lisy): LisyPos1 -= 1
					elif (xr >= 161) and (xr <= 186) and (yr >= 338) and (yr <= 358):
						if LisyPos1 >= 0 and LisyPos1 < len(Lisy)-1: LisyPos1 += 1
					
					# Bloque Camino:
					elif (xr >= 111) and (xr <= 136) and (yr >= 388) and (yr <= 408):
						if LisyPos2 > 0 and LisyPos2 < len(Lisy): LisyPos2 -= 1
					elif (xr >= 161) and (xr <= 186) and (yr >= 388) and (yr <= 408):
						if LisyPos2 >= 0 and LisyPos2 < len(Lisy)-1: LisyPos2 += 1
					
					# Bloque Pasto:
					elif (xr >= 111) and (xr <= 136) and (yr >= 438) and (yr <= 458):
						if LisyPos3 > 0 and LisyPos3 < len(Lisy): LisyPos3 -= 1
					elif (xr >= 161) and (xr <= 186) and (yr >= 438) and (yr <= 458):
						if LisyPos3 >= 0 and LisyPos3 < len(Lisy)-1: LisyPos3 += 1
					
					# Bloque Lava:
					elif (xr >= 111) and (xr <= 136) and (yr >= 488) and (yr <= 508):
						if LisyPos4 > 0 and LisyPos4 < len(Lisy): LisyPos4 -= 1
					elif (xr >= 161) and (xr <= 186) and (yr >= 488) and (yr <= 508):
						if LisyPos4 >= 0 and LisyPos4 < len(Lisy)-1: LisyPos4 += 1
					
					# Bloque Agua:
					elif (xr >= 111) and (xr <= 136) and (yr >= 538) and (yr <= 558):
						if LisyPos5 > 0 and LisyPos5 < len(Lisy): LisyPos5 -= 1
					elif (xr >= 161) and (xr <= 186) and (yr >= 538) and (yr <= 558):
						if LisyPos5 >= 0 and LisyPos5 < len(Lisy)-1: LisyPos5 += 1
					
				#=======================================================
				
				# Coordenadas Recuadros Personajes 1, 2 y 3 respectivamente:
				if   (xr >= 29)  and (xr <= 82)  and (yr >= 199) and (yr <= 252): seleccionPers1 = True
				elif (xr >= 99)  and (xr <= 152) and (yr >= 199) and (yr <= 252): seleccionPers2 = True
				elif (xr >= 169) and (xr <= 222) and (yr >= 199) and (yr <= 252): seleccionPers3 = True
				
			elif evento.type == pygame.MOUSEBUTTONUP:
				
				#=======================================================
				
				if Btn1Pressed and NP == None:
					
					Error = True
					CadenaError = 'Selecciona Un Personaje'
					CargarMapa = False
					
				elif CargarMapa:
					
					xMatrixy, xLisy, xXPOS, xYPOS, xPOS = TODOArchivo()
					
					if xMatrixy == None:
						
						if Cargar == False: pass
						else: Cargar = True
						CargarMapa = False
					
					else:
						
						global SELECT
						SELECT = []
						
						Cargar = True
						
						personaje = Personaje(RutaPersonaje[NombrePersonaje[NP]])
						
						bloque1 = Bloque("img/Bloque1.png")
						bloque2 = Bloque("img/N-A.jpg")
						bloque3 = Bloque("img/camino.jpg")
						bloque4 = Bloque("img/pasto.jpg")
						bloque5 = Bloque("img/Lava Cracks.jpg")
						bloque6 = Bloque("img/Agua.jpg")
						
						Matrixy = xMatrixy
						Lisy = [-1]
						Lisy = Lisy + xLisy
						LisyPos1 = 0
						LisyPos2 = 0
						LisyPos3 = 0
						LisyPos4 = 0
						LisyPos5 = 0
						XPOS = xXPOS
						YPOS = xYPOS
						POS = xPOS
						
						puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
						Objetos = {'Personaje':personaje, 'Pared':bloque1, 'N/A':bloque2, 'Camino':bloque3, 'Pasto':bloque4,
								   'Lava':bloque5, 'Agua':bloque6}
						seleccion = ['A', 1]
						CargarMapa = False
						Error = False
				
				#=======================================================
				
				Btn1Pressed = False
				
				pygame.mouse.set_visible(True)
				SelTemp = ['P',16]
		
		#=====================================================================================================
		#=====================================================================================================
		#=====================================================================================================
		
		screen.blit(BGimg, (0, 0))
		
		#======================================== Seccion Central ========================================
		
		if Cargar: dibujarTablero(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, Fuentes, seleccion, SelTemp, Matrixy, Lisy, Objetos)
		else: pygame.draw.rect(screen, COLOR['Fondo'], [puntoInicio[0], puntoInicio[1], dimension, dimension], 0)
			
		#======================================== Seccion Derecha ========================================
		
		boton1.resize(150, 50)
		boton2.resize(150, 50)
		
		if Btn1Pressed == False: screen.blit(boton1.image, (927, 35))
		else: screen.blit(boton2.image, (927, 35))
		
		if Error:
			
			dibujarTexto(screen, CadenaError, [920, 89], Fuentes['Droid 15'], COLOR['Naranja'])
			dibujarTexto(screen, CadenaError, [921, 90], Fuentes['Droid 15'], COLOR['Rojo'])
		
		dibujarTexto(screen, 'Cargar Mapa',	[937, 45], Fuentes['Wendy 30'], COLOR['Naranja'])
		dibujarTexto(screen, 'Cargar Mapa', [938, 46], Fuentes['Wendy 30'], COLOR['Naranja'])
		dibujarTexto(screen, 'Cargar Mapa', [939, 47], Fuentes['Wendy 30'], COLOR['Amarillo'])
		
		#======================================== Seccion Izquierda ========================================
		
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,  240, 30], 0)
		pygame.draw.rect(screen, COLOR['Blanco'], [10, 10,  240, 30], 3)
		pygame.draw.rect(screen, COLOR['Gris'],   [10, 40,  240, 550], 0)
		pygame.draw.rect(screen, COLOR['Gris'],   [10, 40,  240, 550], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [9, 40],[250,  40], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [9, 155],[250,  155], 3)
		pygame.draw.line(screen, COLOR['Negro'],  [9, 265],[250,  265], 3)
		
		dibujarTexto(screen, 'Informacion',		  [69, 11],  Fuentes['Wendy 30'], COLOR['Verde'])
		dibujarTexto(screen, 'Informacion',		  [70, 12],  Fuentes['Wendy 30'], COLOR['Verde Claro'])
		
					#===============================================================
		
		dibujarTexto(screen, 'Personaje: ',		  [15, 54],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Personaje: ',		  [16, 55],  Fuentes['Droid 20'], COLOR['Azul'])
		
		if NP == None:
			dibujarTexto(screen, 'Seleccionar', [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen, 'Seleccionar', [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
		else:
			dibujarTexto(screen,  NombrePersonaje[NP], [122, 54], Fuentes['Droid 20'], COLOR['Morado'])
			dibujarTexto(screen,  NombrePersonaje[NP], [123, 55], Fuentes['Droid 20'], COLOR['Negro'])
		
		dibujarTexto(screen, 'Posición Actual: ', [14, 85],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Posición Actual: ', [15, 86],  Fuentes['Droid 20'], COLOR['Azul'])
		
		if seleccion == None:
			dibujarTexto(screen,  'Ninguna',	  [162, 85], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen,  'Ninguna',	  [163, 86], Fuentes['Droid 20'], COLOR['Negro'])
		else:
			dibujarTexto(screen,  str(seleccion[0])+', '+str(seleccion[1]),	  [162, 85], Fuentes['Droid 20'], COLOR['Verde'])
			dibujarTexto(screen,  str(seleccion[0])+', '+str(seleccion[1]),	  [163, 86], Fuentes['Droid 20'], COLOR['Negro'])
		
		Temp = 'Ninguno'
		
		for x in VALORES:
			
			if x[0] == seleccion: Temp = x[2]
				 
		dibujarTexto(screen, 'Terreno Actual: ', [14, 115],  Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Terreno Actual: ', [15, 116],  Fuentes['Droid 20'], COLOR['Azul'])
		dibujarTexto(screen,  str(Temp),	  	 [162, 115], Fuentes['Droid 20'], COLOR['Azul'])
		dibujarTexto(screen,  str(Temp),	  	 [163, 116], Fuentes['Droid 20'], COLOR['Negro'])
		
					#===============================================================
		
		dibujarTexto(screen, 'Seleccionar Personaje', [27, 169], Fuentes['Droid 20'], COLOR['Negro'])
		dibujarTexto(screen, 'Seleccionar Personaje', [28, 170], Fuentes['Droid 20'], COLOR['Morado'])
			
		Cuadro1.resize(50,50)
		Cuadro2.resize(50,50)
		Cuadro3.resize(50,50)
		
		pygame.draw.rect(screen, COLOR['Blanco'], [28, 198, 54, 54], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [28, 198, 54, 54], 2)
		pygame.draw.rect(screen, COLOR['Blanco'], [98, 198, 54, 54], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [98, 198, 54, 54], 2)
		pygame.draw.rect(screen, COLOR['Blanco'], [168, 198, 54, 54], 0)
		pygame.draw.rect(screen, COLOR['Negro'],  [168, 198, 54, 54], 2)
		
		screen.blit(Cuadro1.image, (30, 200))
		screen.blit(Cuadro2.image, (100, 200))
		screen.blit(Cuadro3.image, (170, 200))
		
		if seleccionPers1:
			pygame.draw.rect(screen, COLOR['Seleccion'], [30,  200, 51, 51], 0)
			NP = 0
			ElegirPers = False
			seleccionPers1 = False
		elif seleccionPers2:
			pygame.draw.rect(screen, COLOR['Seleccion'], [100, 200, 51, 51], 0)
			NP = 1
			ElegirPers = False
			seleccionPers2 = False
		elif seleccionPers3:
			pygame.draw.rect(screen, COLOR['Seleccion'], [170, 200, 51, 51], 0)
			NP = 2
			ElegirPers = False
			seleccionPers3 = False
		
					#===============================================================
		
		if Cargar:
			
			dibujarTexto(screen, 'Asignar Valores a Bloques', [13, 284], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Asignar Valores a Bloques', [14, 285], Fuentes['Droid 20'], COLOR['Morado'])
			
			# Bloque 1:
			pygame.draw.rect(screen, COLOR['Blanco'], [15, 320, 35, 35], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [15, 320, 35, 35], 2)
			
			Objetos10['Pared'].resize(34, 34)
			bloque = Objetos10['Pared']
			screen.blit(bloque.image, (16,321))
			
			dibujarTexto(screen, 'Tipo:   Pared', [55, 315], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Valor: ', [55, 335], Fuentes['Droid 20'], COLOR['Negro'])
			
			BtnIzq1.resize(25,20); screen.blit(BtnIzq1.image, (111, 338))
			BtnDer1.resize(25,20); screen.blit(BtnDer1.image, (161, 338))
			
			dibujarTexto(screen, str(Lisy[LisyPos1]), [140, 335], Fuentes['Droid 20'], COLOR['Negro'])
			
			# Bloque 2:
			pygame.draw.rect(screen, COLOR['Blanco'], [15, 370, 35, 35], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [15, 370, 35, 35], 2)
			
			Objetos10['Camino'].resize(34, 34)
			bloque = Objetos10['Camino']
			screen.blit(bloque.image, (16,371))
			
			dibujarTexto(screen, 'Tipo:   Camino', [55, 365], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Valor: ', [55, 385], Fuentes['Droid 20'], COLOR['Negro'])
			
			BtnIzq2.resize(25,20); screen.blit(BtnIzq2.image, (111, 388))
			BtnDer2.resize(25,20); screen.blit(BtnDer2.image, (161, 388))
			
			dibujarTexto(screen, str(Lisy[LisyPos2]), [140, 385], Fuentes['Droid 20'], COLOR['Negro'])
			
			# Bloque 3:
			pygame.draw.rect(screen, COLOR['Blanco'], [15, 420, 35, 35], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [15, 420, 35, 35], 2)
			
			Objetos10['Pasto'].resize(34, 34)
			bloque = Objetos10['Pasto']
			screen.blit(bloque.image, (16,421))
			
			dibujarTexto(screen, 'Tipo:   Pasto', [55, 415], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Valor: ', [55, 435], Fuentes['Droid 20'], COLOR['Negro'])
			
			BtnIzq3.resize(25,20); screen.blit(BtnIzq3.image, (111, 438))
			BtnDer3.resize(25,20); screen.blit(BtnDer3.image, (161, 438))
			
			dibujarTexto(screen, str(Lisy[LisyPos3]), [140, 435], Fuentes['Droid 20'], COLOR['Negro'])
			
			# Bloque 4:
			pygame.draw.rect(screen, COLOR['Blanco'], [15, 470, 35, 35], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [15, 470, 35, 35], 2)
			
			Objetos10['Lava'].resize(34, 34)
			bloque = Objetos10['Lava']
			screen.blit(bloque.image, (16,471))
			
			dibujarTexto(screen, 'Tipo:   Lava', [55, 465], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Valor: ', [55, 485], Fuentes['Droid 20'], COLOR['Negro'])
			
			BtnIzq4.resize(25,20); screen.blit(BtnIzq4.image, (111, 488))
			BtnDer4.resize(25,20); screen.blit(BtnDer4.image, (161, 488))
			
			dibujarTexto(screen, str(Lisy[LisyPos4]), [140, 485], Fuentes['Droid 20'], COLOR['Negro'])
			
			# Bloque 5:
			pygame.draw.rect(screen, COLOR['Blanco'], [15, 520, 35, 35], 0)
			pygame.draw.rect(screen, COLOR['Negro'],  [15, 520, 35, 35], 2)
			
			Objetos10['Agua'].resize(34, 34)
			bloque = Objetos10['Agua']
			screen.blit(bloque.image, (16,521))
			
			dibujarTexto(screen, 'Tipo:   Agua', [55, 515], Fuentes['Droid 20'], COLOR['Negro'])
			dibujarTexto(screen, 'Valor: ', [55, 535], Fuentes['Droid 20'], COLOR['Negro'])
			
			BtnIzq5.resize(25,20); screen.blit(BtnIzq5.image, (111, 538))
			BtnDer5.resize(25,20); screen.blit(BtnDer5.image, (161, 538))
			
			dibujarTexto(screen, str(Lisy[LisyPos5]), [140, 535], Fuentes['Droid 20'], COLOR['Negro'])
			
			global Pasto, Camino, Pared, Lava, Agua
			
			Pared  = LisyPos1
			Camino = LisyPos2
			Pasto  = LisyPos3
			Lava   = LisyPos4
			Agua   = LisyPos5
		
		
		#===================================================================================================
		
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()


#=====================================================================================================
#=====================================================================================================
#=====================================================================================================

if __name__ == "__main__":
	
	main()


