# File: Wordle.py
# Name: your name

"""This module is the starter file for the Wordle assignment."""

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_ROWS, N_COLS, UNKNOWN_COLOR
from WordleGraphics import CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR
import random

def wordle():

    def enter_action():
        gw.show_message("You have to implement this function.")

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
