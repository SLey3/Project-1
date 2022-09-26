# File: Wordle.py
# Name: Sergio Ley Languren

"""This module is the starter file for the Wordle assignment."""

from WordleGraphics import WordleGWindow, N_ROWS, N_COLS, UNKNOWN_COLOR
from utils import choose_word, validate_responce


def wordle():

    answer = "scums"

    res_initial = []

    def enter_action():
        MN = 5
        for i in range(5):
            res_initial.append(gw.get_square_letter(gw.get_current_row(), N_COLS-MN))
            MN -= 1
        res = "".join(res_initial).lower()
        print(res)
        result = validate_responce(gw, res, answer)
        res_initial.clear()
        print(res_initial)
        if result:
            gw.show_message("congratulations! You guessed the correct answer!", "limegreen")
            gw._listeners.clear()
            return
        else:
            gw.set_current_row(gw.get_current_row() + 1)

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
