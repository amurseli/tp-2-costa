import io
from tkinter import Tk
from tkinter.filedialog import askdirectory
from googleapiclient.http import MediaIoBaseDownload
from seleccionar_carpeta import seleccionar_carpeta

def descargar_archivos(service) -> None:
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
