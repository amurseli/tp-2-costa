from service_drive import obtener_servicio_drive
from service_gmail import obtener_servicio_gmail
from modulo_drive import descargar_archivos, seleccionar_carpeta, syncronizar, listar_archivos, subir_archivos_drive, crear_archivo
from modulo_gmail import enviar_mensajes, enviar_mensaje_con_adjunto, carpetas_anidadas

SERVICE_DRIVE = obtener_servicio_drive()
SERVICE_GMAIL = obtener_servicio_gmail()

def validar_opcion(minimo: int, maximo: int) -> int:
    opcion = int(input("Ingrese un numero de opcion: "))
    while not opcion in range(minimo, maximo + 1):
        print("Error. Intentelo nuevamente.")
        opcion = int(input("Ingrese un numero de opcion: "))
    
    return int(opcion)


def main() -> None:
    continuar = True
    while continuar:
        print(
            """ 
            1) Listar archivos de la carpeta actual.
            2) Crear un archivo.
            3) Subir un archivo.
            4) Descargar un archivo.
            5) Sincronizar.
            6) Generar carpetas de una evaluacion.
            7) Actualizar entregas de alumnos vía mail.
            8) Salir. 
            """)
        
        opcion = validar_opcion(1, 8)
        if opcion == 1:
            listar_archivos(SERVICE_DRIVE)
        elif opcion == 2:
            crear_archivo(SERVICE_DRIVE)
        elif opcion == 3:
            subir_archivos_drive(SERVICE_DRIVE)
        elif opcion == 4:
            descargar_archivos(SERVICE_DRIVE)
        elif opcion == 5:
            syncronizar(SERVICE_DRIVE)
        elif opcion == 6:
            subject= enviar_mensaje_con_adjunto(SERVICE_GMAIL)
            carpetas_anidadas(subject)
        elif opcion == 7:
            enviar_mensajes(SERVICE_GMAIL)
            subir_archivos_drive(SERVICE_DRIVE)
        elif opcion == 8:
            print("Saliendo del programa")
            continuar = False 

main()