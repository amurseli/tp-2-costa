import os
import csv
import zipfile

def descomprimir_zip():
    zip = "\\alumnos_docentes.zip"
    extraccion = "\\zip_descomprimido"
    ruta_zip = os.getcwd() + zip
    ruta_extraccion = os.getcwd() + extraccion
    password = None
    archivo_zip = zipfile.ZipFile(ruta_zip, "r")

    try:
        #print(archivo_zip.namelist())
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


def main():
    path_zip = descomprimir_zip()
    asunto = input("Ingrese un nombre de carpeta: ")
    path_docentes = (f"{path_zip}/docentes.csv")
    path_docente_alumnos = (f"{path_zip}/docente_alumnos.csv")
    docentes = docente_csv(path_docentes)
    sistema_carpeta(asunto, path_docentes, path_docente_alumnos)
    
main()