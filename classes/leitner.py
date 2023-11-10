import json
import os
import random
from datetime import datetime, timedelta


class Card:
    """A card in a Leitner box."""

    def __init__(
        self,
        question,
        answer,
        box=1,
        created_date=datetime.now().date().strftime("%Y-%m-%d"),
    ):
        """
        Initialize the card.
        Args:
            question: A string representing the question on the card.
            answer: A string representing the answer on the card.
            box: An integer representing the box the card is in.
            created_date: A string representing the date the card was created.
            last_failed_date: A string representing the date the card was last failed.
        Returns:
            None
        """

        self.question = question
        self.answer = answer
        self.box = box
        self.created_date = created_date
        self.last_failed_date = created_date
        self.last_answered_date = created_date

    def to_dict(self):
        """
        Convert the card to a dictionary.
        Args:
            None
        Returns:
            A dictionary representing the card.
        """
        return {
            "question": self.question,
            "answer": self.answer,
            "box": self.box,
            "created_date": self.created_date,
            "last_failed_date": self.last_failed_date,
            "last_answered_date": self.last_answered_date,
        }


class LeitnerSystem:
    """A Leitner system for studying flash cards."""

    def __init__(self):
        """
        Initialize the Leitner system.
        """

        self.boxes = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        self.delays = {1: 1, 2: 2, 3: 4, 4: 7, 5: 15, 6: 30, 7: 60}
        self.cards = [card for box in self.boxes.values() for card in box]
        self.folder = "data/"
        self.extension = ".json"
        self.new_cards_count = 0
        self.file_path = None
        self.file_name = None

    def add_card(self, card, box=1):
        """
        Add a card to box 1.
        Args:
            card: A Card object.
            box: An integer representing the box to add the card to.
        Returns:
            None
        """

        self.boxes[box].append(card)
        self.cards.append(card)

    def check_cards_count(self):
        if self.new_cards_count >= 10:
            input(
                "You have already added 10 new cards today. Please wait tomorrow to add more. Press any key to continue..."
            )
            return False
        return True

    def write_cards(self):
        """
        Loop in order to add cards to the system.
        Args:
            None
        Returns:
            None
        """
        if self.check_cards_count() == False:
            return
        add_card = input("Add card? (y/n) ")
        while add_card.lower() not in ["n", "y"]:
            add_card = input("Add card? (y/n) ")
        while add_card.lower() == "y":
            question = input("Question: ")
            answer = input("Answer: ")
            self.add_card(Card(question, answer))
            self.new_cards_count += 1
            print(self.new_cards_count, "new cards added today.")
            if self.check_cards_count() == False:
                return
            add_card = input("Add another card? (y/n) ")
            while add_card.lower() not in ["n", "y"]:
                add_card = input("Add another card? (y/n) ")

    def study(self, review_cards):
        """
        Study the cards due today.
        Move them to the next box if they are answered correctly.
        Reset them to box 1 if they are answered incorrectly.
        Args:
            review_cards: A list of Card objects.
        Returns:
            None
        """

        if not review_cards:
            print("No cards to review today.")
            return

        review_groups = {}
        for card in review_cards:
            if card.box not in review_groups:
                review_groups[card.box] = []
            review_groups[card.box].append(card)

        for box, cards in review_groups.items():
            random.shuffle(cards)

        sorted_cards_list = []
        for box in sorted(review_groups.keys()):
            sorted_cards_list.extend(review_groups[box])

        for card in sorted_cards_list:
            print(f"Box {card.box}: {card.question}")
            user_answer = input("Your answer: ")
            if user_answer.lower() == card.answer.lower():
                print("Correct!")
                card.last_answered_date = datetime.now().date().strftime("%Y-%m-%d")
                card.box += 1
                if card.box > 7:
                    card.box = 7
            else:
                print("Incorrect. The correct answer is", card.answer)
                card.box = 1
                card.last_failed_date = datetime.now().date().strftime("%Y-%m-%d")
                card.last_answered_date = datetime.now().date().strftime("%Y-%m-%d")
        self._update_boxes()
        input("Press any key to continue...")

    def review_today(self):
        """
        Check if there is any card in the box that must be reviewed today.
        Args:
            None
        Returns:
            A list of cards that must be reviewed today.
        """

        today = datetime.now().date()
        review_cards = []
        for box in self.boxes.values():
            for card in box:
                last_answered_date = datetime.strptime(
                    card.last_answered_date, "%Y-%m-%d"
                ).date()
                delay = self.delays[card.box]
                review_date = last_answered_date + timedelta(days=delay)
                if review_date <= today:
                    review_cards.append(card)
        return review_cards

    def _update_boxes(self):
        """
        Move cards to the next box.
        Args:
            None
        Returns:
            None
        """

        new_boxes = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        for box in self.boxes.values():
            for card in box:
                new_boxes[card.box].append(card)
        self.boxes = new_boxes
        self.display()

    def save_to_file(self, filepath, load_option):
        """
        Save the current state of the Leitner system to a file.
        Args:
            filepath: The path to the file to save to.
            load_option: A string representing whether to load from a file or not.
        Returns:
            None
        """

        file_list = os.listdir("data")
        combined_system = LeitnerSystem()

        if (filepath.split("/")[-1] in file_list) & (load_option.lower() == "n"):
            add_new_questions = input(
                f"File {filepath} already exists. Add new questions to this file? (y/n) "
            )
            if add_new_questions.lower() == "n":
                confirm = input("Overwrite current file? (y/n) ")
                while confirm.lower() not in ["n", "y"]:
                    confirm = input("Overwrite current file? (y/n) ")
                if confirm.lower() == "n":
                    return

            if add_new_questions.lower() == "y":
                existing_system = LeitnerSystem()
                existing_system.load_from_file(load_option="n", filepath=self.file_path)
                for card in existing_system.cards:
                    combined_system.add_card(card)

        for card in self.cards:
            combined_system.add_card(card, box=card.box)

        data = {
            "boxes": {
                box: [card.to_dict() for card in combined_system.boxes[box]]
                for box in combined_system.boxes
            }
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load_from_file(self, load_option):
        """
        Load the current state of the Leitner system from a file.
        Args:
            load_option: A string representing whether to load from a file or not.
            filepath: The path to the file to load from.
        Returns:
            None
        """
        if load_option == "y":
            while self.file_name not in os.listdir("data"):
                print("Choose a file from the following list:")
                for file in os.listdir("data"):
                    print(file[:-5])
                self.file_name = input("File name: ") + self.extension
                self.file_path = self.folder + self.file_name
            with open(self.file_path, "r") as f:
                data = json.load(f)

            current_date = datetime.now().date().strftime("%Y-%m-%d")

            self.new_cards_count = sum(
                1
                for card_data in data["boxes"].values()
                for card in card_data
                if card["created_date"] == str(current_date)
            )

            for box in data["boxes"]:
                for card_data in data["boxes"][box]:
                    card = Card(
                        card_data["question"],
                        card_data["answer"],
                        card_data["box"],
                        card_data["created_date"],
                    )
                    try:
                        card.last_failed_date = card_data["last_failed_date"]
                    except KeyError:
                        card.last_failed_date = card_data["created_date"]
                    try:
                        card.last_answered_date = card_data["last_answered_date"]
                    except KeyError:
                        card.last_answered_date = card_data["created_date"]
                    self.boxes[int(box)].append(card)
                    self.cards.append(card)
        elif load_option == "n":
            self.file_path = (
                self.folder + input("Choose a name for your file: ") + self.extension
            )

    def display(self):
        """
        Display the cards in each box.
        Args:
            None
        Returns:
            None
        """
        for box in self.boxes:
            print(f"Box {box}:")
            for card in self.boxes[box]:
                print(f"\t{card.question}")

    def ask_for_loading(self):
        """
        Ask the user if they want to load from a file.
        Args:
            None
        Returns:
            A string representing whether to load from a file or not.
        """
        load_option = input("Load from file? (y/n) ")
        while load_option.lower() not in ["n", "y"]:
            load_option = input("Load from file? (y/n) ")
        return load_option
