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
        path = dirname(path)
        listar_todo_local(path)

    return path

def navegar_entre_carpetas(path:str)->None: 
    continuar =  True
    while continuar:
        sub_carpetas = checkear_subcarpetas(path)
        if sub_carpetas != []: #Checkeo que en verdad haya alguna sub carpeta para preguntar
            opcion_continuar = validar_ingreso_si_no(input("\nDesea navegar por las sub-carpetas?: "))
            if opcion_continuar.lower() == "si": 
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
    path = getcwd() 
    listar_todo_local(path)
    navegar_entre_carpetas(path)