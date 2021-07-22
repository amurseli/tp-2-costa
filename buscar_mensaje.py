
import io 
import base64
from googleapiclient.http import MediaIoBaseUpload


def buscar_mail(service, query_str:str,labels_id = []):
    '''
    :param service: = servicio de Gmail
    :param query_str: = el nombre del asunto con el que se quiere obtener el mail
    :param label_id: = INBOX en general
    '''
    try:
        lista_de_messajes = service.users().messages().list(userId = 'me', labelIds = labels_id, q = query_str
        ).execute()

        mensajes_items = lista_de_messajes.get('messages')
        next_page_token = lista_de_messajes.get('nextPageToken')

        while next_page_token:
            lista_de_messajes = service.users().messages().list(
                userId = 'me', labelIds = labels_id, q = query_str, pageToken = next_page_token).execute()

        mensajes_items.extend(lista_de_messajes.get('messages'))
        next_page_token = mensajes_items.get('nextPageToken')
        
        return mensajes_items
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")

def obtener_detalles_mensajes(service, id_mensaje, format = 'metadata', headers_metadata = []):
    '''
    :param service: = servicio de Gmail
    :param user_id: =  Email del usuario. y el paramerto userID = 'me'

    '''

    try:
        detalles = service.users().messages().get(userId = 'me',id= id_mensaje, format = format, metadaHeaders = headers_metadata
        ).execute()
        return detalles
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}.\n")
        return None


'''
Buscar Mensajes
query_str = 'Subject: (nombre)'
buscarmail(gmail_service,query_str, ['INBOX'])

'''