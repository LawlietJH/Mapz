
from collections import deque
import os



class Arbol:
	
	
	def __init__(self, Coordenada):
		
		self.Coord = Coordenada		# Posición Del Nodo.
		self.Hijos = []				# Conexión a los Hijos.
		self.PHijos = []
		self.Padre = None
		self.Estado = 'Abierto'
		self.Orden = []
		self.EsIni = False
		self.EsFin = False
		
	def SetPadre(self, Padre):		self.Padre = Padre			# Posición del Padre, Ejemplo ['E',11] o N/A para el Estado Inicial.
	
	def SetHijos(self, Hijo):		self.PHijos.append(Hijo)	# Posiciones de los Hijos, Ejemplo: [['F',12], ['E',13], ['D',12], ].
	
	def SetEstado(self, Estado):	self.Estado = Estado		# Estado Actual del Nodo. (Abierto, Cerrado(Si todos sus hijos ya han sido visitados))
	
	def SetOrden(self, Orden):		self.Orden = Orden			# Orden de Visita, Ejemplo: [1,3,5,7,...]
	
	def SetIniFin(self, EsIni, EsFin):
		
		self.EsIni = EsIni		# True si el Nodo es Estado Inicial.
		self.EsFin = EsFin		# True si el Nodo es Estado Final.
	
	def GetDatos(self):
		
		return {
				'Objetos':self.Hijos,
				'Coordenadas':self.Coord,
				'Padre':self.Padre,
				'Hijos':self.PHijos,
				'Estado':self.Estado,
				'OrdenVisitas':self.Orden,
				'EsInicial':self.EsIni,
				'EsFinal':self.EsFin
			   }


def Agregar(arbol, Padre, Coord, NoRepetir=True, AlFinal=True):
	
	if NoRepetir:
		if Busqueda(arbol, Coord): return
	
	SubArbol = Recorrer(arbol, Padre, AlFinal)
	SubArbol.Hijos.append(Arbol(Coord))

#=======================================================================

def AgregarPadre(arbol, Coord, Padre):
	
	if Coord == arbol.Coord: arbol.SetPadre(Padre); return True
	for SubArbol in arbol.Hijos:
		if AgregarPadre(SubArbol, Coord, Padre): return True

def AgregarHijos(arbol, Coord, Hijo):
	
	if Coord == arbol.Coord: arbol.SetHijos(Hijo); return True
	for SubArbol in arbol.Hijos: 
		if AgregarHijos(SubArbol, Coord, Hijo): return True

def AgregarEstado(arbol, Coord, Estado):
	
	if Coord == arbol.Coord: arbol.SetEstado(Estado); return True
	for SubArbol in arbol.Hijos:
		if AgregarEstado(SubArbol, Coord, Estado): return True

def AgregarOrden(arbol, Coord, Orden):
	
	if Coord == arbol.Coord: arbol.SetOrden(Orden); return True
	for SubArbol in arbol.Hijos:
		if AgregarOrden(SubArbol, Coord, Orden): return True

def AgregarIniFin(arbol, Coord, EsIni=False, EsFin=False):
	
	if Coord == arbol.Coord: arbol.SetIniFin(EsIni, EsFin); return True
	for SubArbol in arbol.Hijos:
		if AgregarIniFin(SubArbol, Coord, EsIni, EsFin): return True

#=======================================================================

def Recorrer(arbol, Coord, AlFinal):
	
	if not AlFinal:
		if arbol.Coord == Coord: return arbol
	
	for SubArbol in arbol.Hijos:
		
		Encontrado = Recorrer(SubArbol, Coord, AlFinal)
		
		if Encontrado != None: return Encontrado
	
	if AlFinal:
		if arbol.Coord == Coord: return arbol
	
	return None


def Busqueda(arbol, Coord):
	
	if Coord == arbol.Coord: return True
	
	for SubArbol in arbol.Hijos:
		
		if Busqueda(SubArbol, Coord): return True
		
	return False


def BusquedaPrecisa(arbol, Padre, Coord):
	
	if Padre == 'N/A': return True
	
	if Padre == arbol.Coord:
		
		for x in range(len(arbol.Hijos)):
			
			if Coord == arbol.Hijos[x].Coord: return True
		
	for SubArbol in arbol.Hijos:
		
		if BusquedaPrecisa(SubArbol, Padre, Coord): return True
	
	return False


