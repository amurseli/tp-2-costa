import io
import os
import mimetypes
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from select_folder import select_folder

def subir_archivos(service) -> None:
    folder_id, flag_root = select_folder(service)

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
    except TypeError:
        print("\nOcurrió un error al subir el archivo, puede que el mismo tenga la extensión cambiada.")
