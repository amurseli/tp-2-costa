from service_gmail import obtener_servicio_gmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os
import base64
import csv
import zipfile

SERVICE_GMAIL = obtener_servicio_gmail()

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
                    sub = x['value'] #asunto
                    print(sub)
            print(leer['snippet'])  #body

            # para el mail con adjuntos-------
            directorio = " "
            descargar(payload,mensaje,directorio)

        return sub


def descargar(payload,mensaje,directorio):
    # --------------Descargar archivos------------------
    if 'parts' in payload:
        for i in payload['parts']:
            msg = i['body']

            if 'attachmentId' in msg:
                att_id = msg['attachmentId']
                respuesta = SERVICE_GMAIL.users().messages().attachments().get(
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
    asunto = "Informacion"
    mensaje = "A continuacion se creara carpetas en tu drive con los archivos .csv, a continuación presiona enter"
    q_str = "subject:Informacion"
    try:
        enviar_mensaje_API(SERVICE_GMAIL,destinatario,asunto,mensaje)
        leer_mensajes_API(SERVICE_GMAIL, q_str, destinatario)
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")

def enviar_mensaje_con_adjunto(SERVICE_GMAIL)->str:
    print("Mail al que se le quiere enviar, ej:example@algo.com")
    destinatario = input()
    asunto = "Evaluacion"
    mensaje = "Se te enviaron archivos para que lo subas a tu carpeta drive"
    attachment = ['alumnos_docentes.zip']
    q_str = "subject:Evaluacion"
    try:
        enviar_mensaje_con_adjuntos_API(SERVICE_GMAIL, destinatario, asunto, mensaje, attachment)
        sub = leer_mensajes_API(SERVICE_GMAIL, q_str,destinatario)
        return sub
    except Exception as e:
        print(f"Ocurrio un error del tipo {e}\n por no seguir los pasos dictados.")
        return None
    
 
#--------------DE ACA PARA ABAJO PARTE DE ALEJANDRO-------------------
 
    
def descomprimir_zip():
    zip = "\\alumnos_docentes.zip"
    extraccion = "\\zip_descomprimido"
    ruta_zip = os.getcwd() + zip
    ruta_extraccion = os.getcwd() + extraccion
    password = None
    archivo_zip = zipfile.ZipFile(ruta_zip, "r")

    try:
        archivo_zip.extractall(pwd = password, path = ruta_extraccion)

    except:
        pass

    archivo_zip.close()
    
    return ruta_extraccion


def docente_alumnos_CSV(path_docente_alumnos: str) -> list:
    docentes = list()
    alumnos = list()
    with open(path_docente_alumnos, newline='') as file:
        header = csv.Sniffer()
        reader = csv.reader(file)
        if header:
            next(reader)
        reader = list(reader)
        for fila in reader:
            nombre_docente = fila[0]
            nombre_alumnos = fila[1]
            docentes.append(nombre_docente)
            alumnos.append(nombre_alumnos)
    
    return set(docentes), alumnos


def docente_csv(path_docentes: str):
    docentes = list()
    with open(path_docentes, newline='') as file:
        header = csv.Sniffer()
        reader = csv.reader(file)
        if header:
            next(reader)
        reader = list(reader)
        for fila in reader:
            nombre_docente = fila[0]
            docentes.append(nombre_docente)
    
    return docentes


def dict_alumnos(path_docente_alumnos: str):
    datos = {}
    with open (path_docente_alumnos, newline='', encoding="UTF-8") as archivo:
        csv_reader = csv.reader(archivo, delimiter=',')
        next(csv_reader)
        for fila in csv_reader:
            if not fila[0] in datos:
                datos[fila[0]] = []
                datos[fila[0]].append(fila[1])

            else:
                datos[fila[0]].append(fila[1])
    
    return datos
    

def sistema_carpeta(asunto: str, path_docentes: str, path_docente_alumnos: str):
    docentes = docente_csv(path_docentes)
    datos = dict_alumnos(path_docente_alumnos)
    evaluacion = os.mkdir(asunto)
    for docente in docentes:
        carpeta_docente = os.mkdir(f"{asunto}/{docente}")
        for alumno in datos[docente]:
            alumnos = os.mkdir(f"{asunto}/{docente}/{alumno}")
            with open(f"{asunto}/{docente}/{alumno}/Archivo.txt", "w") as files:
                elemento = files


def carpetas_anidadas(subject: str):
    path_zip = descomprimir_zip()
    path_docentes = (f"{path_zip}/docentes.csv")
    path_docente_alumnos = (f"{path_zip}/docente_alumnos.csv")
    docentes = docente_csv(path_docentes)
    sistema_carpeta(subject, path_docentes, path_docente_alumnos)