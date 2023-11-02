import json
from datetime import datetime, timedelta


class Card:
    """A card in a Leitner box."""

    def __init__(
        self, question, answer, created_date=datetime.now().date().strftime("%Y-%m-%d")
    ):
        """
        Initialize the card.
        Args:
            question: A string representing the question on the card.
            answer: A string representing the answer on the card.
            created_date: A string representing the date the card was created.
        Returns:
            None
        """

        self.question = question
        self.answer = answer
        self.box = 1
        self.created_date = created_date

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
        }


class LeitnerSystem:
    """A Leitner system for studying flash cards."""

    def __init__(self):
        """
        Initialize the Leitner system.
        """

        self.boxes = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        self.delays = {1: 1, 2: 2, 3: 4, 4: 7, 5: 15, 6: 30, 7: 60}

    def add_card(self, card):
        """
        Add a card to box 1.
        Args:
            card: A Card object.
        Returns:
            None
        """

        self.boxes[1].append(card)

    def study(self):
        """
        Study the cards in box 1. Move them to the next box if they are answered correctly.
        Args:
            None
        Returns:
            None
        """

        for box in self.boxes.values():
            for card in box:
                print(card.question)
                user_answer = input("Your answer: ")
                if user_answer.lower() == card.answer.lower():
                    print("Correct!")
                    card.box += 1
                    if card.box > 7:
                        card.box = 7
                else:
                    print("Incorrect. The correct answer is", card.answer)
                    card.box = 1
        self._update_boxes()

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
                created_date = datetime.strptime(card.created_date, "%Y-%m-%d").date()
                delay = self.delays[card.box]
                review_date = created_date + timedelta(days=delay)
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

    def save_to_file(self, filepath):
        """
        Save the current state of the Leitner system to a file.
        Args:
            filepath: The path to the file to save to.
        Returns:
            None
        """
        data = {
            "boxes": {
                box: [card.to_dict() for card in self.boxes[box]] for box in self.boxes
            }
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load_from_file(self, filepath):
        """
        Load the current state of the Leitner system from a file.
        Args:
            filepath: The path to the file to load from.
        Returns:
            None
        """
        with open(filepath, "r") as f:
            data = json.load(f)
        for box in data["boxes"]:
            for card_data in data["boxes"][box]:
                card = Card(
                    card_data["question"],
                    card_data["answer"],
                    card_data["created_date"],
                )
                card.box = card_data["box"]
                self.boxes[int(box)].append(card)

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