def Modificar(arbol, Coord, Padre, PHijos, Estado, Orden, EsIni, EsFin):
	
	if Coord == arbol.Coord:
		
		arbol.SetPadre(Padre)
		arbol.SetHijos(PHijos)
		arbol.SetEstado(Estado)
		arbol.SetOrden(Orden)
		arbol.SetIniFin(EsIni, EsFin)
		return True
		
	for SubArbol in arbol.Hijos:
		
		if Modificar(SubArbol, Coord, Padre, PHijos, Estado, Orden, EsIni, EsFin): return True
		
	return False


def ExtraerDatos(arbol, Padre, Coord):
	
	if Padre == 'N/A': return [True, arbol.GetDatos()]
	
	if Padre == arbol.Coord:
		
		for x in range(len(arbol.Hijos)):
			
			if Coord == arbol.Hijos[x].Coord: return [True, arbol.Hijos[x].GetDatos()]
			
	for SubArbol in arbol.Hijos:
		
		Val = ExtraerDatos(SubArbol, Padre, Coord)
		if Val[0]: return Val
		
	return [False, None]


def ActualizaEstado(arbol):
	
	if arbol.Estado == 'Abierto':
		
		xD = True
		
		if len(arbol.Hijos) == 0:
			
			if len(arbol.Orden) > 0: arbol.Estado = 'Cerrado'
			
		else:
			
			for SubArbol in arbol.Hijos:
				
				if len(SubArbol.Orden) == 0: xD = False
				
			if xD: arbol.Estado = 'Cerrado'		# Cerrado si todos sus hijos ya han sido visitados.
	
	for SubArbol in arbol.Hijos: ActualizaEstado(SubArbol)



def Tabs(Cont):
	
	if Cont == 101: print('\t', end='')
	if Cont == 102: print('\t| |' + '\t', end='')
	if Cont == 103: print('\t| |' *  2 + '\t', end='')
	if Cont == 104: print('\t| |' *  3 + '\t', end='')
	if Cont == 105: print('\t| |' *  4 + '\t', end='')
	if Cont == 106: print('\t| |' *  5 + '\t', end='')
	if Cont == 107: print('\t| |' *  6 + '\t', end='')
	if Cont == 108: print('\t| |' *  7 + '\t', end='')
	if Cont == 109: print('\t| |' *  8 + '\t', end='')
	if Cont == 110: print('\t| |' *  9 + '\t', end='')
	if Cont == 111: print('\t| |' * 10 + '\t', end='')
	if Cont == 112: print('\t| |' * 11 + '\t', end='')
	if Cont == 113: print('\t| |' * 12 + '\t', end='')
	if Cont == 114: print('\t| |' * 13 + '\t', end='')
	if Cont == 115: print('\t| |' * 14 + '\t', end='')
	if Cont == 116: print('\t| |' * 15 + '\t', end='')
	if Cont == 117: print('\t| |' * 16 + '\t', end='')
	if Cont == 118: print('\t| |' * 17 + '\t', end='')
	if Cont == 119: print('\t| |' * 18 + '\t', end='')
	if Cont == 120: print('\t| |' * 19 + '\t', end='')
	if Cont == 121: print('\t| |' * 20 + '\t', end='')
	if Cont == 122: print('\t| |' * 21 + '\t', end='')
	if Cont == 123: print('\t| |' * 22 + '\t', end='')
	if Cont == 124: print('\t| |' * 23 + '\t', end='')
	if Cont == 125: print('\t| |' * 24 + '\t', end='')
	if Cont == 126: print('\t| |' * 25 + '\t', end='')
	if Cont == 127: print('\t| |' * 26 + '\t', end='')
	if Cont == 128: print('\t| |' * 27 + '\t', end='')
	if Cont == 129: print('\t| |' * 28 + '\t', end='')
	if Cont == 130: print('\t| |' * 29 + '\t', end='')
	if Cont == 131: print('\t| |' * 30 + '\t', end='')
	if Cont == 132: print('\t| |' * 31 + '\t', end='')


def Anchura(arbol, funcion, cola = deque()):
	
	funcion(arbol.Coord)
	
	if (len(arbol.Hijos) > 0): cola.extend(arbol.Hijos)
	
	if (len(cola) != 0): Anchura(cola.popleft(), funcion, cola)


def Profundidad(arbol, Cont):
	
	Cont += 1
	
	# ~ print(arbol.Coord, 'Padre:', arbol.Padre, 'Hijos:', arbol.PHijos)
	# ~ print(arbol.GetDatos())
	print(arbol.Coord, arbol.Orden, arbol.Estado, arbol.PHijos)
	
	for hijo in arbol.Hijos:
		
		Tabs(Cont)
		Profundidad(hijo, Cont)


