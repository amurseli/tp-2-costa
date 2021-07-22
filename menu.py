from crear_archivos import crear_archivo_nuevo
from descargar_archivo import descargar_archivos
from subir_archivo import subir_archivos
from seleccionar_carpeta import seleccionar_carpeta
from service_drive import obtener_servicio_drive
from service_gmail import obtener_servicio_gmail
from syncronizar import syncronizar
from listar_archivos import listar_archivos
from mandar_mensaje import enviar_mensaje, enviar_mensaje_con_adjuntos
from sistema_carpeta import sistema_carpeta

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
<<<<<<< HEAD
            print("Mail al que se le quiere enviar: ej:'example@algo.com'")
=======
            service = SERVICE_GMAIL
            print("Mail al que se le quiere enviar: ej: example@algo.com ")
>>>>>>> 47b96f0f2b6e05d9550ab811049ff05a4c0cfca1
            destinatario = input()
            asunto = "DATOS"
            mensaje = "A continuacion se creara en local evaluacion/docentes/alumnos y tambien una carpeta remota en drive y elija la opcion 4 para crear en remoto"
            enviar_mensaje(SERVICE_GMAIL,destinatario,asunto,mensaje)
            sistema_carpeta()
            
        elif opcion == 7:
<<<<<<< HEAD
            print("Mail eal que se le quiere enviar: ej:'example@algo.com'")
=======
            service = SERVICE_GMAIL
            print("Mail eal que se le quiere enviar: ej: example@algo.com")
>>>>>>> 47b96f0f2b6e05d9550ab811049ff05a4c0cfca1
            destinatario = input()
            asunto = "TENES ARCHIVOS"
            mensaje = "Se te enviaron archivos para que lo subas a tu carpeta drive"
            attachment = ['alumnos_docentes.zip']
            enviar_mensaje_con_adjuntos(SERVICE_GMAIL, destinatario, asunto, mensaje, attachment)
                       
            #parte de drive
        elif opcion == 8:
            continuar = False 
main()
