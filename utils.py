# File: utils.py
# Name: Sergio Ley Languren

"""Utility for wordle program"""

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR, N_COLS, N_ROWS, WordleGWindow
from random import choice
from typing import Type

__all__ = [
    "choose_word",
    "validate_responce"
]

# CONSTANT
MINUS_COL = 5

# Functions
def choose_word() -> str:
    """Chooses the answer from a list of words"""
    a = choice(FIVE_LETTER_WORDS)
    print(f"Answer: {a}")
    return a

def _set_key_color_or_not(gw, key_exists, k, c, override_check=False):
    if not key_exists or override_check:
        gw.set_key_color(k.capitalize(), c)


def drop_letter(string: str, let_index: int):
    new_str = ""
    for i in range(len(string)):
        if i == let_index:
            new_str += " "
        else:
            new_str += string[i]
    return new_str

def validate_responce(gw: Type[WordleGWindow], res: str, a: str) -> bool:
    """Validates user response
    :param gw: Main Wordle window class
    :param res: User responce
    :param a: answer to the wordle

    Returns:
        validity AND word-validation
    """
    global MINUS_COL
    used_char = []
    correct_counter = 0

    # checks if word is not in the word list
    if res not in FIVE_LETTER_WORDS:
        gw.show_message(f"{res} is not a word!!!")
        return False, True
    # compares user responce with the answer
    for ch in res:
        print(f"user responce character: {ch}")
        row = gw.get_current_row()
        col = N_COLS - MINUS_COL
        key_exist = gw.get_key_color(ch.capitalize()) != UNKNOWN_COLOR
        print(f"Current Column: {col}")
        print(f"used_char list: {used_char}")
        if ch in a:
            for c in a:
                print(f"answer character: {c}")
                if c in used_char or ch in used_char:
                    print("user or answer character detected in used_char list")
                    print(a.count(c))
                    print(res.count(ch))
                    if a.count(ch) > 1 and res.count(ch) > 1: # checks if there is more than one character in the answer
                        if c != ch: # if the answer has more than one of the same character and the current 
                                    # answer character does not match the cureent responce character
                            r = a.find(c)
                            print(r)
                            a = a.replace(c, "") if r != -1 else a
                            print(f"new answer: {a}")
                            continue
                    else:
                        print("skipping current character in the answer for loop")
                        continue

                if c == ch:
                    print("character is correct and in the correct position")
                    gw.set_square_color(row, col, CORRECT_COLOR)
                    used_char.append(ch)
                    correct_counter += 1
                    _set_key_color_or_not(gw, key_exist, ch, CORRECT_COLOR, True)
                    break
                else:
                    print("character is correct but in the wrong position")
                    gw.set_square_color(row, col, PRESENT_COLOR)
                    actual_word = a[col] if col != 5 else a[col-1]
                    used_char.extend([ch, actual_word])
                    _set_key_color_or_not(gw, key_exist, ch, PRESENT_COLOR)
                    break
            MINUS_COL -= 1
        else:
            if res.count(ch) > 1 and res in used_char:
                i = used_char.index(ch)
                used_char.pop(i)
            print("character not in answer")
            print(col-1)
            used_char.append(a[col-1]) if col == 5 else used_char.append(a[col])
            
            gw.set_square_color(row, col, MISSING_COLOR)
            _set_key_color_or_not(gw, key_exist, ch, MISSING_COLOR)
            MINUS_COL -= 1
    MINUS_COL += 5
    if correct_counter == 5:
        return True, False
    return False, False