def ContadorDeNodos(arbol, Cont=-1):	# Cuenta Cuantos Nodos Hay En Un SubArbol a Partir de La Raiz Dada.
	
	Cont += 1
	
	for hijo in arbol.Hijos: Cont = ContadorDeNodos(hijo, Cont)
	
	return Cont


def ContadorDeNivel(arbol, Cont=-1, Max=0):		# Cuenta Cuantos Niveles de Profundidad Hay En Un SubArbol a Partir de La Raiz Dada.
	
	Cont += 1
	
	if Cont > Max: Max = Cont
	
	for hijo in arbol.Hijos: Max, Cont = ContadorDeNivel(hijo, Cont, Max)
	
	Cont -= 1
	
	return Max, Cont


def ImprimirArbol(raiz):
	
	Cont = 100
	os.system('Cls')
	
	# ~ print('\n\n\nLvl 1\tLvl 2\tLvl 3\tLvl 4\tLvl 5\tLvl 6\tLvl 7\tLvl 8\tLvl 9\tLvl 10\tLvl 11\tLvl 12\tLvl 13\tLvl 14\tLvl 15\n')
	
	Profundidad(raiz, Cont)


def printElement(Coord): print(Coord)

def Raiz(raiz): return Arbol(raiz)


if __name__ == "__main__":	# Datos de Prueba.
	
	raiz = Raiz('0')
	
	Agregar(raiz, '0', '1')
	Agregar(raiz, '1', '2')
	Agregar(raiz, '1', '3')
	Agregar(raiz, '1', '4')
	Agregar(raiz, '2', '5')
	Agregar(raiz, '4', '6')
	Agregar(raiz, '4', '7')
	
	AgregarPadre(raiz, '0', 'N/A')
	AgregarPadre(raiz, '1', '0')	
	AgregarPadre(raiz, '2', '1')
	AgregarPadre(raiz, '3', '1')
	AgregarPadre(raiz, '4', '1')
	AgregarPadre(raiz, '5', '2')
	AgregarPadre(raiz, '6', '4')
	AgregarPadre(raiz, '7', '4')
	
	AgregarHijos(raiz, '0', '1')
	for x in ['2','3','4']: AgregarHijos(raiz, '1', x)
	AgregarHijos(raiz, '2', '5')
	for x in ['6','7']: AgregarHijos(raiz, '4', x)
	
	AgregarOrden(raiz, '0', ['1'])
	AgregarOrden(raiz, '1', ['2'])
	AgregarOrden(raiz, '2', ['3','5'])
	AgregarOrden(raiz, '3', ['4'])
	AgregarOrden(raiz, '4', ['6'])
	AgregarOrden(raiz, '5', ['7'])
	
	ActualizaEstado(raiz)
	
	ImprimirArbol(raiz)
	
	print('\n\n\n [+] Desde La Raiz:')
	print('\n\n\n [+] Nodos:', ContadorDeNodos(raiz))
	print('\n\n\n [+] Niveles:', ContadorDeNivel(raiz)[1])
	
	# ~ print(BusquedaPrecisa(raiz, '4', '7'))
	
	# ~ print('Datos: ')
	
	# ~ Modificar(raiz, '0', None, None, 'Abierto', [1,3,5], False, False)
	
	# ~ Datos = ExtraerDatos(raiz, '101')
	
	# ~ print(Datos)
	
	
	

	# ~ pos = pygame.mouse.get_pos()	# Obtiene una Tupla con los Valores X y Y del Mouse, en Pixeles.
	# ~ xr, yr = pos[0], pos[1]		# Posición X y Y del Mouse por separado, Coordenadas por Pixeles.
	
	# ~ XX1 += MoveX
	# ~ YY1 += MoveY
	
	# ~ InicialX,InicialY = 500, 250
	# ~ TamX, TamY = 100, 100
	
	# ~ if  (InicialX + XX1 >= puntoInicio[0] - TamX) and (InicialX + XX1 <= puntoInicio[0] + dimension*XPOS)\
	# ~ and (InicialY + YY1 >= puntoInicio[1] - TamY) and (InicialY + YY1 <= puntoInicio[1] + dimension*YPOS):
		# ~ pygame.draw.rect(screen, COLOR['Blanco'], [InicialX+XX1, InicialY+YY1, TamX, TamY], 0)
		
