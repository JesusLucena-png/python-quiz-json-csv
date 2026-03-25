import json
import random
import csv
from datetime import datetime

fecha_actual = datetime.now()

# Question categories
questions_movies = []
questions_series = []
questions_anime = []
questions_videogames = []
questions_music = []
questions_basic_programming = []

# Store player results
results = []

# Store ranking
ranking = []

# Load questions from JSON file
with open("data.json", "r", encoding="utf-8") as file:
    data = json.loads(file.read())

    # Iterate through all questions
    for question in data:
        for key, value in question.items():

            # Classify questions by category
            if key == "categoria" and value == "Películas":
                questions_movies.append(question)

            elif key == "categoria" and value == "Series":
                questions_series.append(question)

            elif key == "categoria" and value == "Anime":
                questions_anime.append(question)

            elif key == "categoria" and value == "Videojuegos":
                questions_videogames.append(question)

            elif key == "categoria" and value == "Música":
                questions_music.append(question)

            elif key == "categoria" and value == "Programación Básica":
                questions_basic_programming.append(question)
    

# Function to confirm if the user wants to exit
def confirm_exit(message="Press (n) to finish and any key to continue: "):
    
    user_option = input(f"\n\033[31m >> \033[0m{message}").strip().lower()
        
    if user_option == "n":
        return True     


# Function to display a random question
def show_question(question_list, question_counter, user_index):
    
    # Select a random question
    random_index = random.randint(0, len(question_list) - 1)
    question_data = question_list[random_index]

    # Print question
    print(f"\n{question_counter}. {question_data.get('pregunta')}\n")

    # Get options
    options = question_data.get("opciones")

    # Display options
    for option, value in options.items():
        print(f"{option}. {value}")

    valid_option = True
    while valid_option:
        
        # Ask user for input
        selected_option = input("\n\033[34m >> \033[0mEnter an option: ").upper()

        # Validate name (not necessary here but kept as original logic)
        if not selected_option.strip():
            print("\n\033[1;31m" + "-"*60 + f"\nError: Please enter a option." + "\n" + "-"*60 + "\033[0m")
            continue

        # Validate option
        if selected_option in ["A", "B", "C", "D"]:
            
            # Check correct answer
            if selected_option == question_data.get("respuesta_correcta"):
                print("\n\033[1;32m+ 20 points\033[0m")

                # Save correct result
                results[user_index].append({
                    "pregunta": question_data.get("pregunta"),
                    "opcion": selected_option,
                    "puntos": 20,
                })
                return 20
            else:
                print("\n\033[1;31m+ 0 points\033[0m")

                # Save incorrect result
                results[user_index].append({
                    "pregunta": question_data.get("pregunta"),
                    "opcion": selected_option,
                    "puntos": 0,
                })
                return 0
        else:
            # Invalid option message
            print("\n\033[1;31m" + "-"*60 + f"\nError: Please enter a valid option." + "\n" + "-"*60 + "\033[0m")
            continue


# Game control
game_active = True
while game_active:

    validate_name = True
    while validate_name:

        # UI separator
        print("\033[34m" + "-"*60 + "\033[0m")

        # Ask for username
        nombre = input("\n\033[34m >> \033[0mEnter user name: ")

        print("\033[34m" + "-"*60 + "\033[0m")

        # Validate input
        if not nombre.strip():
            print("\n\033[1;31m" + "-"*60 + f"\nError: Please enter a name." + "\n" + "-"*60 + "\033[0m")
            continue
        else:
            # Save user
            user_index = len(results)
            results.append([nombre, fecha_actual])
            validate_name = False

    total_score = 0
    question_number = 1

    # Select 5 random categories
    random_categories = random.sample(range(0, 6), 5)

    while question_number != 5:

        # All category lists
        question_lists = [
            questions_movies,
            questions_series,
            questions_anime,
            questions_music,
            questions_videogames,
            questions_basic_programming
        ]

        # Iterate through selected categories
        for num in random_categories:
            score = show_question(question_lists[num], question_number, user_index)
            total_score += score
            question_number += 1
            print("\033[34m" + "-"*60 + "\033[0m")
        
        break

    # Save total score
    results[user_index].append(total_score)

    print("\033[34m" + "-"*60 + "\033[0m")

    # Show summary
    print(f"Name: {results[user_index][0]}")
    print(f"Date: {results[user_index][1]}")

    # Show each question result
    for i, question_data in enumerate(results[user_index][2:7]):
        print(f"\n{i+1}. {question_data['pregunta']}")
        print(f"Selected Option: {question_data['opcion']}  |  Points: {question_data['puntos']}\n")
    
    print(f"Total Points: {results[user_index][7]}")

    # Add to ranking
    ranking.append([results[user_index][0], results[user_index][7]])

    print("\033[34m" + "-"*60 + "\033[0m")

    # Ask to exit
    exit_game = confirm_exit()
    if exit_game:
        game_active = False
    else:
        continue


# Save ranking to CSV
with open("ranking.csv", mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(ranking)


# Reload ranking from CSV
ranking = []
try:
    with open("ranking.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                ranking.append([row[0], int(row[1])])
except FileNotFoundError:
    print("The file ranking.csv does not exist yet.")


# Sort ranking (highest score first)
ranking.sort(key=lambda x: x[1], reverse=True)

# Display ranking
print("\n\033[34m" + "-"*60 + "\033[0m")
print("RANKING")
print("\033[34m" + "-"*60 + "\033[0m")
print(f"{'POSITION':<8} {'NAME':<10} - {'POINTS':<10}")
print("\033[34m" + "-"*60 + "\033[0m")

# Show top 10
for cont, row in enumerate(ranking):

    print(f"{cont+1:<8} {row[0]:<10} - {row[1]:<10}")

    if cont+1 == 10:
        break