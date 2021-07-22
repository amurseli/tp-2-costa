import os

def sistema_carpeta():
    evaluacion = os.mkdir("Evaluacion")
    docente = os.mkdir("Evaluacion/Docentes")
    alumnos = os.mkdir("Evaluacion/Docentes/Alumnos")
    with open("Evaluacion/Docentes/Alumnos/Archivo.txt", "w") as files:
        elemento = files
        
""" sistema_carpeta()
print("Se creo el sistema de carpetas en local") """