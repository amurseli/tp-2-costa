import io
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from select_folder import select_folder

def subir_archivos(service) -> None:
    folder_id, flag_root = select_folder(service)

    mime_type = "image/jpeg"

    print("Seleccione un archivo en la ventan que se acaba de abrir. Es posible que no se haya abierto en primer plano.")
    path = askopenfilename(title='Seleccione un archivo')
    path_split = path.split("/")
    file_name = path_split[-1]

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

    service.files().create(
        body = file_metadata,
        media_body = media,
        fields = "id"
    ).execute()

    print("El archivo se subió Exitosamente")
