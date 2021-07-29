from os import listdir, getcwd, walk, remove
from os.path import join, isfile, isdir, split, dirname, getmtime, abspath
from io import BytesIO
from shutil import move
from datetime import datetime
from mimetypes import guess_extension, guess_type
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

ID = 0
MIMETYPE = 1
NAME = 2
PARENTS = 3

MIME_TYPES = [
    "text/plain",
    "image/jpeg",
    "audio/mpeg",
    'application/vnd.google-apps.folder',
    "application/json",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]

OPTIONS = [
    "1- Archivo de texto .txt",
    "2- Foto .jpg",
    "3- Audio .mp3",
    "4- Carpeta vacía",
    "5- Archivo json .json",
    "6- Microsoft Word .doc",
    "7- Microsoft Word OpenXML .docx",
    "8- Archivo Excel .xls",
    "9- Archivo Excel OpenXML .xlsx"
]

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

def modifi_sub_carpetas_local(sub_carpetas:list, path:str)->None:
    for carpeta in listdir(path):
        nuevo_path = join(path, carpeta)
        if isdir(nuevo_path):
            sub_carpetas.append(carpeta)

def checkear_subcarpetas_local(path:str)->list:
    sub_carpetas = []
    modifi_sub_carpetas_local(sub_carpetas, path)

    return sub_carpetas

def validar_ingreso_si_no(ingreso:str)->str:
    while ingreso.lower() != "si" and ingreso.lower() != "no":
        ingreso = input("Ingreso invalido, responda con si o no: ")

    return ingreso

def validar_carpeta_existente_local(sub_carpetas:list, carpeta_acceder:str)->str:
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
        carpeta_acceder = validar_carpeta_existente_local(sub_carpetas, input("\nIngrese la carpeta a la que quiere acceder: "))
        path = join(path, carpeta_acceder) #Se va modificando la var path que pase al principio
        listar_todo_local(path)

    else:
        path = dirname(path)
        listar_todo_local(path)

    return path

def navegar_entre_carpetas(path:str)->None: 
    continuar =  True
    while continuar:
        sub_carpetas = checkear_subcarpetas_local(path)
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

#DE ACA PARA ABAJO ES REMOTO

def listar_carpetas_remoto(servicio:str, id_carpeta_acceder:str)->None:
    pagina = None
    seguir_procesando = True
    while seguir_procesando:
        response = servicio.files().list(fields='files(name, id, mimeType)', 
                                        q="parents='{}'".format(id_carpeta_acceder), 
                                        pageSize=1000, 
                                        supportsAllDrives=True,
                                        pageToken=pagina,
                                        includeItemsFromAllDrives=True).execute()

        pagina = response.get('nextPageToken', None)
        if pagina is None:
            seguir_procesando = False
    
    files = response.get('files')
    print("\nLas carpetas de su sub-carpeta son: ")
    for datos_carpeta in files:
        if datos_carpeta['mimeType'] == 'application/vnd.google-apps.folder':
            print("Nombre de la carpeta: {}".format(datos_carpeta["name"]))

def listar_archivos_remoto(servicio:str, id_carpeta_acceder:str)->None:
    pagina = None
    seguir_procesando = True
    while seguir_procesando:
        response = servicio.files().list(fields='files(name, id, mimeType)', 
                                        q="parents='{}'".format(id_carpeta_acceder), 
                                        pageSize=1000, 
                                        supportsAllDrives=True,
                                        pageToken=pagina,
                                        includeItemsFromAllDrives=True).execute()

        pagina = response.get('nextPageToken', None)
        if pagina is None:
            seguir_procesando = False
    
    files = response.get('files')
    print("\nLos archivos de su sub-carpeta son: ")
    for datos_carpeta in files:
        if datos_carpeta['mimeType'] != 'application/vnd.google-apps.folder':
            print("Nombre del archivo: {} - Tipo de archivo: {}".format(datos_carpeta["name"], datos_carpeta["mimeType"]))

def listar_todo_remoto(servicio:str, id_carpeta_acceder:str)->None:
    listar_archivos_remoto(servicio, id_carpeta_acceder)
    listar_carpetas_remoto(servicio, id_carpeta_acceder)

