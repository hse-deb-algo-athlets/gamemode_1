import Jonas.textsuche as lec


#rye test -v
def test_search_with_ret_list ():
    text = "Das ist kein pattern mit einer Ente"
    pattern = "ein"
    expected = [9,25]
    ret = lec.search_with_ret_list(pattern,text)
    assert ret==expected

def test_search_bitmap():
    text = "Das ist kein pattern mit einer Ente"
    pattern = "ein"
    bitmap = [0] * len(text)
    expected = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
    ret = lec.search_bitmap(pattern,text,bitmap)
    assert ret==expected