import os
from service_drive import obtener_servicio_drive
from service_gmail import obtener_servicio_gmail
from mandar_mensaje import enviar_mensaje
from mandar_mensaje import enviar_mensaje_con_adjuntos

SERVICE_DRIVE = obtener_servicio_drive()
SERVICE_GMAIL = obtener_servicio_gmail()

destinatario = input("Ingrese el mail al que desea enviarlo: ")
asunto = 'datos'
mensaje = 'informacion de crear la carpeta, eso pone come crear la carpeta'
attachment = 'el archivo.zip'

enviar_mensaje(SERVICE_GMAIL, destinatario, asunto, mensaje)
enviar_mensaje_con_adjuntos(SERVICE_GMAIL, destinatario, asunto, mensaje, attachment)

def sistema_carpeta():
    evaluacion = os.mkdir("Carpeta_Prueba")
    docente = os.mkdir("Carpeta_Prueba/Docentes")
    alumnos = os.mkdir("Carpeta_Prueba/Docentes/Alumnos")
    with open("Carpeta_Prueba/Docentes/Alumnos/Archivo.txt", "w") as files:
        elemento = files

service = obtener_servicio_drive()

from subir_archivo import subir_archivos
subir_archivos(service)