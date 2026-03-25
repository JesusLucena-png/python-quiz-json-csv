import json
import random
import csv

# Categorías de preguntas
preguntas_peliculas = []
preguntas_series = []
preguntas_anime = []
preguntas_videojuegos = []
preguntas_musica = []
preguntas_programacion_basica = []

# Listas para resultados y ranking
resultados = []
ranking = []

# Leer archivo JSON con las preguntas
with open("data.json", "r", encoding="utf-8") as archivo:
    datos = json.loads(archivo.read())

    # Recorrer cada pregunta
    for pregunta in datos:
        for clave, valor in pregunta.items():

            # Clasificar preguntas por categoría
            if clave == "categoria" and valor == "Películas":
                preguntas_peliculas.append(pregunta)

            elif clave == "categoria" and valor == "Series":
                preguntas_series.append(pregunta)

            elif clave == "categoria" and valor == "Anime":
                preguntas_anime.append(pregunta)

            elif clave == "categoria" and valor == "Videojuegos":
                preguntas_videojuegos.append(pregunta)

            elif clave == "categoria" and valor == "Música":
                preguntas_musica.append(pregunta)

            elif clave == "categoria" and valor == "Programación Básica":
                preguntas_programacion_basica.append(pregunta)
    

# Función para confirmar salida del juego
def confirmar_salida(mensaje="Presione (n) para salir o cualquier tecla para continuar: "):
    
    opcion_usuario = input(f"\n\033[31m >> \033[0m{mensaje}").strip().lower()
        
    if opcion_usuario == "n":
        return True     


# Función para mostrar una pregunta
def mostrar_pregunta(lista_preguntas, numero_pregunta, indice_usuario):
    
    # Seleccionar pregunta aleatoria
    indice_aleatorio = random.randint(0, len(lista_preguntas) - 1)
    datos_pregunta = lista_preguntas[indice_aleatorio]

    # Mostrar enunciado
    print(f"\n{numero_pregunta}. {datos_pregunta.get('pregunta')}\n")

    # Obtener opciones
    opciones = datos_pregunta.get("opciones")

    # Mostrar opciones
    for opcion, valor in opciones.items():
        print(f"{opcion}. {valor}")

    opcion_valida = True
    while opcion_valida:
        
        # Pedir respuesta al usuario
        opcion_usuario = input("\n\033[34m >> \033[0mIngrese una opción: ").upper()

        # Validar nombre (aunque aquí no es necesario)
        if not nombre.strip():
            print("\n\033[1;31m" + "-"*60 + f"\nError: Por favor ingrese un nombre." + "\n" + "-"*60 + "\033[0m")
            continue

        # Validar opción
        if opcion_usuario in ["A", "B", "C", "D"]:
            if opcion_usuario == datos_pregunta.get("respuesta_correcta"):
                print("\n\033[1;32m+ 20 puntos\033[0m")

                # Guardar respuesta correcta
                resultados[indice_usuario].append({
                    "pregunta": datos_pregunta.get("pregunta"),
                    "opcion": opcion_usuario,
                    "puntos": 20,
                })
                return 20
            else:
                print("\n\033[1;31m+ 0 puntos\033[0m")

                # Guardar respuesta incorrecta
                resultados[indice_usuario].append({
                    "pregunta": datos_pregunta.get("pregunta"),
                    "opcion": opcion_usuario,
                    "puntos": 0,
                })
                return 0
        else:
            # Error si la opción no es válida
            print("\n\033[1;31m" + "-"*60 + f"\nError: Por favor ingrese una opción válida." + "\n" + "-"*60 + "\033[0m")
            continue


# Control del juego
juego_activo = True
while juego_activo:

    validar_nombre = True
    while validar_nombre:

        print("\033[34m" + "-"*60 + "\033[0m")

        # Pedir nombre del usuario
        nombre = input("\n\033[34m >> \033[0mIngrese nombre del usuario: ")

        print("\033[34m" + "-"*60 + "\033[0m")

        # Validar nombre
        if not nombre.strip():
            print("\n\033[1;31m" + "-"*60 + f"\nError: Por favor ingrese un nombre." + "\n" + "-"*60 + "\033[0m")
            continue
        else:
            # Guardar usuario
            indice_usuario = len(resultados)
            resultados.append([nombre, True])
            validar_nombre = False

    puntaje_total = 0
    numero_pregunta = 1
    categorias_aleatorias = random.sample(range(0, 6), 5)

    while numero_pregunta != 5:

        # Lista de categorías
        listas_preguntas = [
            preguntas_peliculas,
            preguntas_series,
            preguntas_anime,
            preguntas_musica,
            preguntas_videojuegos,
            preguntas_programacion_basica
        ]

        # Recorrer categorías aleatorias
        for num in categorias_aleatorias:
            puntos = mostrar_pregunta(listas_preguntas[num], numero_pregunta, indice_usuario)
            puntaje_total += puntos
            numero_pregunta += 1
            print("\033[34m" + "-"*60 + "\033[0m")
        
        break

    # Guardar puntaje total
    resultados[indice_usuario].append(puntaje_total)

    print("\033[34m" + "-"*60 + "\033[0m")

    # Mostrar resultados
    print(f"Nombre: {resultados[indice_usuario][0]}")
    print(f"Fecha: {resultados[indice_usuario][1]}")

    for i, datos_pregunta in enumerate(resultados[indice_usuario][2:7]):
        print(f"\n{i+1}. {datos_pregunta['pregunta']}")
        print(f"Opción seleccionada: {datos_pregunta['opcion']}  |  Puntos: {datos_pregunta['puntos']}\n")
    
    print(f"Puntos totales: {resultados[indice_usuario][7]}")

    # Agregar al ranking
    ranking.append([resultados[indice_usuario][0], resultados[indice_usuario][7]])

    print("\033[34m" + "-"*60 + "\033[0m")

    # Confirmar salida
    salir = confirmar_salida()
    if salir:
        juego_activo = False
    else:
        continue


# Guardar ranking en CSV
with open("ranking.csv", mode='a', newline='', encoding='utf-8') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerows(ranking)


# Cargar ranking desde CSV
ranking = []
try:
    with open("ranking.csv", mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            if fila:
                ranking.append([fila[0], int(fila[1])])
except FileNotFoundError:
    print("El archivo ranking.csv aún no existe.")


# Ordenar ranking por puntaje
ranking.sort(key=lambda x: x[1], reverse=True)
posicion = 0

# Mostrar ranking
print("\n\033[34m" + "-"*60 + "\033[0m")
print("RANKING")
print("\033[34m" + "-"*60 + "\033[0m")
print(f"{'PUESTO':<8} {'NOMBRE':<10} - {'PUNTOS':<10}")
print("\033[34m" + "-"*60 + "\033[0m")

# Mostrar top 10
for fila in ranking:
    posicion += 1
    print(f"{posicion:<8} {fila[0]:<10} - {fila[1]:<10}")

    if posicion == 10:
        break