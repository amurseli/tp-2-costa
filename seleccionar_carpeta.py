
def seleccionar_carpeta(service) -> tuple:
    folder_id = " "
    flag_root = True
    files = service.files().list(fields='files(name, id, mimeType)',q="mimeType='application/vnd.google-apps.folder'").execute().get('files')
    i = 0
    for element in files:
        for key,value in element.items():
            if key == "name":
                print (f"-{value}")
    print("Recuerde que si desea el direcotrio raíz, no complete el siguiente campo")
    name = input("Porfavor copie y pegue el nombre de la carpeta que desea.")

    for element in files:
        for key,value in element.items():
            if element[key] == name:
                target_file = element
                folder_id = target_file["id"] 
                flag_root = False

    
    
    return (folder_id, flag_root)
    