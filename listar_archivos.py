from listar_archivos_locales import listar_archivos_locales
from listar_archivos_remotos import listar_archivos_remotos

def mostrar_opciones()->None:
    print(
    '''
    1. Listar archivos locales
    2. Listar archivos de su drive

    '''  )

def validar_opcion_menu(opcion_menu: str)->str:
    while opcion_menu != "1" and opcion_menu != "2":
        mostrar_opciones()
        print("Ingreso invalido, vuelva a intentarlo")
        opcion_menu = input("Ingrese una opcion: ")

    return opcion_menu

def listar_archivos()->None:
    mostrar_opciones()
    opcion_menu = validar_opcion_menu(input("Ingrese una opcion: ")) #el return de la funcion es STR
    if opcion_menu.lower() == '1':
        listar_archivos_locales()
    
    else:
        listar_archivos_remotos()