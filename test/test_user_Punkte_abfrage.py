import Felix.user_Punkte_abfrage

def test_user_punkte_laden():
    User = "Test_User_1"

    expectet = [69]

    ret = Felix.user_Punkte_abfrage.user_punkte_laden(User)

    assert ret == expectet, "Ergebnis ist nicht wie erwartet"



def test_user_punkte_hinzufügen():
    User = "Test_User_2"
    Punkte = 1

    expectet = [Punkte]

    Felix.user_Punkte_abfrage.user_punkte_hinzufügen(User,Punkte)
    ret = Felix.user_Punkte_abfrage.user_punkte_laden(User)

    assert ret == expectet, "Ergebniss ist Falsch"