# Trivia Game with Ranking 🎮

## User Story

**As a** player  
**I want** to enter my name, answer trivia questions, and see my final score  
**So that** I can evaluate my knowledge and compare myself with other players  

---

## Acceptance Criteria

### Game Start

- The system must request the player's name before starting the game.
- The player's name is required to continue.

---

### Questions

- The system must load questions from a JSON file.
- The system must select **5 random questions without repetition** in each game.
- Each question must display:
  - The question text
  - 4 answer options: A, B, C, and D
- The player must be able to select only one answer per question.

---

### Scoring

- Each correct answer awards **20 points**.
- Incorrect answers give **0 points**.
- At the end of the 5 questions, the system must display:
  - Total score obtained
  - Number of correct answers

---

### Result Persistence

- At the end of the game, the system must save the results in a CSV file.
- Each row in the CSV must contain:
  - Player name
  - Score obtained
  - Date and time of the game

---

### Ranking

- The system must allow viewing a player ranking.
- The ranking must display the **top 10 players with the highest scores**.
- The ranking must be sorted from highest to lowest score.

---

## Definition of Done

- The game runs correctly (console-based).
- Questions are properly loaded from the JSON file.
- Questions do not repeat within the same game.
- The CSV file is automatically created if it does not exist.
- Results are correctly saved in the CSV file.
- The ranking correctly displays the top 10 sorted players.
- The system has been tested with multiple game sessions.

---

## Technologies Used

- Python 3
- JSON (for questions storage)
- CSV (for ranking persistence)

---

## How to Run

1. Make sure you have Python installed.
2. Place your `data.json` file in the same directory.
3. Run the script:

```bash
python main.py