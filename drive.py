from json.encoder import py_encode_basestring_ascii
from service_drive import obtener_servicio
from googleapiclient.http import MediaFileUpload
#CLIENT_SECRET_FILE = "client_secret_drive.json"

service = obtener_servicio()

folder_id = "1jjV0gKN_gM7aSYWCsqdLnIX_wa_qBSxt"

file_names = ["Prueba.txt", "Esto es otra Prueba.rar"]
mime_types = ["text/plain","application/vnd.rar"]

# for file_name, mime_type in zip(file_names, mime_types):
#     file_metadata = {
#         "name" : file_name,
#         "parents" : [folder_id]

#     }

#     media = MediaFileUpload("C:\\Users\\Matias\\Desktop\\{0}".format(file_name), mimetype=mime_type)

#     service.files().create(
#         body = file_metadata,
#         media_body = media,
#         fields = "id"
#     ).execute()

#Hacer Carpetas Vacías
group = ['agustin', 'nehuen', 'ingnacio', 'alejandro']

for participant in group:
    file_metadata = {
        'name': participant,
        'mimeType': 'application/vnd.google-apps.folder'
        #"parents": []
    }

service.files().create(body=file_metadata).execute()