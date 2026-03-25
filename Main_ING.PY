import json
import random
import csv

# Lists to store questions by category
preguntas_peliculas = []
preguntas_series = []
preguntas_anime = []
preguntas_videojuegos = []
preguntas_musica = []
preguntas_programacion = []

# List to store each player's results
resultados = []

# List to store the overall ranking
ranking = []

# Open and read the JSON file with the questions
with open("data.json", "r", encoding="utf-8") as archivo_json:
    datos = json.loads(archivo_json.read())

    # Iterate through each question in the JSON
    for pregunta in datos:
        for clave, valor in pregunta.items():

            # Classify questions based on their category
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
                preguntas_programacion.append(pregunta)


# Function to confirm if the user wants to exit the game
def confirmar_salida(mensaje="Press (n) to exit or any key to continue: "):
    
    opcion_usuario = input(f"\n\033[31m >> \033[0m{mensaje}").strip().lower()
        
    if opcion_usuario == "n":
        return True     


# Function to display a random question from a list
def mostrar_pregunta(lista_preguntas, numero_pregunta, indice_usuario):
    
    # Select a random question
    indice_aleatorio = random.randint(0, len(lista_preguntas) - 1)
    pregunta_actual = lista_preguntas[indice_aleatorio]

    # Display the question text
    print(f"\n{numero_pregunta}. {pregunta_actual.get('pregunta')}\n")

    # Get answer options
    opciones = pregunta_actual.get("opciones")

    # Display each option
    for opcion, valor in opciones.items():
        print(f"{opcion}. {valor}")

    opcion_valida = True
    while opcion_valida:
        
        # Ask for user's answer
        opcion_usuario = input("\n\033[34m >> \033[0mEnter an option: ").upper()

        # Validate that the name is not empty (not really needed here)
        if not nombre.strip():
            print("\n\033[1;31m" + "-"*60 + f"\nError: Please enter a name." + "\n" + "-"*60 + "\033[0m")
            continue

        # Check if the option is valid
        if opcion_usuario in ["A", "B", "C", "D"]:
            
            # Check if the answer is correct
            if opcion_usuario == pregunta_actual.get("respuesta_correcta"):
                print("\n\033[1;32m+ 20 points\033[0m")

                # Save correct answer result
                resultados[indice_usuario].append({
                    "pregunta": pregunta_actual.get("pregunta"),
                    "opcion": opcion_usuario,
                    "puntos": 20,
                })
                return 20
            else:
                print("\n\033[1;31m+ 0 points\033[0m")

                # Save incorrect answer result
                resultados[indice_usuario].append({
                    "pregunta": pregunta_actual.get("pregunta"),
                    "opcion": opcion_usuario,
                    "puntos": 0,
                })
                return 0
        else:
            # Error message for invalid option
            print("\n\033[1;31m" + "-"*60 + f"\nError: Please enter a valid option." + "\n" + "-"*60 + "\033[0m")
            continue
    
    opcion_valida = False


# Game control variable
juego_activo = True

# Main game loop
while juego_activo:

    validar_nombre = True
    while validar_nombre:

        # Display visual separator
        print("\033[34m" + "-"*60 + "\033[0m")

        # Ask for user's name
        nombre = input("\n\033[34m >> \033[0mEnter user name: ")

        print("\033[34m" + "-"*60 + "\033[0m")

        # Validate name is not empty
        if not nombre.strip():
            print("\n\033[1;31m" + "-"*60 + f"\nError: Please enter a name." + "\n" + "-"*60 + "\033[0m")
            continue
        else:
            # Store user in results
            indice_usuario = len(resultados)
            resultados.append([nombre, True])
            validar_nombre = False
    
    puntaje_total = 0
    numero_pregunta = 1
    categorias_aleatorias = random.sample(range(0, 6), 5)

    while numero_pregunta != 5:

        # List of all question categories
        listas_preguntas = [
            preguntas_peliculas,
            preguntas_series,
            preguntas_anime,
            preguntas_musica,
            preguntas_videojuegos,
            preguntas_programacion
        ]

        # Iterate through random categories
        for num in categorias_aleatorias:
            puntos = mostrar_pregunta(listas_preguntas[num], numero_pregunta, indice_usuario)
            puntaje_total += puntos
            numero_pregunta += 1
            print("\033[34m" + "-"*60 + "\033[0m")
        
        break

    # Save total score
    resultados[indice_usuario].append(puntaje_total)

    print("\033[34m" + "-"*60 + "\033[0m")

    # Display user results
    print(f"Name: {resultados[indice_usuario][0]}")
    print(f"Date: {resultados[indice_usuario][1]}")

    # Show each answered question
    for i, pregunta_guardada in enumerate(resultados[indice_usuario][2:7]):
        print(f"\n{i+1}. {pregunta_guardada['pregunta']}")
        print(f"Selected option: {pregunta_guardada['opcion']}  |  Points earned: {pregunta_guardada['puntos']}\n")
    
    print(f"Total points: {resultados[indice_usuario][7]}")

    # Add to ranking
    ranking.append([resultados[indice_usuario][0], resultados[indice_usuario][7]])

    print("\033[34m" + "-"*60 + "\033[0m")

    # Ask if user wants to exit
    salir = confirmar_salida()
    if salir == True:
        juego_activo = False
    else:
        continue


# Save ranking to CSV file
with open("ranking.csv", mode='a', newline='', encoding='utf-8') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerows(ranking)


# Reload ranking from file
ranking = []
try:
    with open("ranking.csv", mode='r', encoding='utf-8') as archivo_csv:
        lector = csv.reader(archivo_csv)
        for fila in lector:
            if fila:
                ranking.append([fila[0], int(fila[1])])
except FileNotFoundError:
    print("The ranking.csv file does not exist yet.")


# Sort ranking by score (descending)
ranking.sort(key=lambda x: x[1], reverse=True)
posicion = 0

# Display ranking table
print("\n\033[34m" + "-"*60 + "\033[0m")
print("RANKING")
print("\033[34m" + "-"*60 + "\033[0m")
print(f"{'POSITION':<8} {'NAME':<10} - {'POINTS':<10}")
print("\033[34m" + "-"*60 + "\033[0m")

# Show top 10 players
for fila in ranking:
    posicion += 1
    print(f"{posicion:<8} {fila[0]:<10} - {fila[1]:<10}")

    if posicion == 10:
        break