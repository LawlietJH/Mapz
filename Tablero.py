import pygame
import sys, os

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (20, 80, 240)
FONDO = (24, 25, 30)
SELECCIONA = (220, 200, 0)
DIMENCIONES = (1120, 650)
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
VALORES =[]
SELECT = []
POSBLANCO = [[2,3],[3,3],[4,3],[5,7],[5,8],[5,9],[5,10]]
POSAZUL = [[1,3],[1,4],[1,5],[1,6],[3,4],[3,5]]

  # Clases 
class Bola(pygame.sprite.Sprite, pygame.font.Font): 
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = load_image("img/ball.png", True) 
        self.rect = self.image.get_rect() 
        self.rect.centerx = DIMENSIONES[0] / 2 
        self.rect.centery = DIMENSIONES[1] / 2 

def dibujarTablero(XPOS, YPOS, screen, dimension, p_inicio, tamanio_fuente, fuente, fuenteT, seleccion, SelTemp):
	
	global SELECT
	'''
	# Funcion que dibuja el tablero
	screen: 		referencia del lienzo donde dibujar
	dimension: 		tamanio de los rectangulos
	p_inicio: 		coordenadas del punto de inicio del tablero
	tamanio_fuente: tamanio de fuente segun el tablero
	fuente: 		Objeto fuente 
	seleccion: 		rectangulo seleccionado 
	'''
	color = [NEGRO, BLANCO, AZUL]
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]
			y = j * dimension + p_inicio[1]
			
			xp = i+1 * dimension + p_inicio[0]
			yp = j+1 * dimension + p_inicio[1]
			
			DistX = (x + xp) // 2
			DistY = (y + yp) // 2
			print(DistX, DistY, i, j)
			
			if [i,j] in POSBLANCO: pygame.draw.rect(screen, color[1], [x, y, dimension, dimension], 0)
			elif [i,j] in POSAZUL: pygame.draw.rect(screen, color[2], [x, y, dimension, dimension], 0)
			else: pygame.draw.rect(screen, color[0], [x, y, dimension, dimension], 0)
			
			if seleccion[0] == LETRAS[i] and j == seleccion[1] - 1:
				#~ print(seleccion[0], seleccion[1])
				#~ pygame.draw.rect(screen, (0,255,0), [x, y, dimension, dimension], 0)
				# establece las propiedades del círculo
				
				# dibuja el círculo
				print(x)
				if i == 0 and j == 0:		pygame.draw.circle(screen, (40, 210, 250), ((x+xp)//2, (y+yp)//2), 290//XPOS)
				elif (i > 0 and i < XPOS):  pygame.draw.circle(screen, (40, 210, 250), ((x+xp)//2, (y+yp)//2), 290//XPOS)
				elif (j > 0 and j < YPOS):  pygame.draw.circle(screen, (40, 210, 250), ((x+xp)//2, (y+yp)//2), 290//XPOS)
				#~ elif (i > 0 and i < XPOS) and (j > 0 and j < YPOS): pygame.draw.circle(screen, (40, 210, 250), ((x+xp)//2, (y+yp)//2), x//XPOS)
				else: pygame.draw.circle(screen, (40, 210, 250), (((x + (x-xd))+xp)//2, (y+yp)//2), 290//2)
					
				
				if not seleccion in SELECT: SELECT.append(seleccion)
				
			if SelTemp[0] == LETRAS[i] and j == SelTemp[1] - 1:
				#~ print(seleccion[0], seleccion[1])
				
				print([i,j],SELECT)
				#~ os.system('Pause')
				pygame.draw.rect(screen, SELECCIONA, [x, y, dimension, dimension], 0)
			
			if i == 0: dibujarTexto(screen, str(j + 1), [p_inicio[0] - tamanio_fuente, j * dimension + p_inicio[1]], fuente, AZUL)
			
			#~ if [LETRAS[i],j] in SELECT: dibujarTexto(screen, Cont, [x, y], fuenteT, AZUL)
			
		dibujarTexto(screen, LETRAS[i], [i * dimension + p_inicio[0], p_inicio[1] - tamanio_fuente], fuente, AZUL)
		

def dibujarTexto(screen, texto, posicion, fuente, color):
	
    Texto = fuente.render(texto, 1, color)
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
            #~ print(i,j)
            if (xr >= x) and (xr <= x + dimension) and (yr >= y) and (yr <= y + dimension): actual = [LETRAS[i], j + 1]
    
    return actual


def obtenerPosicion(XPOS, YPOS, Dir, Actual):
	
	PosLetra = LETRAS.index(Actual[0])
	
	if Dir == 'U':
		
		if   Actual[0] in LETRAS and Actual[1] == 1: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(2,YPOS+1)]: Actual = [Actual[0],Actual[1]-1]
		
	elif Dir == 'D':
		
		if   Actual[0] in LETRAS and Actual[1] == YPOS: pass
		elif Actual[0] in LETRAS and Actual[1] in [x for x in range(1,YPOS)]: Actual = [Actual[0],Actual[1]+1]
		
	elif Dir == 'L':
		
		if   Actual[0] == LETRAS[0]  and Actual[1] in [x for x in range(1,YPOS+1)]:	pass
		elif Actual[0] in LETRAS[1:] and Actual[1] in [x for x in range(1,YPOS+1)]:	Actual = [LETRAS[PosLetra-1],Actual[1]]
		
	elif Dir == 'R':
		
		if   Actual[0] == LETRAS[XPOS-1]   and Actual[1] in [x for x in range(1,YPOS+1)]: pass
		elif Actual[0] in LETRAS[0:XPOS-1] and Actual[1] in [x for x in range(1,YPOS+1)]: Actual = [LETRAS[PosLetra+1],Actual[1]]
	
	return Actual

def EscribirEnCuadricula(XPOS, YPOS, screen, dimension, p_inicio, fuente, seleccion):
	
	for i in range(XPOS):
		
		for j in range(YPOS):
			
			x = i * dimension + p_inicio[0]
			y = j * dimension + p_inicio[1]
			
			dibujarTexto(screen, 'Informacion', [x, y], fuenteT, AZUL)
			

def main():
	
	FULL = False
	XPOS = 12
	YPOS = 12
	POS = (XPOS if XPOS > YPOS else YPOS)
	
	if XPOS > 1 and YPOS > 1: pass
	else: sys.exit(1)
	
	pygame.init()
	screen = pygame.display.set_mode(DIMENCIONES)
	pygame.display.set_caption("__Tablero__")
	game_over = False
	clock = pygame.time.Clock()
	tamanio_fuente = 30
	
	NombrePersonaje = ['Hombre','Mono','Pez']
	
	seleccion = ['A', 1]
	SelTemp = ['P',16]
	
	fuente  = pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", tamanio_fuente)
	fuenteT = pygame.font.Font("fuentes/Wendy.ttf",30)
	fuente2 = pygame.font.Font("fuentes/DroidSans.ttf", 16)
	
	puntoInicio, dimension = ajustarMedidas(POS, tamanio_fuente)
	
	#~ print(puntoInicio, dimension)
	
	while game_over is False:
		
		#~ MousePos = pygame.mouse.get_pos()
		
		for evento in pygame.event.get():
			
			if evento.type == pygame.QUIT: game_over = True
			
			elif evento.type == pygame.KEYDOWN:
				
				if   evento.key == pygame.K_LEFT:	seleccion = obtenerPosicion(XPOS, YPOS, 'L', seleccion)
				elif evento.key == pygame.K_RIGHT:	seleccion = obtenerPosicion(XPOS, YPOS, 'R', seleccion)
				elif evento.key == pygame.K_UP:		seleccion = obtenerPosicion(XPOS, YPOS, 'U', seleccion)
				elif evento.key == pygame.K_DOWN:	seleccion = obtenerPosicion(XPOS, YPOS, 'D', seleccion)
			
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
				print(pos)
				#~ if pos > []
				pygame.mouse.set_visible(False)
				SelTemp = seleccion
				
				SelTemp = obtenerPosicionClic(XPOS, YPOS, pos, dimension, puntoInicio, SelTemp)
				
			elif evento.type == pygame.MOUSEBUTTONUP:
				
				pygame.mouse.set_visible(True)
				SelTemp = ['P',16]
			
			#~ if pygame.mouse.get_cursor()
			
			#~ # El usuario deja de presionar la tecla
			#~ elif evento.type == pygame.KEYUP:
				#~ # Si es una de las flechas, resetea el vector a cero.
				#~ if evento.key == pygame.K_LEFT:
					#~ x_speed = 0
				#~ elif evento.key == pygame.K_RIGHT:
					#~ x_speed = 0
				#~ elif evento.key == pygame.K_UP:
					#~ y_speed = 0
				#~ elif evento.key == pygame.K_DOWN:
					#~ y_speed = 0
		
		screen.fill(FONDO)
		
		pygame.draw.rect(screen, NEGRO, [10, 10, 240, 580], 3)
		pygame.draw.line(screen, NEGRO, [10,40], [250,40], 3)
		
		dibujarTexto(screen, 'Informacion', [70, 15], fuenteT, AZUL)
		dibujarTexto(screen, 'Personaje: ' + NombrePersonaje[0], [12, 50], fuenteT, NEGRO)
		dibujarTexto(screen, 'Posicion Actual: ' + str(seleccion), [12, 70], fuenteT, NEGRO)
		
		dibujarTablero(XPOS, YPOS, screen, dimension, puntoInicio, tamanio_fuente, fuente, fuenteT, seleccion, SelTemp)
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()


if __name__ == "__main__":
    main()
