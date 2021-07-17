from service_drive import obtener_servicio
from json import dumps, loads
from listar_archivos import validar_ingreso_si_no, validar_opcion_navegar

#DUMP = PONER BONITO
#LOAD = PASAR DE JSON A DICCIONARIO DE PYTHON
'''
"id": "10HAw-qZbXx4kQS8oBAtuFQZ-q90L9u04",
        "name": "61.03 - AM 2 (Sirne) (2021-06-29 at 10:05 GMT-7)",
        "mimeType": "application/vnd.google-apps.shortcut",
        "parents": [
            "1ZNFWQslerkyu2erbAPtoTYn4b-48Hgdw"
'''
def listar_carpetas_drive_inicial(servicio:str)->None:
    files = servicio.files().list(fields='files(name, id, mimeType)', q="mimeType='application/vnd.google-apps.folder'").execute().get('files')
    #.files.list() genera un https request, .execute lo ejecuta y me da un dict, .get me da el valor de
    #clave files (lista de diccionarios con los datos). El parametro q me filta los archivos que tengan
    #el mimeType de una carpeta
    print("\nLas carpetas existentes en su drive actual son: ")
    for datos_carpeta in files:
        print("Nombre de la carpeta: {} - ID de la carpeta: {}".format(datos_carpeta["name"], datos_carpeta["id"]))

def listar_archivos_drive_inicial(servicio:str)->None:
    files = servicio.files().list(fields='files(name, id, mimeType)', q="mimeType!='application/vnd.google-apps.folder'").execute().get('files')
    #Es igual a la funcion para listar carpetas, solo que pongo que el mimeType sea != del propio 
    #de las carpetas
    print("\nLos archivos existentes en su drive actual son: ")
    for datos_archivo in files:
        print("Nombre del archivo: {} - Tipo de archivo: {} - ID del archivo: {} ".format(datos_archivo["name"], datos_archivo["mimeType"], datos_archivo["id"]))

def listar_todo_drive_inicial(servicio:str)->None:
    listar_archivos_drive_inicial(servicio)
    listar_carpetas_drive_inicial(servicio)

def checkear_sub_carpetas(servicio:str, id_carpeta_actual:str)->dict:
    carpetas_validas = {}
    if id_carpeta_actual != " ":
        files = servicio.files().list(fields='files(name, id, mimeType)', q="parents={}".format(id_carpeta_actual)).execute().get('files')
        for datos_carpeta in files:
            if datos_carpeta['mimeType'] == 'application/vnd.google-apps.folder':
                carpetas_validas[datos_carpeta['id']] = datos_carpeta['name']
    
    else:
        files = servicio.files().list(fields='files(name, id, mimeType)', q="mimeType='application/vnd.google-apps.folder'").execute().get('files')
        for datos_carpeta in files:
            carpetas_validas[datos_carpeta['id']] = datos_carpeta['name']

    return carpetas_validas

def validar_carpeta_existente(carpeta_acceder:str, carpetas_validas:dict)->str:
    while not carpeta_acceder in carpetas_validas.values():
        print("La carpeta que ingreso no es valida, vuelva a intentarlo")
        carpeta_acceder = input("Ingrese la carpeta a la que quiere acceder: ")

    return carpeta_acceder

def ids_validos(carpeta_acceder:str, carpetas_validas:dict)->list:
    ids_validos = []
    for id, name in carpetas_validas.items():
        if carpeta_acceder == name:
            ids_validos.append(id)

    return ids_validos

def validar_cantidad_ids(ids_carpeta_acceder:list )->str:
    if len(ids_carpeta_acceder) != 1:
        print("Tiene varias carpetas con el mismo nombre, los ids de las carpetas son estos:")
        for i in range(len(ids_carpeta_acceder)):
            print("ID {}: {}".format(i, ids_carpeta_acceder))

        print("Elija uno de los ids: ")
        id_elegido = input("Ingrese el ID con el que quiere quedarse: ")
        while not id_elegido in carpeta_acceder:
            print("Ingreso invalido, copie y pegue el id con el que quiere quedarse: ")

        id_elegido = input("Ingrese el ID con el que quiere quedarse: ")

    else:
        id_elegido = ids_carpeta_acceder[0]

    return id_elegido

