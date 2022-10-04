# File: utils.py
# Name: Sergio Ley Languren

"""Utility for wordle program"""

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR, N_COLS, N_ROWS, WordleGWindow
from random import choice
from typing import Type, Union, Optional
from copy import deepcopy
from tempfile import NamedTemporaryFile
from os import getcwd, unlink

__all__ = [
    "choose_word",
    "validate_responce",
    "ScoreFileParser"
]

# CONSTANT
MINUS_COL = 5

t = None

# Functions
def choose_word() -> str:
    """Chooses the answer from a list of words of five characters"""
    a = choice(FIVE_LETTER_WORDS)
    print(a)
    return a

# -----------------------------------------------

def _set_key_color_or_not(gw, key_colored, k, c, override_check=False):
    if not key_colored or override_check:
        gw.set_key_color(k.capitalize(), c)
    
def _add_color(gw, column, keycolored, character, color, ac, oc: Optional[bool] = None):
    gw.set_square_color(gw.get_current_row(), column, color)
    if oc:
        _set_key_color_or_not(gw, keycolored, character, color, oc)
    else:
        _set_key_color_or_not(gw, keycolored, character, color)
    a_copy = ac.replace(character, "", 1)
    return a_copy

def add_tempfile() -> NamedTemporaryFile:
    """creates score file"""
    global t
    if not t:
        t = NamedTemporaryFile("w+", encoding="utf-8", prefix="wordle_", dir=getcwd(), delete=False)
    return t

def validate_responce(gw: Type[WordleGWindow], res: str, a: str) -> Union[bool, bool, NamedTemporaryFile]:
    """Validates user response
    :param gw: Main Wordle window class
    :param res: User responce
    :param a: answer to the wordle

    Returns:
        validity | word-validation | score tempfile
    """
    global MINUS_COL
    a_copy = deepcopy(a)
    correct_counter = 0

    temp = add_tempfile()
    # checks if word is not in the word list
    if res not in FIVE_LETTER_WORDS:
        gw.show_message(f"{res} is not a word!!!")
        return False, True, temp

    for c in a:
        col = N_COLS - MINUS_COL
        ch = gw.get_square_letter(gw.get_current_row(), col).lower()
        key_colored = gw.get_key_color(c.capitalize()) != UNKNOWN_COLOR
        if ch == c:
            a_copy = _add_color(gw, col, key_colored, ch, CORRECT_COLOR, a_copy, True)
            correct_counter += 1
        elif ch in a_copy:
            a_copy = _add_color(gw, col, key_colored, ch, PRESENT_COLOR, a_copy)
        else:
            a_copy = _add_color(gw, col, key_colored, ch, MISSING_COLOR, a_copy)
        MINUS_COL -= 1
    
    line = f"{gw.get_current_row()}|{correct_counter}\n"
    temp.write(line)
    temp.flush()
    
    MINUS_COL = 5

    if correct_counter == 5:
        return True, False, temp
    return False, False, temp


class ScoreFileParser:
    """
    Parses and adds score to wordle grid based on the scorefile
    """
    cleared = False

    def __init__(self, gw: Type[WordleGWindow], tmp: Type[NamedTemporaryFile]):
        self.gw = gw
        self.tmpfile = tmp

    def parse(self):
        """Main function to parse the score file"""
        self.tmpfile.seek(0)
        lines = self.tmpfile.readlines()
        if not self.cleared:
            self.clear_grid()
            self.parse()
        for l in lines:
            row = l.split("|")[0]
            correct_points = l.split("|")[1].replace("\n", "")
            self.gw.set_square_letter(int(row), 0, str(int(row) + 1))
            self.gw.set_square_letter(int(row), 4, correct_points)
            self.gw.set_square_color(int(row), 0, PRESENT_COLOR)
            if int(correct_points) == 5:
                self.gw.set_square_color(int(row), 4, CORRECT_COLOR)
            else:
                self.gw.set_square_color(int(row), 4, MISSING_COLOR)
        self.gw.show_message("rows                           points", "limegreen")

    def clear_grid(self):
        """Clear wordle grid"""
        for i in range(N_ROWS):
            self.gw.set_current_row(i)
            for j in range(N_COLS):
                self.gw.set_square_letter(i, j, "")
        self.cleared = True


    def close(self):
        """closes the score file"""
        self.tmpfile.close()
        path = self.tmpfile.name
        print(path)
        unlink(path)