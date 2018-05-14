

# v1.2.0

import os
from tkinter import filedialog, Tk


Tk().withdraw()


class Explorer():
	
	def GetFileName( FileTypes=[ ['Archivos de Texto','.txt'], ['Todos los Archivos','.*'] ], Titulo='', DirInicial=os.getcwd() ):
		
		Nombre = filedialog.askopenfile(
											title		=	Titulo,
											initialdir	=	DirInicial,
											filetypes	=	FileTypes
									   )
		
		if Nombre == None: return
		
		return Nombre.name
	
	
	def GetFolderName( Titulo='', DirInicial=os.getcwd() ):
		
		Directorio = filedialog.askdirectory(
												initialdir	=	DirInicial,
												title		=	Titulo
											)
		
		return Directorio
	
	
	def GetSaveFileName( FileTypes=[ ['Archivos de Texto','.txt'], ['Todos los Archivos','.*'] ], Titulo='', DirInicial=os.getcwd() ):
		
		Nombre = filedialog.asksaveasfilename(
												title		=	Titulo,
												initialdir	=	DirInicial,
												filetypes	=	FileTypes
											 )
		
		if Nombre == None: return
		
		return Nombre




