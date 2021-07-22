from os import listdir, getcwd
from os.path import join, isfile, isdir, split, dirname

def mostrar_archivos_local(path:str)->None:
    print("\nCarpeta actual: {}".format(path))
    print("Lista de archivos que se encuentran en su carpeta actual:\n")
    for archivo in listdir(path):
        nuevo_path = join(path, archivo)
        if isfile(nuevo_path):
            print(archivo)

def mostrar_carpetas_local(path:str)->None:
    print("\nCarpeta actual: {}".format(path))
    print("Lista de sub-carpetas que se encuentran en su carpeta actual:\n")
    for carpeta in listdir(path):
        nuevo_path = join(path, carpeta)
        if isdir(nuevo_path):
            print(carpeta)

def listar_todo_local(path:str)->None:
    mostrar_archivos_local(path)
    mostrar_carpetas_local(path)

def modifi_sub_carpetas(sub_carpetas:list, path:str)->None:
    for carpeta in listdir(path):
        nuevo_path = join(path, carpeta)
        if isdir(nuevo_path):
            sub_carpetas.append(carpeta)

def checkear_subcarpetas(path:str)->list:
    sub_carpetas = []
    modifi_sub_carpetas(sub_carpetas, path)

    return sub_carpetas

def validar_ingreso_si_no(ingreso:str)->str:
    while ingreso.lower() != "si" and ingreso.lower() != "no":
        ingreso = input("Ingreso invalido, responda con si o no: ")

    return ingreso

def validar_carpeta_existente(sub_carpetas:list, carpeta_acceder:str)->str:
    while not carpeta_acceder in sub_carpetas:
        print("La carpeta que indico no existe, vuelva a intentarlo")
        carpeta_acceder = input("Ingrese la carpeta a la que quiere acceder: ")

    return carpeta_acceder

def validar_opcion_navegar(opcion_navegar:str)->None:
    while opcion_navegar.lower() != "volver" and opcion_navegar.lower() != "acceder":
        print("Responda con acceder o volver")
        opcion_navegar = input("Desea acceder a alguna de las carpetas o desea volver para atras?: ")

    return opcion_navegar

def opcion_navegar(path:str, sub_carpetas:list)->str:
    print("\nResponda con acceder o volver")
    opcion_navegar = validar_opcion_navegar(input("Desea acceder a alguna de las carpetas o desea volver para atras?: "))
    if opcion_navegar.lower() == "acceder":
        carpeta_acceder = validar_carpeta_existente(sub_carpetas, input("\nIngrese la carpeta a la que quiere acceder: "))
        path = join(path, carpeta_acceder) #Se va modificando la var path que pase al principio
        listar_todo_local(path)

    else:
        #PD: se puede usar os.path.split(path) para obtener una tupla (path, carpeta)
        #y mostrarle la carpeta de la que acaba de salir, pero ya en los prints le muestro donde
        #esta parado, asi que creo que no hace falta
        path = dirname(path)
        listar_todo_local(path)

    return path

def navegar_entre_carpetas(path:str)->None: 
    #1. Ver de modularizar un toque mas, esta medio largo, debajo de c/for que hace una accion se puede
    #pd: recordar retornar el path nuevo e igualarlo a path para que funciona la logica  (Hecho)
    #2. Ver de validar que no pueda volver mas atras de la carpeta en la que inicio, usar el len del
    #path original p/eso (PREGUNTAR SI HACE FALTA)
    continuar =  True
    while continuar:
        sub_carpetas = checkear_subcarpetas(path) #["SUB-CARPETA", "SUB-CARPETA", ...] Lista de STRs
        #Se checkea para c/iteracion del ciclo, para que asi no me guarde la lista de carpetas
        #anterior y solo se muestren las carpetas de la direc actual
        if sub_carpetas != []: #Checkeo que en verdad haya alguna sub carpeta para preguntar
            opcion_continuar = validar_ingreso_si_no(input("\nDesea navegar por las sub-carpetas?: "))
            if opcion_continuar.lower() == "si": 
                #Solo se pregunta c/vez que se ejecuta el ciclo
                #(se ejecuta unicamente si HAY sub-carpetas la preg si quiere cerrar, sino cierra de una)
                path = opcion_navegar(path, sub_carpetas)
            else:
                continuar = False

        else:
            opcion_volver = validar_ingreso_si_no(input("\nDesea volver para atras?: "))
            if opcion_volver == "si":
                path = dirname(path)
                listar_todo_local(path)

            else:
                continuar = False 

def listar_archivos_locales()->None:
    path = getcwd() #Carpeta actual
    listar_todo_local(path)
    navegar_entre_carpetas(path)