from json.encoder import py_encode_basestring_ascii
from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from select_folder import select_folder
import io

FILE_TYPES = [
    "1- Archivo de texto .txt",
    "2- Archivo excel .xls",
    "3- Foto .jpg",
    "4- Audio .mp3",
    "5- Carpeta vacía"
]

MIME_TYPES_DICT = {
    "txt": "text/plain",
    "xls": "application/vnd.ms-excel",
    "jpg": "image/jpeg",
    "mp3": "audio/mpeg"
}

SERVICE = obtener_servicio()

def crear_archivo_nuevo() -> None: 
    folder_id, flag_root = select_folder(SERVICE)
    if flag_root == True:
        new_file_name = input("Escriba el nombre que quiere darle a su archivo, sin su extension: ")
        for element in FILE_TYPES:
            print (element)
        file_ext_choice = input("Seleccione un número correspondiente al tipo de archivo que desea subir: ")
        if file_ext_choice == "1":
            mime_type = "text/plain"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "2":
            mime_type = "application/vnd.ms-excel"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "3":
            mime_type = "image/jpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "4":
            mime_type = "audio/mpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "5":
            mime_type = 'application/vnd.google-apps.folder'
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            SERVICE.files().create(body=file_metadata).execute()
    else:
        new_file_name = input("Escriba el nombre que quiere darle a su archivo, sin su extension: ")
        for element in FILE_TYPES:
            print (element)
        file_ext_choice = input("Seleccione un número correspondiente al tipo de archivo que desea subir: ")
        if file_ext_choice == "1":
            mime_type = "text/plain"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "2":
            mime_type = "application/vnd.ms-excel"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "3":
            mime_type = "image/jpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "4":
            mime_type = "audio/mpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            SERVICE.files().create(body=file_metadata).execute()
        elif file_ext_choice == "5":
            mime_type = 'application/vnd.google-apps.folder'
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            SERVICE.files().create(body=file_metadata).execute()


    print("¡El archivo fue creado con éxito!")

crear_archivo_nuevo()

def subir_archivos() ->None:
    folder_id = "1jjV0gKN_gM7aSYWCsqdLnIX_wa_qBSxt"

    file_names = ["Prueba.txt", "Esto es otra Prueba.rar"]
    mime_types = ["text/plain","application/vnd.rar"]

    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            "name" : file_name,
            "parents" : [folder_id]
        }

        media = MediaFileUpload("C:\\Users\\Matias\\Desktop\\{0}".format(file_name), mimetype=mime_type)

        service.files().create(
            body = file_metadata,
            media_body = media,
            fields = "id"
        ).execute()

#Meter archivos del local al remoto 


# #Hacer Carpetas Vacías
# group = ['agustin', 'nehuen', 'ingnacio', 'alejandro']

# for participant in group:
#     file_metadata = {
#         'name': participant,
#         'mimeType': 'application/vnd.google-apps.folder'
#         #"parents": []
#     }

# service.files().create(body=file_metadata).execute()