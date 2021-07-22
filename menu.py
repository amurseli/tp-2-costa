from crear_archivos import crear_archivo_nuevo
from descargar_archivo import descargar_archivos
from subir_archivo import subir_archivos
from seleccionar_carpeta import seleccionar_carpeta
from service_drive import obtener_servicio_drive
from service_gmail import obtener_servicio_gmail
from syncronizar import syncronizar
from listar_archivos import listar_archivos
#from sistema_carpeta import sistema_carpeta

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
            6) Generar carpetas de una evaluacion.
            7) Actualizar entregas de alumnos vía mail.
            8) Salir. 
            """)
        
        opcion = validar_opcion(1, 8)
        if opcion == 1:
            listar_archivos()
        elif opcion == 2:
            crear_archivo_nuevo(SERVICE_DRIVE)
        elif opcion == 3:
            subir_archivos(SERVICE_DRIVE)
        elif opcion == 4:
            descargar_archivos(SERVICE_DRIVE)
        elif opcion == 5:
            syncronizar()
        elif opcion == 6:
            print("Mail al que se le quiere enviar:")
            destinatario = input()
            asunto = "DATOS"
            mensaje = "    "
            enviar_mensaje(SERVICE_GMAIL,destinatario,asunto,mensaje)
 
            #sistema_carpeta()
        elif opcion == 7:
            print("Mail al que se le quiere enviar:")
            destinatario = input()
            asunto = "TENES ARCHIVOS"
            mensaje = "Se te enviaron archivos para que lo subas a tu carpeta drive"
            attachment = ['alumnos_docnetes.zip']
            enviar_mensaje_con_adjuntos(SERVICE_GMAIL, destinatario, asunto, mensaje, attachment)
                       
            #parte de drive
        elif opcion == 8:
            continuar = False 
main()