def checkear_sub_carpetas_remoto(servicio:str, id_carpeta_actual:str)->dict:
    carpetas_validas = {}
    files = servicio.files().list(fields='files(name, id, mimeType)', q="parents='{}'".format(id_carpeta_actual)).execute().get('files')
    for datos_carpeta in files:
        if datos_carpeta['mimeType'] == 'application/vnd.google-apps.folder':
            carpetas_validas[datos_carpeta['id']] = datos_carpeta['name']

    return carpetas_validas

def validar_carpeta_existente_remoto(carpeta_acceder:str, carpetas_validas:dict)->str:
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

def opcion_navegar_subcarpetas_remoto(servicio:str, carpetas_validas:dict, ids_carpetas_recorridas:list)->None:
    print("\nResponda con acceder o volver")
    opcion_navegar = validar_opcion_navegar(input("Desea acceder a alguna de las carpetas o desea volver para atras?: "))
    if opcion_navegar.lower() == "acceder":
        carpeta_acceder = validar_carpeta_existente_remoto(input("Ingrese la carpeta a la que quiere acceder: "), carpetas_validas)
        id_carpeta_acceder = validar_cantidad_ids(ids_validos(carpeta_acceder, carpetas_validas))
        listar_todo_remoto(servicio, id_carpeta_acceder)
        ids_carpetas_recorridas.append(id_carpeta_acceder)
            
    else:
        if len(ids_carpetas_recorridas) == 1:
            print("No puede volver mas atras, se encuentra en el drive inicial")

        else:
            ids_carpetas_recorridas.pop()
            id_carpeta_actual = ids_carpetas_recorridas[-1::1][0]
            listar_todo_remoto(servicio, id_carpeta_actual)

def listar_archivos_remotos(servicio:tuple)->None:
    driveid = servicio.files().get(fileId='root').execute().get('id')
    listar_todo_remoto(servicio, driveid)
    ids_carpetas_recorridas = []
    ids_carpetas_recorridas.append(driveid)
    continuar = True
    while continuar: 
        id_carpeta_actual = ids_carpetas_recorridas[-1::1][0]
        carpetas_validas = checkear_sub_carpetas_remoto(servicio, id_carpeta_actual) #DICT - KEY=ID (str), VAL=NAME (str)
        if carpetas_validas.keys() != []: #Checkeo que de verdad haya subcarpetas p/ preg
            opcion_continuar = validar_ingreso_si_no(input("\nDesea navegar por las carpetas? "))

            if opcion_continuar.lower() == "si":
                opcion_navegar_subcarpetas_remoto(servicio, carpetas_validas, ids_carpetas_recorridas)
    
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

def listar_archivos(servicio:tuple)->None:
    mostrar_opciones()
    opcion_menu = validar_opcion_menu(input("Ingrese una opcion: ")) #el return de la funcion es STR
    if opcion_menu.lower() == '1':
        listar_archivos_locales()
    
    else:
        listar_archivos_remotos(servicio)

#DE ACA PARA ABAJO ES SINCRONIZAR

def todos_archivos_locales(path:str)->tuple:
    paths_locales = {}
    mtime_locales = {}
    for root, dirs, files in walk(path):
        for archivo in files:
            try:
                fecha_unix = getmtime(root)
                fecha_normalizada = datetime.fromtimestamp(fecha_unix)
                mtime_locales[archivo] = fecha_normalizada
            except:
                pass
            #Hay archivos que son propios de git y estan ocultos, al parecer no tienen fecha de modificacion
            #y al hacer esto me tira un error
            if archivo in mtime_locales.keys():
                paths_locales[archivo] = split(root)[0]
        
    return paths_locales, mtime_locales

