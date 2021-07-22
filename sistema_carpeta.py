import os
from service_drive import obtener_servicio_drive

evaluacion = os.mkdir("Carpeta_Prueba")
docente = os.mkdir("Carpeta_Prueba/Docentes")
alumnos = os.mkdir("Carpeta_Prueba/Docentes/Alumnos")
with open("Carpeta_Prueba/Docentes/Alumnos/Archivo.txt", "w") as files:
    elemento = files

service = obtener_servicio_drive()

from subir_archivos import subir_archivos
subir_archivos(service)