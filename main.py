from classes.leitner import LeitnerSystem
import os
import sys


# determine if application is a script file or frozen exe
if getattr(sys, "frozen", False):
    os.chdir("../..")

# Initialize Leitner System
leitner = LeitnerSystem()

# Load cards from file
load_option = leitner.ask_for_loading()
if load_option.lower() == "y":
    leitner.load_from_file(load_option)
else:
    leitner.file_path = (
        leitner.folder + input("Choose a name for your file: ") + leitner.extension
    )

# Display cards
leitner.display()

# Add cards
leitner.write_cards()

# Review cards that are due today
review_cards = leitner.review_today()
leitner.study(review_cards)

# Save cards to file
leitner.save_to_file(leitner.file_path, load_option=load_option)
