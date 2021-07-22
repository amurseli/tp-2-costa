from os import remove, getcwd, walk
from os.path import abspath, getmtime
from io import BytesIO
from shutil import move
from service_drive import obtener_servicio_drive
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
                fecha_unix = getmtime(archivo)
                fecha_normalizada = datetime.fromtimestamp(fecha_unix)
                mtime_locales[archivo] = type(fecha_normalizada)
            except:
                pass
            #Hay archivos que son propios de git y estan ocultos, al parecer no tienen fecha de modificacion
            #y al hacer esto me tira un error, por eso dejo esto asi. Lo de abajo es para que no 
            #haya diferencias entre los diccionarios
            if archivo in mtime_locales.keys():
               paths_locales[archivo] = abspath(archivo)

    return paths_locales, mtime_locales

def todos_archivos_remotos(servicio:tuple)->dict:
    datos_remotos = {}
    mtime_remotos = {}
    files = servicio.files().list(fields='files(name, id, modifiedTime, mimeType, parents)', q="mimeType!='application/vnd.google-apps.folder'").execute().get('files')
    for archivo in files:
        extension = guess_extension(archivo['mimeType']) #Devuelve la extension con el punto o none
        if extension != None:
        #guess_extension puede devolver None, asi que puede que ser pierdan archivos, pero al estar 
        #trabajando con extensiones muy comunes, y al no encontrar una forma garantizada de que me devuelva 
        #la extension correcta, voy a asumir que no se va a perder nada en medio
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
    mimetype_corresp = guess_type(nombre_archivo) #Devuelve (mType, encoding), None en mType si no encuentra
    
    return mimetype_corresp[0]

def subir_archivo(servicio:tuple, datos_remotos:dict, archivo:str, mimetype_corresp:str)->None:
    file_metadata = {'name' : archivo, 'parents' : [datos_remotos[archivo][PARENTS]]}
    media_content = MediaFileUpload(archivo, mimetype='{}'.format(mimetype_corresp) )

    servicio.files().create(body=file_metadata, media_body=media_content).execute()

def borrar_archivo_remoto(servicio:tuple, datos_remotos: dict, archivo:str)->None:
    #Por ahi no tiene sentido hacer esta funcion, pero queda mas claro asi
    servicio.files().delete(fileId='{}'.format(datos_remotos[archivo][ID])).execute()

def bajar_archivo(servicio:tuple, datos_remotos:dict, archivo:str)->None:
    request = servicio.files().get_media(fileId=datos_remotos[archivo][ID])
    fh = BytesIO() 
    #No entiendo que hace esto, en la documentacion de la api no se explica bien, y
    #googleando no termino de entender que es lo que realmente hace
    MediaIoBaseDownload(fd=fh, request=request)

def mover_archivo(archivo:str, paths_locales:dict)->None:
    path_actual = abspath(archivo)
    path_deseado = paths_locales[archivo] #es la ubicacion del archivo borrado
    move(path_actual, path_deseado)

def actualizar_archivos_comunes(mtime_locales:dict, mtime_remotos:dict, datos_remotos:dict, paths_locales:dict, servicio:tuple, path:str)->None:
    #Aclaracion, ante CUALQUIER modifiacion va a cambiar el modified time y el archivo mas nuevo va a ser
    #el que prevalezca sobre el otro
    for archivo in mtime_locales:
        #da igual cual de los dos tome, siempre va a ver todos los que hay en comun
        if archivo in mtime_remotos:
            #PD: el objeto datetime admite que compare de esta forma las fechas
            #Lo que se compara es: Anio-mes-dia hora:minuto:segundo:milisegundo 
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
    #nombres, tambien mtime = modifiedtime
    path = getcwd()
    servicio = obtener_servicio_drive()
    archivos_locales = todos_archivos_locales(path)
    paths_locales = archivos_locales[0]
    mtime_locales = archivos_locales[1]
    archivos_remotos = todos_archivos_remotos(servicio)
    datos_remotos = archivos_remotos[0]
    mtime_remotos = archivos_remotos[1]

    actualizar_archivos_comunes(mtime_locales, mtime_remotos, datos_remotos, paths_locales, servicio, path)