def listar_carpetas_subcarpetas(servicio:str, id_carpeta_acceder:str)->None:
    files = servicio.files().list(fields='files(name, id, mimeType)', q="parents={}".format(id_carpeta_acceder)).execute().get('files')
    for datos_carpeta in files:
        print("Las carpetas de su sub-carpeta de id {} son: ".format(id_carpeta_acceder))
        if datos_carpeta['mimeType'] == 'application/vnd.google-apps.folder':
            print("Nombre de la carpeta: {} - ID de la carpeta: {}".format(datos_carpeta["name"], datos_carpeta["id"]))

def listar_archivos_subcarpetas(servicio:str, id_carpeta_acceder:str)->None:
    files = servicio.files().list(fields='files(name, id, mimeType)', q="parents={}".format(id_carpeta_acceder)).execute().get('files')
    for datos_carpeta in files:
        print("Los archivos de su sub-carpeta de id {} son: ".format(id_carpeta_acceder))
        if datos_carpeta['mimeType'] != 'application/vnd.google-apps.folder':
            print("Nombre del archivo: {} - ID de la carpeta: {} - Tipo de archivo: {}".format(datos_carpeta["name"], datos_carpeta["id"], datos_carpeta["mimeType"]))

def listar_todo_subcarpetas(servicio:str, id_carpeta_acceder:str)->None:
    listar_archivos_subcarpetas(servicio, id_carpeta_acceder)
    listar_carpetas_subcarpetas(servicio, id_carpeta_acceder)

def encontrar_id_carpeta_actual(ids_carpetas_recorridas:list)->str:
    if ids_carpetas_recorridas == []:
        id_carpeta_actual = " "

    else:
        id_carpeta_actual = ids_carpetas_recorridas[-1:0:1]

    return id_carpeta_actual

def opcion_navegar_subcarpetas(servicio:str, carpetas_validas:dict, ids_carpetas_recorridas:list)->None:
    print("\nResponda con acceder o volver")
    opcion_navegar = validar_opcion_navegar(input("Desea acceder a alguna de las carpetas o desea volver para atras?: "))
    if opcion_navegar.lower() == "acceder":
        carpeta_acceder = validar_carpeta_existente(input("Ingrese la carpeta a la que quiere acceder: "), carpetas_validas)
        id_carpeta_acceder = validar_cantidad_ids(ids_validos(carpeta_acceder, carpetas_validas))
        listar_todo_subcarpetas(servicio, id_carpeta_acceder)
        ids_carpetas_recorridas.append(id_carpeta_acceder)

    else:
        if ids_carpetas_recorridas == []:
            print("No puede volver mas atras, se encuentra en el drive inicial")

        else:
            ids_carpetas_recorridas.pop()
            id_carpeta_actual = encontrar_id_carpeta_actual(ids_carpetas_recorridas)
            listar_todo_subcarpetas(servicio, id_carpeta_actual)

def listar_archivos_remotos()->None:
    servicio = obtener_servicio() #Solo esto va afuera y en main, voy a pasarle siempre esto
    listar_todo_drive_inicial(servicio)
    ids_carpetas_recorridas = []
    continuar = True
    while continuar: #No while true (HECHO)
        id_carpeta_actual = encontrar_id_carpeta_actual(ids_carpetas_recorridas)
        carpetas_validas = checkear_sub_carpetas(servicio, id_carpeta_actual) #DICT - KEY=ID (str), VAL=NAME (str)
        if carpetas_validas.keys() != []: #Checkeo que de verdad haya subcarpetas p/ preg
            opcion_continuar = validar_ingreso_si_no(input("Desea navegar por las carpetas? "))

            if opcion_continuar.lower() == "si":
                opcion_navegar_subcarpetas(servicio, carpetas_validas, ids_carpetas_recorridas)
    
            else:
                continuar = False #No quiere seguir navegando
        else:
            #No hay subcarpetas para acceder
            if ids_carpetas_recorridas != []: 
            #No hay subcarpetas para acceder, pero se encuentra en una subcarpeta, puede volver
                opcion_volver = validar_ingreso_si_no(input("Desea volver para atras? (si/no): "))
                if opcion_volver.lower() == "si":
                    ids_carpetas_recorridas.pop()

                else:
                    continuar = False
            
            else: 
                continuar = False 
                #No solo no hay subcarpetas, sino que se encuentra en el el drive inicial, no
                #puede hacer nada
                
listar_archivos_remotos()