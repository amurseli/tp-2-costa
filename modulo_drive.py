import io
import os
import mimetypes
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

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
    fh = io.BytesIO()
        
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

    mime_type, encoding = mimetypes.guess_type(path, strict=True) # guess_type() utiliza el path que le de y te devuelve su mimetype y su encoding
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
