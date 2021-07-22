import io
import os
from seleccionar_carpeta import seleccionar_carpeta
from descargar_archivo import descargar_archivos

FILE_TYPES = [
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

def crear_archivo_nuevo(service) -> None: 
    folder_id, flag_root = seleccionar_carpeta(service)
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
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "2":
            mime_type = "image/jpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "3":
            mime_type = "audio/mpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "4":
            mime_type = 'application/vnd.google-apps.folder'
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "5":
            mime_type = "application/json"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "6":
            mime_type = "application/msword"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "7":
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "8":
            mime_type = "application/vnd.ms-excel"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "9":
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
            }
            service.files().create(body=file_metadata).execute()

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
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "2":
            mime_type = "image/jpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "3":
            mime_type = "audio/mpeg"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "4":
            mime_type = 'application/vnd.google-apps.folder'
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "5":
            mime_type = "application/json"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "6":
            mime_type = "application/msword"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "7":
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "8":
            mime_type = "application/vnd.ms-excel"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
        elif file_ext_choice == "9":
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            file_metadata = {
                'name': new_file_name,
                'mimeType': mime_type,
                "parents": [folder_id]
            }
            service.files().create(body=file_metadata).execute()
    print("¡El archivo fue creado con éxito!")
