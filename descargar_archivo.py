import io
from tkinter import Tk
from tkinter.filedialog import askdirectory
from googleapiclient.http import MediaIoBaseDownload
from select_folder import select_folder

def descargar_archivos(service) -> None:
    folder_id, flag_root = select_folder(service)
    if flag_root == False:
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

    file_name = input("Porfavor copie y pegue el nombre del archivo a descargar.")

    for element in files:
        for key,value in element.items():
            if element[key] == file_name:
               target_file = element
               file_id = target_file["id"] 

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
        
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False

    print("Seleccione una Carpeta en la ventan que se acaba de abrir. Es posible que no se haya abierto en primer plano.")
    path = askdirectory(title='Seleccione una carpeta') 

    try:
        # Download the data in chunks
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        with open(f"{path}\\{file_name}", 'wb') as f:
            f.write(fh.read())

        print("Archivo Descargado con éxito!")
    except :
    
        print("Algo salió Mal.")
        print("Es probable que estes intentando descargar un archivo no descargable.")
        print("Algunos de los archivos no descargables son los que fueron editados por las aplicaciones de drive como 'Google Docs' o 'Goggle Sheets'")
        return False
    
