from GmailAPI import obtener_servicio_gmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os
import base64

SERVICE_GMAIL = obtener_servicio_gmail()
service = obtener_servicio_gmail()
#-------------------------MODULO GMAIL------------------------------------------#

def enviar_mensaje_API(service, destinatario:str, asunto:str, mensaje:str)->None:
    '''
    :param service: = funcion del servicio de google API  
    :param destinatario: = al address donde va a enviar el mail
    :param asunto: = va a ser el asunto xd
    :param mensaje: = el body del mensaje
    '''

    email_msg = mensaje    
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = destinatario    
    mimeMessage['subject'] = asunto   
    mimeMessage.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    try:
        enviar = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")

def enviar_mensaje_con_adjuntos_API(service, destinatario:str,asunto:str,mensaje:str,attachment:list)->None:
    '''
     :param service: = funcion del servicio de google API  Gmail
     :param destinatario: = al address donde va a enviar el mail,
     :param asunto: = va a ser el asunto xd,
     :param mensaje: = el body del mensaje,
     :param attachment: = va a ser una lista con los archivos .csv   
                                                             
    '''

    archivos_adjuntos = attachment
    email_msg = mensaje
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = destinatario
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
    enviar = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    
def leer_mensajes_API(service,q_str:str,destinatario:str)-> str:
    '''
    :param service: = funcion del servicio de google API  
    :param q_str: = el dato para poder filtrar los mails
    :param destinatario: = al address donde va a enviar el mail
    '''

    resultado = service.users().messages().list(userId= destinatario,q= q_str,labelIds= ['INBOX']).execute()
    mensajes = resultado.get('messages', [])
    
    if not mensajes:
        print ("No encontraron mensajes.")
    else:
        print("")
        print ("Mensaje:")
        for mensaje in mensajes[:1]:
            leer = service.users().messages().get(userId='me', id=mensaje['id']).execute()
            payload = leer.get("payload")
            header = payload.get("headers")
            for x in header:
                if x['name'] == 'subject':
                    sub = print(x['value']) #asunto
            print(leer['snippet'])  #body

            # para el mail con adjuntos-------
            directorio = "tp-2-costa"
            descargar(payload,mensaje,directorio)

        return sub


def descargar(payload,mensaje,directorio):
    # --------------Descargar archivos------------------
            if 'parts' in payload:
                for i in payload['parts']:
                    msg = i['body']

                    if 'attachmentId' in msg:
                        att_id = msg['attachmentId']
                        respuesta = service.users().messages().attachments().get(
                            userId= 'me',
                            messageId = mensaje['id'],
                            id = att_id
                        ).execute()

                        data = base64.urlsafe_b64decode(respuesta.get('data').encode('utf-8'))
                        path = ''.join([directorio, i['filename']])
                        with open(path, 'wb')  as p:
                            p.write(data)


def enviar_mensajes(SERVICE_GMAIL):
    print("Mail al que se le quiere enviar, ej:example@algo.com")
    destinatario = input()
    asunto = "DATOS"
    mensaje = "A continuacion se creara en local evaluacion/docentes/alumnos y tambien una carpeta remota en drive y elija la opcion 4 para crear en remoto"
    q_str = "subject:DATOS"
    try:
        enviar_mensaje_API(SERVICE_GMAIL,destinatario,asunto,mensaje)
        leer_mensajes_API(SERVICE_GMAIL, q_str, destinatario)
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")

def enviar_mensaje_con_adjunto(SERVICE_GMAIL)->str:
    print("Mail al que se le quiere enviar, ej:example@algo.com")
    destinatario = input()
    asunto = "TENES ARCHIVOS"
    mensaje = "Se te enviaron archivos para que lo subas a tu carpeta drive"
    attachment = ['alumnos_docentes.zip']
    q_str = "subject:TENES ARCHIVOS"
    try:
        enviar_mensaje_con_adjuntos_API(SERVICE_GMAIL, destinatario, asunto, mensaje, attachment)
        sub = leer_mensajes_API(SERVICE_GMAIL, q_str,destinatario)
        return sub
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")
        return None

