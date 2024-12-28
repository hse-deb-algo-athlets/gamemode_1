
import Felix.Textsuche


def test_textsuche():
    text = "Das ist ein Test"
    pattern = "ein"

    expectet = [8]

    ret = Felix.Textsuche.search_with_ret_list(pattern, text)

    assert ret == expectet, "Ergebnis ist nicht wie erwartet"


def test_bitmap():
    text = "Das ist ein Test"
    pattern = "ein"

    expectet = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]

    ret = Felix.Textsuche.search_bitmap(pattern, text)

    assert ret == expectet, "Ergebnis ist nicht wie erwartet"