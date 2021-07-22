from service_drive import ARCHIVO_SECRET_CLIENT, obtener_servicio_drive
from json import dumps, loads

def listar_carpetas(servicio:str, id_carpeta_acceder:str)->None:
    files = servicio.files().list(fields='files(name, id, mimeType)', q="parents='{}'".format(id_carpeta_acceder)).execute().get('files')
    print("\nLas carpetas de su sub-carpeta de id {} son: ".format(id_carpeta_acceder))
    for datos_carpeta in files:
        if datos_carpeta['mimeType'] == 'application/vnd.google-apps.folder':
            print("Nombre de la carpeta: {} - ID de la carpeta: {}".format(datos_carpeta["name"], datos_carpeta["id"]))

def listar_archivos(servicio:str, id_carpeta_acceder:str)->None:
    files = servicio.files().list(fields='files(name, id, mimeType)', q="parents='{}'".format(id_carpeta_acceder)).execute().get('files')
    print("\nLos archivos de su sub-carpeta de id {} son: ".format(id_carpeta_acceder))
    for datos_carpeta in files:
        if datos_carpeta['mimeType'] != 'application/vnd.google-apps.folder':
            print("Nombre del archivo: {} - ID del archivo {} - Tipo de archivo: {}".format(datos_carpeta["name"], datos_carpeta["id"], datos_carpeta["mimeType"]))

def listar_todo(servicio:str, id_carpeta_acceder:str)->None:
    listar_archivos(servicio, id_carpeta_acceder)
    listar_carpetas(servicio, id_carpeta_acceder)

def checkear_sub_carpetas(servicio:str, id_carpeta_actual:str)->dict:
    carpetas_validas = {}
    files = servicio.files().list(fields='files(name, id, mimeType)', q="parents='{}'".format(id_carpeta_actual)).execute().get('files')
    for datos_carpeta in files:
        if datos_carpeta['mimeType'] == 'application/vnd.google-apps.folder':
            carpetas_validas[datos_carpeta['id']] = datos_carpeta['name']

    return carpetas_validas

def validar_ingreso_si_no(ingreso:str)->str: #SE USA EN EL OTRO ARCHIVO, BORRARLA DESPUES
    while ingreso.lower() != "si" and ingreso.lower() != "no":
        ingreso = input("Ingreso invalido, responda con si o no: ")

    return ingreso

def validar_opcion_navegar(opcion_navegar:str)->None: #SE USA EN EL OTRO ARCHIVO, BORRARLA DESPUES
    while opcion_navegar.lower() != "volver" and opcion_navegar.lower() != "acceder":
        print("Responda con acceder o volver")
        opcion_navegar = input("Desea acceder a alguna de las carpetas o desea volver para atras?: ")

    return opcion_navegar

def validar_carpeta_existente(carpeta_acceder:str, carpetas_validas:dict)->str:
    while not carpeta_acceder in carpetas_validas.values():
        print("La carpeta que ingreso no es valida, vuelva a intentarlo")
        carpeta_acceder = input("Ingrese la carpeta a la que quiere acceder: ")

    return carpeta_acceder

def validar_cantidad_ids(ids_carpeta_acceder:list )->str:
    if len(ids_carpeta_acceder) != 1:
        print("Tiene varias carpetas con el mismo nombre, los ids de las carpetas son estos:")
        for i in range(len(ids_carpeta_acceder)):
            print("ID {}: {}".format(i, ids_carpeta_acceder))

        print("Elija uno de los ids: ")
        id_elegido = input("Ingrese el ID con el que quiere quedarse: ")
        while not id_elegido in ids_carpeta_acceder:
            print("Ingreso invalido, copie y pegue el id con el que quiere quedarse: ")

        id_elegido = input("Ingrese el ID con el que quiere quedarse: ")

    else:
        id_elegido = ids_carpeta_acceder[0]

    return id_elegido

def ids_validos(carpeta_acceder:str, carpetas_validas:dict)->list:
    ids_validos = []
    for id, name in carpetas_validas.items():
        if carpeta_acceder == name:
            ids_validos.append(id)

    return ids_validos

def opcion_navegar_subcarpetas(servicio:str, carpetas_validas:dict, ids_carpetas_recorridas:list)->None:
    print("\nResponda con acceder o volver")
    opcion_navegar = validar_opcion_navegar(input("Desea acceder a alguna de las carpetas o desea volver para atras?: "))
    if opcion_navegar.lower() == "acceder":
        carpeta_acceder = validar_carpeta_existente(input("Ingrese la carpeta a la que quiere acceder: "), carpetas_validas)
        id_carpeta_acceder = validar_cantidad_ids(ids_validos(carpeta_acceder, carpetas_validas))
        listar_todo(servicio, id_carpeta_acceder)
        ids_carpetas_recorridas.append(id_carpeta_acceder)
            
    else:
        if len(ids_carpetas_recorridas) == 1:
            print("No puede volver mas atras, se encuentra en el drive inicial")

        else:
            ids_carpetas_recorridas.pop()
            id_carpeta_actual = ids_carpetas_recorridas[-1::1][0]
            listar_todo(servicio, id_carpeta_actual)

def listar_archivos_remotos()->None:
    servicio = obtener_servicio_drive() #Solo esto va afuera y en main, voy a pasarle siempre esto
    driveid = servicio.files().get(fileId='root').execute().get('id')
    listar_todo(servicio, driveid)
    ids_carpetas_recorridas = []
    ids_carpetas_recorridas.append(driveid)
    continuar = True
    while continuar: 
        id_carpeta_actual = ids_carpetas_recorridas[-1::1][0]
        carpetas_validas = checkear_sub_carpetas(servicio, id_carpeta_actual) #DICT - KEY=ID (str), VAL=NAME (str)
        if carpetas_validas.keys() != []: #Checkeo que de verdad haya subcarpetas p/ preg
            opcion_continuar = validar_ingreso_si_no(input("\nDesea navegar por las carpetas? "))

            if opcion_continuar.lower() == "si":
                opcion_navegar_subcarpetas(servicio, carpetas_validas, ids_carpetas_recorridas)
    
            else:
                continuar = False #No quiere seguir navegando
        else:
            #No hay subcarpetas para acceder
            if len(ids_carpetas_recorridas) > 1: 
            #No hay subcarpetas para acceder, pero se encuentra en una subcarpeta, puede volver
                opcion_volver = validar_ingreso_si_no(input("\nDesea volver para atras? (si/no): "))
                if opcion_volver.lower() == "si":
                    ids_carpetas_recorridas.pop()

                else:
                    continuar = False
            
            else: 
                continuar = False 
                #No solo no hay subcarpetas, sino que se encuentra en el el drive inicial, no
                #puede hacer nada