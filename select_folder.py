
def select_folder(service) -> str:
    files = service.files().list(fields='files(name, id, mimeType)',q="mimeType='application/vnd.google-apps.folder'").execute().get('files')
    i = 0
    for element in files:
        for key,value in element.items():
            if key == "name":
                print (f"-{value}")
    print("Recuerde que si desea poner el archivo en el direcotrio raíz, no complete el siguiente campo")
    name = input("Porfavor copie y pegue el nombre de la carpeta en la que desea poner el archivo.")

    for element in files:
        for key,value in element.items():
            if element[key] == name:
                target_file = element

    folder_id = target_file["id"]
    return folder_id
    