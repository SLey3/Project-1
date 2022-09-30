# File: Wordle.py
# Name: Sergio Ley Languren

"""Wordle main file"""

from WordleGraphics import WordleGWindow, N_COLS, N_ROWS
from utils import choose_word, validate_responce


def wordle():
    """worldle main(0 function. Runs the entire program"""

    answer = "whisk"

    res_initial = []

    def enter_action():
        MN = 5
        for i in range(5):
            res_initial.append(gw.get_square_letter(gw.get_current_row(), N_COLS-MN))
            MN -= 1
        MN += 5
        res = "".join(res_initial).lower()
        result, not_word = validate_responce(gw, res, answer)
        res_initial.clear()
        if result:
            gw.show_message("congratulations! You guessed the correct answer!", "limegreen")
            gw._listeners.clear()
            return
        else:
            if not_word:
                for i in range(5):
                    gw.set_square_letter(gw.get_current_row(), N_COLS-MN, "")
                    MN -= 1
                gw.set_current_row(gw.get_current_row())
            elif gw.get_current_row() == N_ROWS-1:
                gw.show_message(f"Ran out of tries. The answer was: {answer}", "red")
                gw._listeners.clear()
                return
            else:
                gw.set_current_row(gw.get_current_row() + 1)

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
