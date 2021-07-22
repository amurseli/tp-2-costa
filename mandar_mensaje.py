import email
from GmailAPI import obtener_servicio_gmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os
import base64


def enviar_mensaje(destinatario:str, asunto:str, mensaje:str)->None:
    '''
    Explicaion de lo que deben contener las variables:
     destinatario = el mail al que se le quiere mandar un mensaje
     asunto = va a ser el asunto xd
     mensaje = el body del mensaje
    '''
    service = obtener_servicio_gmail()

    email_msg = mensaje    
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = destinatario    
    #mimeMessage['from'] = el mail desde que queremos mandar, pero toma como predeterminado el que le dimos allow
    mimeMessage['subject'] = asunto   
    mimeMessage.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    try:
        enviar = service.users().messages().send(userId='Yo', body={'raw': raw_string}).execute()
        print(enviar)
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")

def enviar_mensaje_con_adjuntos(destinatario:str,asunto:str,mensaje:str,attachment:list)->None:
    '''
    Explicaion de lo que deben contener las variables:
     destinatario = el mail al que se le quiere mandar un mensaje,
     asunto = va a ser el asunto xd,
     mensaje = el body del mensaje,
     attachment = va a ser una lista con los archivos .csv  # no se que onda pero no los manda, no se si sera que esten vacios pero otras coasas si manda
                                                            # en la casilla de mensajes enviados si aparecen
    '''

    service = obtener_servicio_gmail()
    archivos_adjuntos = attachment
    email_msg = mensaje
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = destinatario
    #mimeMessage['from'] = el mail desde que queremos mandar, pero toma como predeterminado el que le dimos allow
    mimeMessage['subject'] = asunto
    mimeMessage.attach(MIMEText(email_msg, 'plain'))

    for archivos in archivos_adjuntos:
        
        content_type, encoding = mimetypes.guess_type(archivos)
        main_type, sub_type = content_type.split('/', 1)
        nombre_archivo = os.path.basename(archivos)

        try:
            with open(archivos,'rb') as archivo:

                mi_archivo = MIMEBase(main_type, sub_type)
                mi_archivo.set_payload(archivo.read())
                mi_archivo.add_header('Content-Disposition','archivos', filename = nombre_archivo)
                encoders.encode_base64(mi_archivo)
                mimeMessage.attach(mi_archivo)

        except Exception as e:
            print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    enviar = service.users().messages().send(userId='Yo', body={'raw': raw_string}).execute()
    print(enviar)


destinatario = 'itot...@...'
asunto = 'PRUEBA'
mensaje= 'HOLA'
enviar_mensaje(destinatario,asunto, mensaje)