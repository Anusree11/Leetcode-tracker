import csv
from datetime import date

FILE_NAME = "leetcode_tracker.csv"

def add_problem():
    problem_name = input("Problem name: ")
    difficulty = input("Difficulty (Easy/Medium/Hard): ")
    topic = input("Topic (Array/String/etc): ")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date.today(), problem_name, difficulty, topic])

    print("Problem added succesfully")

def menu():
    print("\nLeetCode Tracker")
    print("1. Add problem")
    print("2. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_problem()
    elif choice == "2":
        print("Goodbye!")
    else:
        print("Invalid choice")

menu()