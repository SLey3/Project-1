# File: utils.py
# Name: Sergio Ley Languren

"""Utility for wordle program"""

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, N_COLS, WordleGWindow
from random import choice
from typing import Any, Type

__all__ = [
    "choose_word",
    "validate_responce"
]

# CONSTANT
MINUS_COL = 4

# Functions
def choose_word() -> str:
    """Chooses the answer from a list of words"""
    a = choice(FIVE_LETTER_WORDS)
    print(f"Answer: {a}")
    return a

def validate_responce(gw: Type[WordleGWindow], res: Any, a: str) -> bool:
    """Validates user response
    :param gw: Main Wordle window class
    :param res: User responce
    :param a: answer to the wordle
    """
    global MINUS_COL
    print(f"Answer: {a}")
    used_char = []
    correct_counter = 0

    # checks if word is not in the word list
    if res not in FIVE_LETTER_WORDS:
        gw.show_message(f"{res} is not a word!!!")
        return
    # compares user responce with the answer
    for ch in res:
        print(f"MINUS_COL: {MINUS_COL}")
        print(f"res character: {ch}")
        row = gw.get_current_row()
        col = N_COLS - MINUS_COL
        if ch in a:
            print("character in answer")
            print(f"used_char list: {used_char}")
            for c in a:
                if c in used_char:
                    if not a.count(c) > 1: # checks if there is more than one character in the answer
                        print("continued")
                        continue
                    else:
                        if c != ch:
                            print("c != ch")
                            i = a.index(c)
                            a = a[i+1:]
                            print(f"Edited Answer: {a}")
                            used_char.remove(c)
                            continue
                print(f"current column: {col}")
                print(f"answer character: {c}")
                if c == ch:
                    print("correct word in the right spot")
                    gw.set_square_color(row, col, CORRECT_COLOR)
                    used_char.append(ch)
                    correct_counter += 1
                    break
                else:
                    print("correct word in the wrong spot")
                    gw.set_square_color(row, col, PRESENT_COLOR)
                    used_char.append(ch)
                    break
            MINUS_COL -= 1
        else:
            print("wrong word")
            gw.set_square_color(row, col, MISSING_COLOR)
            MINUS_COL -= 1
    if correct_counter == 5:
        return True
    return False