def todos_archivos_remotos(servicio:tuple)->dict:
    datos_remotos = {}
    mtime_remotos = {}
    pagina = None
    seguir_procesando = True
    while seguir_procesando:
        response = servicio.files().list(fields='files(name, id, modifiedTime, mimeType, parents)',
                                        q="mimeType!='application/vnd.google-apps.folder'",
                                        pageSize=1000, 
                                        supportsAllDrives=True,
                                        pageToken=pagina,
                                        includeItemsFromAllDrives=True).execute()

        pagina = response.get('nextPageToken', None)
        if pagina is None:
            seguir_procesando = False
    
    files = response.get('files')
    for archivo in files:
        extension = guess_extension(archivo['mimeType']) #Devuelve la extension con el punto o none
        if extension != None:
            nombre_archivo = archivo['name'] + extension
            try:
               datos_remotos[nombre_archivo] = [archivo['id'], archivo['mimeType'], archivo['name'], archivo['parents'][0]]
            except:
                pass
            
            mtime_remotos[nombre_archivo] = archivo['modifiedTime']
        
    return datos_remotos, mtime_remotos  

def obtener_mimetype(nombre_archivo:str)->str:
    mimetype_corresp = guess_type(nombre_archivo) 
    
    return mimetype_corresp[0]

def subir_archivo(servicio:tuple, datos_remotos:dict, archivo:str, mimetype_corresp:str)->None:
    file_metadata = {'name' : archivo, 'parents' : [datos_remotos[archivo][PARENTS]]}
    media_content = MediaFileUpload(archivo, mimetype='{}'.format(mimetype_corresp) )

    servicio.files().create(body=file_metadata, media_body=media_content).execute()

def borrar_archivo_remoto(servicio:tuple, datos_remotos: dict, archivo:str)->None:
    servicio.files().delete(fileId='{}'.format(datos_remotos[archivo][ID])).execute()

def bajar_archivo(servicio:tuple, datos_remotos:dict, archivo:str)->None:
    request = servicio.files().get_media(fileId=datos_remotos[archivo][ID])
    fh = BytesIO() 
    MediaIoBaseDownload(fd=fh, request=request)
    fh.seek(0)
    with open(abspath(archivo), 'wb') as f:
        f.write(fh.read())

def mover_archivo(archivo:str, paths_locales:dict)->None:
    path_actual = abspath(archivo) 
    path_deseado = paths_locales[archivo] #es la ubicacion del archivo borrado
    move(path_actual, path_deseado)

def actualizar_archivos_comunes(mtime_locales:dict, mtime_remotos:dict, datos_remotos:dict, paths_locales:dict, servicio:tuple, path:str)->None:
    for archivo in mtime_locales:
        if archivo in mtime_remotos:
            if mtime_locales[archivo] > mtime_remotos[archivo]:
                mimetype_corresp = obtener_mimetype(archivo)
                subir_archivo(servicio, datos_remotos, archivo, mimetype_corresp)
                borrar_archivo_remoto(servicio, datos_remotos, archivo)
    
            elif mtime_locales[archivo] < mtime_remotos[archivo]:
                remove(archivo) #Lo borro a nivel local
                bajar_archivo(servicio, datos_remotos, archivo)
                mover_archivo(archivo, paths_locales)

    print("\nSe han sincronizado los archivos comunes entre su carpeta {} y su drive".format(path))
    
def syncronizar(servicio:tuple)->None:
    #PD: omiti la palabra archivos en todas las varaibles pq sino quedaban demasiado largos los 
    #nombres
    path = getcwd()
    archivos_locales = todos_archivos_locales(path)
    paths_locales = archivos_locales[0]
    mtime_locales = archivos_locales[1]
    archivos_remotos = todos_archivos_remotos(servicio)
    datos_remotos = archivos_remotos[0]
    mtime_remotos = archivos_remotos[1]

    actualizar_archivos_comunes(mtime_locales, mtime_remotos, datos_remotos, paths_locales, servicio, path)

#DE ACA PARA ABAJO PARTE AGUSTIN

def seleccionar_carpeta(service, flag_empty = False) -> tuple:
    folder_id = " "
    flag_root = True
    files = service.files().list(fields='files(name, id, mimeType)',q="mimeType='application/vnd.google-apps.folder'").execute().get('files')
    i = 0
    for element in files:
        for key,value in element.items():
            if key == "name":
                print (f"-{value}")
    if flag_empty == True:
        print("Se seleccionó un directorio Vacío, Intentelo denuevo")
    print("Recuerde que si desea el direcotrio raíz, no complete el siguiente campo")
    name = input("Porfavor copie y pegue el nombre de la carpeta que desea.")

    for element in files:
        for key,value in element.items():
            if element[key] == name:
                target_file = element
                folder_id = target_file["id"] 
                flag_root = False

    
    
    return (folder_id, flag_root)

