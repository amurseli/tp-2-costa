from logging import StreamHandler
from google.oauth2 import service_account        #  Estos se instalaron solos no se que onda
from googleapiclient.discovery_cache import base #  """"""""""""""""""""""""""""""""""""
from googleapiclient.http import HttpRequest
from six import assertCountEqual     #  """"""""""""""""""""""""""""""""""""
from DriveAPI import obtener_servicio_drive
from GmailAPI import obtener_servicio_gmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import base64 
import os.path

SERVICE_GMAIL = obtener_servicio_gmail()
SERVICE_DRIVE = obtener_servicio_drive()

FILES = ['\alumnos.csv','\docentes.csv','\alumnos-docentes.csv']
#mensaje email

def enviar_mensaje(service: None , user:str, mensaje:str):
    try:
        msg  = service.users().messages().send(userId = user, body = mensaje).execute()
        print(f"El contenido del mensaje es: {mensaje}")
        return msg

    except Exception as e:
        print(f"Ocurrio un error del tipo {e}")
        return None



def crear_mensaje(sender:str, to :str, asunto:str, mensaje_texto:str, files:None):
    
    mensaje = MIMEMultipart()
    mensaje['to'] = to
    mensaje['from'] = sender
    mensaje['asunto'] = asunto

    msg_text = MIMEText(mensaje_texto)
    mensaje.attach(msg_text)

    for adjuntos in files:
        with open(adjuntos, 'rb') as a:
            content_type, encodig = mimetypes.guess_type(adjuntos)  #creo que al pedo no lo uso y el archivo 
            main_tipe, sub_type   = content_type.split("/",1)       # va a ser texto osea .CSV
            msg = MIMEText(a.read().decode('utf-8'))

        file_name = os.path.basename(adjuntos)
        msg.add_header('Content-Disposition', 'attachment',filename = file_name)
        mensaje.attach(msg)
        raw_string = base64.urlsafe_b64encode(mensaje.as_bytes()).decode("utf-8")
    return {'raw': raw_string.decode('utf-8')}

def main():
    service = SERVICE_GMAIL
    user = "Ignacio"
    sender = "itotino@fi..."
    to = "ignaciotomas@...."
    asunto = "TEST"
    mensaje_texto = "Esto es una prueba"
    files = FILES

    mensaje = crear_mensaje(sender, to, asunto, mensaje_texto, files)
    enviar_mensaje(service,user,mensaje)
