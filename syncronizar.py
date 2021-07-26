from os import remove, getcwd, walk
from os.path import abspath, getmtime, split
from io import BytesIO
from shutil import move
from service_drive import obtener_servicio
from datetime import datetime
from mimetypes import guess_extension, guess_type
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

ID = 0
MIMETYPE = 1
NAME = 2
PARENTS = 3

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
    files = servicio.files().list(fields='files(name, id, modifiedTime, mimeType, parents)', q="mimeType!='application/vnd.google-apps.folder'").execute().get('files')
    for archivo in files:
        extension = guess_extension(archivo['mimeType']) #Devuelve la extension con el punto o none
        if extension != None:
            nombre_archivo = archivo['name'] + extension
            try:
               datos_remotos[nombre_archivo] = [archivo['id'], archivo['mimeType'], archivo['name'], archivo['parents'][0]]
            except:
                pass
            #Si hay archivos compartidos de otros drives, algunos de esos archivos no tienen el parametro
            #parents, el drive en el que testeo todo tiene muchos archivos compartidos, hago esto para que no
            #salte
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
    
def syncronizar()->None:
    #PD: omiti la palabra archivos en todas las varaibles pq sino quedaban demasiado largos los 
    #nombres
    path = getcwd()
    servicio = obtener_servicio()
    archivos_locales = todos_archivos_locales(path)
    paths_locales = archivos_locales[0]
    mtime_locales = archivos_locales[1]
    archivos_remotos = todos_archivos_remotos(servicio)
    datos_remotos = archivos_remotos[0]
    mtime_remotos = archivos_remotos[1]

    actualizar_archivos_comunes(mtime_locales, mtime_remotos, datos_remotos, paths_locales, servicio, path)  