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

GRIS   = (189, 189, 189)

FONDO  = (24,  25,  30)

COLOR  = [BLANCO, NEGRO, GRISC, ROJO, VERDE, AZUL, AZULL, FONDO, GRIS]

SELECCIONA = (220, 200, 0)
DIMENCIONES = (1120, 600)
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

VALORES = []
SELECT = []
POSBLANCO = []
POSAZUL = []


#Clases 
class Bloque(pygame.sprite.Sprite, pygame.font.Font):
	
	def __init__(self, Nombre):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(Nombre, True)
	
	def resize(self, TX, TY):
		
		self.image = pygame.transform.scale(self.image, (TX, TY))

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



#=======================================================================

def dibujarTablero(XPOS, YPOS, screen, dimension, p_inicio, tamanio_fuente, fuentes, seleccion, SelTemp, Matriz, Lisy, Objetos):
	
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
				
				VALORES.append(([LETRAS[i],j+1], Lisy[0], 'Camino'))
				#~ pygame.draw.rect(screen, COLOR[2], [x, y, dimension, dimension], 0)
				
				Objetos[3].resize(DistX, DistY)
				bloque = Objetos[3]
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[1]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[1], 'Pared'))
				
				#~ pygame.draw.rect(screen, COLOR[7], [x, y, dimension, dimension], 0)
				
				Objetos[1].resize(DistX, DistY)
				bloque = Objetos[1]
				screen.blit(bloque.image, (x,y))
				
			elif Matriz[j][i] == Lisy[2]:
				
				VALORES.append(([LETRAS[i],j+1], Lisy[2], 'Pasto'))
				
				#~ pygame.draw.rect(screen, COLOR[4], [x, y, dimension, dimension], 0)
				
				Objetos[4].resize(DistX, DistY)
				bloque = Objetos[4]
				screen.blit(bloque.image, (x,y))
				
			else:
				
				VALORES.append(([LETRAS[i],j+1], 'N/A', 'N/A'))
				
				#~ pygame.draw.rect(screen, COLOR[0], [x, y, dimension, dimension], 0)
				
				Objetos[2].resize(DistX, DistY)
				bloque = Objetos[2]
				screen.blit(bloque.image, (x,y))
				
			if seleccion[0] == LETRAS[i] and j == seleccion[1] - 1:
				
				#~ pygame.draw.rect(screen, (0,255,0), [x, y, dimension, dimension], 0)
				# dibuja el círculo
				
				if XPOS <= YPOS:
					
					#~ if i == 0 and j == 0: pygame.draw.circle(screen, COLOR[5], (x+(DistX//2), y+(DistY//2)), 290//YPOS-8)
					#~ elif (i > 0 and i < XPOS) or (j > 0 and j < YPOS): pygame.draw.circle(screen, COLOR[5], (x+(DistX//2), y+(DistY//2)), 290//YPOS-8)
					
					#~ pygame.draw.circle(screen, COLOR[5], (x+(DistX//2), y+(DistY//2)), 290//YPOS-8)
					
					Objetos[0].resize(DistX, DistY)
					personaje = Objetos[0]
					screen.blit(personaje.image, (x, y))
					
				else:
					
					Objetos[0].resize(DistX, DistY)
					personaje = Objetos[0]
					screen.blit(personaje.image, (x, y))
					#~ pygame.draw.circle(screen,  COLOR[5], (x+(DistX//2), y+(DistY//2)), 290//XPOS-8)
				
				# Si la coordenada no esta en la lista, se aniade al registro de Recorrido:
				if not seleccion in SELECT: SELECT.append(seleccion)
				
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1: pygame.draw.rect(screen, SELECCIONA, [x, y, dimension, dimension], 0)
			
			# Imprimir El Recorrido:
			if [LETRAS[i],j+1] in SELECT: dibujarTexto(screen, str(SELECT.index([LETRAS[i],j+1]) + 1), [x+1, y], fuentes[5], COLOR[3])
			
			# Dibuja Los Numeros En Y
			if i == 0: dibujarTexto(screen, str(j + 1), [p_inicio[0] - tamanio_fuente, j * dimension + p_inicio[1] + ((DistY // 2) - (tamanio_fuente//2))], fuentes[0], COLOR[5])
			
		# Dibuja Las Letras En X
		dibujarTexto(screen, LETRAS[i], [i * dimension + p_inicio[0] + ((DistX // 2) - 7), p_inicio[1] - tamanio_fuente], fuentes[0], COLOR[5])
		

def dibujarTexto(screen, texto, posicion, fuentes, color):
	
	Texto = fuentes.render(texto, 1, color)
	screen.blit(Texto, posicion)


def ajustarMedidas(POS, tamanio_fuente):
	
	if DIMENCIONES[1] < DIMENCIONES[0]:
		ancho = int((DIMENCIONES[1] - (tamanio_fuente * 2)) / POS)
		inicio = tamanio_fuente + 260, tamanio_fuente + 10
	else:
		ancho = int((DIMENCIONES[0] - (tamanio_fuente * 2)) / POS)
		inicio = tamanio_fuente + 10, tamanio_fuente + 10
	return [inicio, ancho]


def obtenerPosicionClic(XPOS, YPOS, mouse, dimension, p_inicio, actual):
	
	xr, yr = mouse[0], mouse[1]
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]
			y = j * dimension + p_inicio[1]
			
			if (xr >= x) and (xr <= x + dimension) and (yr >= y) and (yr <= y + dimension): actual = [LETRAS[i], j + 1]
	
	return actual


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


def AbrirArchivo():
	
	Cadena = ''
	Nombre = explorer.GetFileName()
	
	if Nombre == None: print('\n\n\t Error! Nombre de Archivo No Fue Especificado.'); sys.exit(1)
	
	with open(Nombre, 'r') as Archivo: Cadena = Archivo.read()
	Archivo.close()
	
	return Cadena


def ObtenerMatriz(Cadena):
	
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


#=======================================================================

# Funciones 
def load_image(filename, transparent=False):
	
	try: image = pygame.image.load(filename)
	except pygame.error as message: raise SystemExit
	
	image = image.convert()
	
	if transparent:
		
		color = image.get_at((0,0))
		image.set_colorkey(color, RLEACCEL)
		
	return image

#=======================================================================

def main():
	
	Cadena  = AbrirArchivo()
	Matrixy = ObtenerMatriz(Cadena)
	
	if Matrixy == True: print('\n\n\t Error! La Cuadricula No Puede Ser Diseñada!\n\n\t No Todas Las Filas Son De La Misma Longitud.'); sys.exit(1)
	elif Matrixy == False: print('\n\n\t Error! Ingrese Solo Numeros En La Cuadricula.'); sys.exit(1)
	
	Lisy = []
	
	for x in Matrixy:
		for y in x:
			if not y in Lisy: Lisy.append(y)
	
	Lisy = sorted(Lisy)
	
	FULL = False
	XPOS = len(Matrixy[0])
	YPOS = len(Matrixy)
	
	POS  = (XPOS if XPOS > YPOS else YPOS)
	
	if XPOS <= 1 or YPOS <= 1:
		print('\n\n\t Error! La Cuadricula es Más Pequeña de lo permitido!')
		print('\n\n\t Minimo Permitido: 2 x 2\n\n\t Valores Actuales: ' + str(XPOS) + ' x ' + str(YPOS))
		sys.exit(1)
	elif XPOS >= 16 or YPOS >= 16:
		print('\n\n\t Error! La Cuadricula es Más Grande de lo permitido!')
		print('\n\n\t Maximo Permitido: 15 x 15\n\n\t Valores Actuales: ' + str(XPOS) + ' x ' + str(YPOS))
		sys.exit(1)
	
	pygame.init()
	screen = pygame.display.set_mode(DIMENCIONES)
	BGimg = load_image('img/fondo-negro.jpg')
	#~ bola = Bola()
	pygame.display.set_caption("Laberinto")
	game_over = False
	clock = pygame.time.Clock()
	tamanio_fuente = 30
	
	NombrePersonaje = ['Hombre','Mono','Pez']
	
	seleccion = ['A', 1]
	SelTemp = ['P',16]
	
	fuentes = [ pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", tamanio_fuente),
				pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", 15),
				pygame.font.Font("fuentes/Wendy.ttf", tamanio_fuente),
				pygame.font.Font("fuentes/Wendy.ttf", 24),
				pygame.font.Font("fuentes/Wendy.ttf", 20),
				pygame.font.Font("fuentes/DroidSans.ttf", 16),
				pygame.font.Font("fuentes/DroidSans.ttf", 12)]
	
	puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
	
	personaje = Personaje("img/SinRostro.png")
	bloque1 = Bloque("img/Bloque1.png")
	bloque2 = Bloque("img/N-A.jpg")
	bloque3 = Bloque("img/piedra.jpg")
	bloque4 = Bloque("img/pasto.jpg")
	
	Objetos = [personaje, bloque1, bloque2, bloque3, bloque4]
	
	while game_over is False:
		
		#~ MousePos = pygame.mouse.get_pos()
		
		for evento in pygame.event.get():
			
			if evento.type == pygame.QUIT: game_over = True
			
			elif evento.type == pygame.KEYDOWN:
				
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
				
			elif evento.type == pygame.MOUSEBUTTONDOWN:
				
				pos = pygame.mouse.get_pos()
				
				#~ print(pos)
				
				pygame.mouse.set_visible(False)
				SelTemp = seleccion
				
				SelTemp = obtenerPosicionClic(XPOS, YPOS, pos, dimension, puntoInicio, SelTemp)
				
			elif evento.type == pygame.MOUSEBUTTONUP:
				
				pygame.mouse.set_visible(True)
				SelTemp = ['P',16]
		
		screen.blit(BGimg, (0, 0)) 
		#~ screen.fill(FONDO)
		
		pygame.draw.rect(screen, BLANCO, [10, 10,  240, 580], 0)
		pygame.draw.rect(screen, NEGRO,  [10, 10,  240, 580], 3)
		pygame.draw.line(screen, NEGRO,  [10, 40],[250,  40], 3)
		
		dibujarTexto(screen, 'Informacion',		  [80, 15],  fuentes[3], COLOR[4])
		dibujarTexto(screen, 'Personaje: ',		  [16, 50],  fuentes[5], COLOR[1])
		dibujarTexto(screen,  NombrePersonaje[0], [150, 50], fuentes[5], COLOR[5])
		dibujarTexto(screen, 'Posicion Actual: ', [16, 70],  fuentes[5], COLOR[1])
		dibujarTexto(screen,  str(seleccion),	  [150, 70], fuentes[5], COLOR[5])
		
		Temp = None
		
		for x in VALORES:
			
			if x[0] == seleccion: Temp = x[2]
				 
		dibujarTexto(screen, 'Terreno Actual: ', [16, 90],  fuentes[5], COLOR[1])
		dibujarTexto(screen,  str(Temp),	  	 [150, 90], fuentes[5], COLOR[5])
		
		dibujarTablero(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, fuentes, seleccion, SelTemp, Matrixy, Lisy, Objetos)
		
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()


if __name__ == "__main__":
	
	main()