def descargar_archivos(service) -> None:
    file_id, file_name = seleccionar_archivo(service)
    request = service.files().get_media(fileId=file_id)
    fh = BytesIO()
        
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False

    print("Seleccione una Carpeta en la ventan que se acaba de abrir. Es posible que no se haya abierto en primer plano.")
    path = askdirectory(title='Seleccione una carpeta') 

    try:
        # Descarga la info "Chunk por Chunk"
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        with open(f"{path}\\{file_name}", 'wb') as f:
            f.write(fh.read())                       #Reescribe el archivo creado en al linea anterior con la ingormación en fh

        print("Archivo Descargado con éxito!")
    except :
    
        print("Algo salió Mal.")
        print("Es probable que estes intentando descargar un archivo no descargable.")
        print("Algunos de los archivos no descargables son los que fueron editados por las aplicaciones de drive como 'Google Docs' o 'Goggle Sheets'")
        return False

def seleccionar_archivo(service) -> tuple:
    file_id = ""
    folder_id, flag_root = seleccionar_carpeta(service)
    if flag_root == False:
        query = f"parents = '{folder_id}'"
        files = service.files().list(fields='files(name, id, mimeType)',q=query).execute().get('files')
        while bool(files) == False:
            folder_id, flag_root = seleccionar_carpeta(service, True)
            query = f"parents = '{folder_id}'"
            files = service.files().list(fields='files(name, id, mimeType)',q=query).execute().get('files')
        for element in files:
            for key,value in element.items():
                if key == "name":
                    print (f"-{value}")
    else:
        files = service.files().list(fields='files(name, id, mimeType)').execute().get('files')
        for element in files:
            for key,value in element.items():
                if key == "name":
                    print (f"-{value}")

    while file_id == "":
        file_name = input("Porfavor copie y pegue el nombre del archivo a descargar.")  

        for element in files:
            for key,value in element.items():
                if element[key] == file_name:
                    target_file = element
                    file_id = target_file["id"] 
    return (file_id,file_name)

def crear_archivo(service) -> None:
    folder_id, flag_root = seleccionar_carpeta(service)
    new_file_name = input("Escriba el nombre que quiere darle a su archivo, sin su extension: ")
    for element in OPTIONS:
        print (element)
    file_ext_choice = int(input("Seleccione un número correspondiente al tipo de archivo que desea subir: ")) - 1
    if flag_root == True:
        file_metadata = {
            'name': new_file_name,
            'mimeType': MIME_TYPES[file_ext_choice],
        }
    else:
        file_metadata = {
            'name': new_file_name,
            'mimeType': MIME_TYPES[file_ext_choice],
            "parents": [folder_id]
        }
    service.files().create(body=file_metadata).execute()
    print("¡El archivo fue creado con éxito!")

def subir_archivos_drive(service) -> None:
    folder_id, flag_root = seleccionar_carpeta(service)

    print("Seleccione un archivo en la ventan que se acaba de abrir. Es posible que no se haya abierto en primer plano.")
    path = askopenfilename(title='Seleccione un archivo') 
    path_split = path.split("/") # Crea una lista con las partes del path
    file_name = path_split[-1] # y guarda el último de los elementos en una variable

    mime_type, encoding = guess_type(path, strict=True) # guess_type() utiliza el path que le de y te devuelve su mimetype y su encoding
    #El parámetro strict limita los mimetypes solo a los oficiales

    if flag_root == False:
        file_metadata = {
            "name" : file_name,
            "parents" : [folder_id]
        }
    else:
        file_metadata = {
            "name" : file_name,
        }

    media = MediaFileUpload(path, mimetype=mime_type)

    try:
        service.files().create(
            body = file_metadata,
            media_body = media,
            fields = "id"
        ).execute()

        print("\nEl archivo se subió Exitosamente")
    except TypeError: #Esta excepcion ocurre si el mime_type.guess_type falla
        print("\nOcurrió un error al subir el archivo, puede que el mismo tenga la extensión cambiada.")