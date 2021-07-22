<<<<<<< HEAD
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
            pass
        elif opcion == 2:
            pass
        elif opcion == 3:
            pass
        elif opcion == 4:
            pass
        elif opcion == 5:
            pass    
        elif opcion == 6:
            pass
        elif opcion == 7:
            pass
        elif opcion == 8:
            continuar = False 
=======
def menu()->None:

    continuar = True
    while continuar:
        print("Opciones")
        print("1. Listar archivos de la carpeta actual")
        print("2. Crear un archivo")
        print("3. Subir un archivo")
        print("4. Descargar un archivo")
        print("5. Sincronizar carpetas")
        print("6. Generar carpetas de una evaluacion")
        print("7. Actualizar entregas de alumnos v´ıa mail.")
        print("8. Salir")

        opcion = input("\nIngrese una opcion: ")
        while not opcion.isnumeric() and not int(opcion) > 8:
            print("Error! ingrese una respuesta valida")
            opcion = input("Error! ingrese una respuesta valida")

        if opcion == "1":
            pass
        elif opcion == '2':
            pass
        elif opcion == '3':
            pass
        elif opcion == '4':
            pass
        elif opcion == '5':
            pass
        elif opcion == '6':
            pass
        elif opcion == '7':
            pass
        elif opcion == '8':
            continuar = False

def main()->None:
    menu()
>>>>>>> ignacio
main()