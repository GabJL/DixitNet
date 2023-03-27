import csv
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from jinja2 import Template

def read_student_data(filename):
    # Abrir el archivo CSV y leerlo
    with open(filename, encoding="utf8", newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Crear una lista vacía para almacenar los datos
        participantes = []

        # Iterar sobre cada fila del arTTchivo CSV
        for row in reader:
            # Crear un diccionario para almacenar los datos de cada participante
            datos_participante = {}

            # Asignar los valores de cada columna a las claves correspondientes
            datos_participante['ID'] = row['ID de participante único en todo CV']
            datos_participante['DNI'] = row['DNI/NIE/Pasaporte']
            datos_participante['ID_centro'] = row['ID de participante en este centro']
            datos_participante['Nombre'] = row['Nombre']
            datos_participante['Apellido'] = row['Apellido/s']
            datos_participante['Inscripcion'] = row['Inscripción']
            datos_participante['Grupos'] = row['Grupos']
            datos_participante['Correo'] = row['Correo electrónico']
            datos_participante['Ultima_descarga'] = row['Última descarga de esta asignatura']

            # Agregar los datos del participante al diccionario de participantes
            participantes.append(datos_participante)

    return participantes

def get_student_names(d):
    return [s['Apellido']+", "+s["Nombre"] for s in d]

def get_last_number(ID):
    for c in ID[::-1]:
        if c.isdigit():
            return int(c)

def get_group(d, name):
    for student in d:
        if student["Apellido"] + ", " + student["Nombre"] == name:
            return get_last_number(student["DNI"])%2
        
def initialize_points(d, al):
    datos = {
        "grupo0_puntuacion_total": 0,
        "grupo0_miembros": [],
        "grupo0_puntuaciones": {s:0 for s in al if get_group(d, s) == 0},
        "grupo1_puntuacion_total": 0,
        "grupo1_miembros": [],
        "grupo1_puntuaciones": {s:0 for s in al if get_group(d, s) == 1}
    }
    return datos

def assign_points(turno, num_resp, participantes, representantes, alumno, data):
    if num_resp == 2:
        points = 4
        r_points = 2
    elif num_resp == 4:
        points = 3
        r_points = 2
    elif num_resp == 6:
        points = 2
        r_points = 1
    else:
        points = 1
        r_points = 1
    
    if get_group(participantes, alumno) == 0:
        data["grupo0_puntuacion_total"] += points
        if alumno not in data["grupo0_miembros"]:
            data["grupo0_miembros"].append(alumno)
        data["grupo0_puntuaciones"][alumno] += points
    else:
        data["grupo1_puntuacion_total"] += points
        if alumno not in data["grupo1_miembros"]:
            data["grupo1_miembros"].append(alumno)
        data["grupo1_puntuaciones"][alumno] += points
    
    for p in representantes:
        if get_group(participantes, p) == turno:
            if turno == 0:
                if p not in data["grupo0_miembros"]:
                    data["grupo0_miembros"].append(p)
                data["grupo0_puntuaciones"][p] += r_points
            else:
                if p not in data["grupo1_miembros"]:
                    data["grupo1_miembros"].append(p)
                data["grupo1_puntuaciones"][p] += r_points
    
# Leer datos
participantes = read_student_data("alumnos.csv")
alumnos = get_student_names(participantes)

# Configurar la función de autocompletado
AlumnoCompleter = WordCompleter(alumnos, ignore_case=True)

# Inicializar puntos
datos = initialize_points(participantes, alumnos)
#print(datos)

# Leer representantes:
representantes = []
print("Representantes: ")
entrada = prompt("Alumno> ", completer=AlumnoCompleter)
while entrada:
    representantes.append(entrada)
    entrada = prompt("Alumno> ", completer=AlumnoCompleter)

# Leer plantilla
with open('plantilla.html', 'r') as f:
    contenido = f.read()
template = Template(contenido)
    


# Renderizamos la plantilla con los datos
resultado = template.render(datos)
with open("puntuacion.html", "w") as f:
    f.write(resultado)
# Leer turno
turno = int(input("¿Qué grupo empieza? "))
while True:
    num_resp = int(input("Número de pistas del acierto (0 no acierto): "))
    if num_resp:
        alumno = prompt("Alumno> ", completer=AlumnoCompleter)
        assign_points(turno, num_resp, participantes, representantes, alumno, datos)
    turno = 1 - turno
    # Abrimos un archivo en modo escritura y escribimos el resultado
    # Renderizamos la plantilla con los datos
    resultado = template.render(datos)
    with open("puntuacion.html", "w") as f:
        f.write(resultado)