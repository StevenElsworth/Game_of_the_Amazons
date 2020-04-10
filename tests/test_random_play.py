import pytest
from utility.game_backend import Game
from game import main

def random_game():
    g = Game()

    try:
        g.play()
    except:
        return False
    return True

def random_GUI_game():
    try:
        main(testgame=1)
    except Exception as e:
        print(e)
        return False
    return True


def test_random_game():
    assert random_game()

def test_random_GUI_game():
    assert random_GUI_game()
