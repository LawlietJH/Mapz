
from collections import deque
import os



class Arbol:
	
    def __init__(self, Elemento):
		
        self.Elem = Elemento
        self.Hijos = []


def Append(arbol, Elem, Padre):
	
	if Busqueda(arbol, Elem): return
	
	SubArbol = Recorrer(arbol, Padre);
	SubArbol.Hijos.append(Arbol(Elem))


def Recorrer(arbol, Elem):
	
	if arbol.Elem == Elem: return arbol
	
	for SubArbol in arbol.Hijos:
		
		Encontrado = Recorrer(SubArbol, Elem)
		
		if Encontrado != None: return Encontrado
	
	return None


def Tabs(Cont):
	
	if Cont == 101: print('\t', end='')
	if Cont == 102: print('\t| |\t', end='')
	if Cont == 103: print('\t| |\t| |\t', end='')
	if Cont == 104: print('\t| |\t| |\t| |\t', end='')
	if Cont == 105: print('\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 106: print('\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 107: print('\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 108: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 109: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 110: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 111: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 112: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 113: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 114: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 115: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')
	if Cont == 116: print('\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t| |\t', end='')


def Busqueda(arbol, Elem):
	
	if Elem == arbol.Elem: return True
	
	for SubArbol in arbol.Hijos:
		
		if Busqueda(SubArbol, Elem): return True
		
	return False


def Anchura(arbol, funcion, cola = deque()):
	
	funcion(arbol.Elem)
	
	if (len(arbol.Hijos) > 0): cola.extend(arbol.Hijos)
	
	if (len(cola) != 0): Anchura(cola.popleft(), funcion, cola)


def Profundidad(arbol, Cont):
	
	Cont += 1
	
	print(arbol.Elem)
	
	for hijo in arbol.Hijos:
		
		Tabs(Cont)
		Profundidad(hijo, Cont)
		
	Cont -= 1


def ImprimirArbol(raiz):
	
	Cont = 100
	os.system('Cls')
	
	print('\n\n\nLvl 1\tLvl 2\tLvl 3\tLvl 4\tLvl 5\tLvl 6\tLvl 7\tLvl 8\tLvl 9\tLvl 10\tLvl 11\tLvl 12\tLvl 13\tLvl 14\tLvl 15\n')
	
	Profundidad(raiz, Cont)


def printElement(Elem): print(Elem)

def Raiz(raiz): return Arbol(raiz)

def Agregar(raiz, Elem, Padre): Append(raiz, Elem, Padre)



if __name__ == "__main__":	# Datos de Prueba.
	
	raiz = Raiz('0')
	
	Agregar(raiz, '1','0')
	Agregar(raiz, '31','0')
	Agregar(raiz, '21','0')
	Agregar(raiz, '27','1')
	Agregar(raiz, '23','1')
	Agregar(raiz, '2','1')
	Agregar(raiz, '3','2')
	Agregar(raiz, '9','1')
	Agregar(raiz, '4','2')
	Agregar(raiz, '5','3')
	Agregar(raiz, '11','3')
	Agregar(raiz, '6','3')
	Agregar(raiz, '7','4')
	Agregar(raiz, '8','5')
	Agregar(raiz, '26','27')
	Agregar(raiz, '33','6')
	Agregar(raiz, '34','6')
	Agregar(raiz, '36','27')
	Agregar(raiz, '45','36')
	Agregar(raiz, '47','36')
	Agregar(raiz, '32','27')
	Agregar(raiz, '101','45')
	Agregar(raiz, '102','45')
	Agregar(raiz, '103','45')
	Agregar(raiz, '200','9')
	Agregar(raiz, '16','47')
	Agregar(raiz, '17','101')
	
	ImprimirArbol(raiz)
	
	
	
