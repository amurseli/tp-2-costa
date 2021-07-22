from GmailAPI import obtener_servicio_gmail
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def buscar_mensaje(query):
    service = obtener_servicio_gmail()

    resultado = service.users().messages().list(userId='me',q=query).execute()
    mensajes = [ ]
    if 'messages' in resultado:
        mensajes.extend(resultado['messages']) #añado el elemento al final de la lista
    while 'nextPageToken' in resultado:
        page_token = resultado['nextPageToken']
        resultado = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in resultado:
            mensajes.extend(resultado['messages'])
    return mensajes

#FALTA TERMINAR

#query = 'test'
#buscar_mensaje(query)