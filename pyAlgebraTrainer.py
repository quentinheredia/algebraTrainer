import random
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        initial_leaderboard = {"easy": [], "medium": [], "hard": []}
        with open(LEADERBOARD_FILE, "w") as file:
            json.dump(initial_leaderboard, file, indent=4)
        return initial_leaderboard
    
    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)

def reset_leaderboard():
    empty_leaderboard = {"easy": [], "medium": [], "hard": []}
    save_leaderboard(empty_leaderboard)
    print("Leaderboard has been reset.")

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)

def update_leaderboard(leaderboard, difficulty, username, score):
    leaderboard[difficulty].append({"username": username, "score": score})
    leaderboard[difficulty] = sorted(leaderboard[difficulty], key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)

def display_leaderboard(leaderboard, difficulty):
    print(f"\nLeaderboard ({difficulty.title()} Difficulty):")
    for entry in leaderboard[difficulty]:
        print(f"{entry['username']}: {entry['score']}")


def generate_question(operation, difficulty):
    if difficulty == 'easy':
        num2 = random.randint(1, 10)
    elif difficulty == 'medium':
        num2 = random.randint(1, 50)
    else:  # hard
        num2 = random.randint(1, 100)

    if operation == '**':
        num2 = random.randint(1, 3 if difficulty == 'easy' else 5)  # Smaller exponent

    if operation == '/':
        # Ensure division results in whole numbers or simple decimals
        multiplier = random.choice([0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5])
        num1 = num2 * multiplier
    else:
        num1 = random.randint(1, num2 * 10)

    question = f"What is {num1} {operation} {num2}?"
    answer = eval(f"{num1} {operation} {num2}")
    return question, answer

def ask_questions(operations, num_questions, difficulty):
    score = 0
    for i in range(num_questions):
        operation = random.choice(operations)
        question, correct_answer = generate_question(operation, difficulty)
        print(f"Question {i+1}: {question}")
        user_answer = input("Your answer (or 'quit' to exit): ")

        if user_answer.lower() == 'quit':
            return score, i  # Return current score and number of questions answered

        try:
            if float(user_answer) == correct_answer:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer is {correct_answer}.")
        except ValueError:
            print("Invalid input. Skipping to the next question.")

    return score, num_questions

# Test functions
def test_generate_question():
    for operation in ['+', '-', '*', '/', '**']:
        for difficulty in ['easy', 'medium', 'hard']:
            question, answer = generate_question(operation, difficulty)
            assert isinstance(question, str), "Question must be a string"
            assert isinstance(answer, (int, float)), "Answer must be a number"
    print("generate_question: All tests passed.")

def test_calculate_grade():
    assert calculate_grade(10, 10) == 'A'
    assert calculate_grade(7, 10) == 'B'
    assert calculate_grade(5, 10) == 'C'
    assert calculate_grade(3, 10) == 'D'
    assert calculate_grade(1, 10) == 'F'
    assert calculate_grade(0, 0) == 'N/A'
    print("calculate_grade: All tests passed.")

def calculate_grade(score, num_questions):
    if num_questions == 0:  # Avoid division by zero
        return 'N/A'
    percentage = (score / num_questions) * 100

    if percentage >= 90:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 30:
        return 'D'
    else:
        return 'F'

def main():

    leaderboard = load_leaderboard()

    while True:
        print("\nAlgebra Practice App")
        print("1. Play Game")
        print("2. Reset Leaderboard")
        print("3. Exit")
        user_choice = input("Choose an option (1-3): ")

        if user_choice == '1':
            # Ensure username is valid
            while True:
                username = input("Enter your username (3-8 characters): ")
                if 3 <= len(username) <= 8:
                    break
                print("Invalid username length. Please try again.")

            while True:
                print("\nAlgebra Practice App")
                print("Type 'exit' at any point to quit the game.")
                difficulty = input("Choose difficulty (easy, medium, hard): ").lower()

                if difficulty == 'exit':
                    print("Exiting game. Goodbye!")
                    break

                try:
                    num_questions = int(input("How many questions would you like to answer (1-20)? "))
                    if num_questions <= 0:
                        raise ValueError
                except ValueError:
                    print("Invalid number of questions. Please enter a positive integer.")
                    continue

                print("1. Addition / Subtraction")
                print("2. Multiplication / Division")
                print("3. Exponents")
                print("4. Combined Questions")
                choice = input("Choose an option (1-4): ")

                if choice.lower() == 'exit':
                    print("Exiting game. Goodbye!")
                    break

                if choice == '1':
                    operations = ['+', '-']
                elif choice == '2':
                    operations = ['*', '/']
                elif choice == '3':
                    operations = ['**']
                elif choice == '4':
                    operations = ['+', '-', '*', '/', '**']
                else:
                    print("Invalid choice. Please select a valid option.")
                    continue

                score, questions_answered = ask_questions(operations, num_questions, difficulty)
                grade = calculate_grade(score, questions_answered)
                print(f"\nYour score: {score}/{questions_answered}")
                print(f"Your grade: {grade}")

                if questions_answered > 10:
                    update_leaderboard(leaderboard, difficulty, username, score)

                display_leaderboard(leaderboard, difficulty)

                again = input("\nDo you want to play again? (yes/no): ")
                if again.lower() not in ['yes', 'y']:
                    print("Thank you for playing! Goodbye!")
                    break

        # Rest of Menu Choices
        elif user_choice == '2':
            reset_leaderboard()
            continue
        elif user_choice == '3':
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    test_generate_question()
    test_calculate_grade()
    main()
