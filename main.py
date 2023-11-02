from classes.leitner import LeitnerSystem, Card
import os

# Initialize Leitner System
leitner = LeitnerSystem()

# Load cards from file
if input("Load from file? (y/n) ").lower() == "y":
    print("Choose a file from the following list:")
    file_list = os.listdir("data")
    for file_name in file_list:
        print(file_name[:-5])
    file_to_load = input("File name: ")
    leitner.load_from_file(f"data/{file_to_load}.json")

# Display cards
leitner.display()

# Add cards
if input("Add cards? (y/n) ").lower() == "y":
    while True:
        question = input("Question: ")
        answer = input("Answer: ")
        leitner.add_card(Card(question, answer))
        if input("Add another card? (y/n) ").lower() != "y":
            break

# Review cards that are due today
review_cards = leitner.review_today()
if review_cards:
    for card in review_cards:
        # Ask user for answer
        print(f"Box {card.box}: {card.question}")
        user_answer = '"' + input("Your answer: ") + '"'
        if user_answer.lower() == card.answer.lower():
            # Correct answer: move card to next box
            print(
                f"Correct! Moving to box {card.box + 1}. Next review in {leitner.delays[card.box + 1]} days."
            )
            card.box += 1
            if card.box > 7:
                card.box = 7
        else:
            # Incorrect answer: move card to first box
            print("Incorrect. The correct answer is", card.answer, ". Moving to box 1.")
            card.box = 1
    # Update boxes
    leitner._update_boxes()
else:
    # No cards to review
    print("No cards to review today.")

# Save cards to file
leitner.save_to_file(f"data/{file_to_load}.json")
