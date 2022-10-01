# File: utils.py
# Name: Sergio Ley Languren

"""Utility for wordle program"""

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR, N_COLS, N_ROWS, WordleGWindow
from random import choice
from typing import Type
from copy import deepcopy

__all__ = [
    "choose_word",
    "validate_responce"
]

# CONSTANT
MINUS_COL = 5
DUPLICATE_COUNT = 0

# Functions
def choose_word() -> str:
    """Chooses the answer from a list of words of five characters"""
    a = choice(FIVE_LETTER_WORDS)
    return a

# -----------------------------------------------

def _set_key_color_or_not(gw, key_colored, k, c, override_check=False):
    if not key_colored or override_check:
        gw.set_key_color(k.capitalize(), c)

def validate_responce(gw: Type[WordleGWindow], res: str, a: str) -> bool:
    """Validates user response
    :param gw: Main Wordle window class
    :param res: User responce
    :param a: answer to the wordle

    Returns:
        validity AND word-validation
    """
    global MINUS_COL
    a_copy = deepcopy(a)
    correct_counter = 0

    # checks if word is not in the word list
    if res not in FIVE_LETTER_WORDS:
        gw.show_message(f"{res} is not a word!!!")
        return False, True

    for c in a:
        col = N_COLS - MINUS_COL
        ch = gw.get_square_letter(gw.get_current_row(), col).lower()
        key_colored = gw.get_key_color(c.capitalize()) != UNKNOWN_COLOR
        if ch == c:
            gw.set_square_color(gw.get_current_row(), col, CORRECT_COLOR)
            _set_key_color_or_not(gw, key_colored, ch, CORRECT_COLOR, True)
            a_copy = a_copy.replace(ch, "", 1)
            correct_counter += 1
        elif ch in a_copy:
            gw.set_square_color(gw.get_current_row(), col, PRESENT_COLOR)
            _set_key_color_or_not(gw, key_colored, ch, PRESENT_COLOR)
            a_copy = a_copy.replace(ch, "", 1)
        else:
            gw.set_square_color(gw.get_current_row(), col, MISSING_COLOR)
            _set_key_color_or_not(gw, key_colored, ch, MISSING_COLOR)
            a_copy = a_copy.replace(ch, "", 1)
        MINUS_COL -= 1
    
    MINUS_COL = 5

    if correct_counter == 5:
        return True, False
    return False, False



