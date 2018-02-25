

from tkinter import filedialog, Tk


Tk().withdraw()


def GetFileName():
	
	Nombre = filedialog.askopenfile(filetypes = (("Archivos de Texto","*.txt"),("Todos los Archivos","*.*")))
	
	if Nombre == None: return
	
	return Nombre.name


def GetFolderName():
	
	Directorio = filedialog.askdirectory()
	
	return Directorio


def GetSaveFileName(initialdir = "/"):
	
	if initialdir == None: Archivo = filedialog.asksaveasfilename(title = "Select file", filetypes = (("Archivos de Texto","*.txt"),("Todos los Archivos","*.*")))
		
	else: Archivo = filedialog.asksaveasfilename(initialdir = initialdir, title = "Select file",filetypes = (("Archivos de Texto","*.txt"),("Todos los Archivos","*.*")))
		
	return Archivo


