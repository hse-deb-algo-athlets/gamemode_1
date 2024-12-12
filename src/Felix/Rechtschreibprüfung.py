import pandas as pd
input = 'one two three'

a = input.split()
print(a[0])


def minDis(source,target,n,m):
    dp = [[0 for i in range(m+1)]for j in range(n+1)]
    for j in range(0, m + 1):
        dp[0][j] = j
    
    # If first string (source) is empty, only option is to
    #insert all characters of second string

    for i in range (0, n + 1):
        dp[i][0] = i
    
    # Fill dp[][] table in bottom up manner
    for i in range(1, n + 1 ):
        for j in range(1, m + 1):
            # If last characters are same, ignore last char
            # and recur for remaining string
            if (source[i - 1] == target[j - 1]):
                dp[i][j] = dp[i - 1][j - 1]
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], # Insert
                            dp[i - 1][j], # Delete
                            dp[i - 1][j - 1]) #Replace
    print(dp[n][m])
    return dp[n][m]



class Dictionary:
    def __init__(self, max_size=1000):
        self.words = []
        self.max_size = max_size

    def add_word(self, word):
        """Fügt ein Wort zum Wörterbuch hinzu, falls Platz verfügbar ist."""
        if len(self.words) < self.max_size:
            self.words.append(word)
        else:
            print("Dictionary is full.")

    def is_word_in_dictionary(self, word):
        """Überprüft, ob ein Wort im Wörterbuch enthalten ist."""

        abstand_wörter = [100,100,100]
        wörter = ["","",""]

        for word_in_Dictionary in self.words:
            abstand = minDis(word_in_Dictionary,word, len(word_in_Dictionary), len(word))

            if abstand < abstand_wörter[2]:
                if abstand < abstand_wörter[1]:
                    if abstand < abstand_wörter[0]:
                        wörter[0] = word_in_Dictionary
                        abstand_wörter[0] = abstand
                    else:
                         wörter[1] = word_in_Dictionary
                         abstand_wörter[1] = abstand
                else:
                     wörter[2] = word_in_Dictionary
                     abstand_wörter[2] = abstand



        print(wörter)
        return word in self.words
    


# Hauptprogramm
if __name__ == "__main__":
    # Wörterbuch initialisieren
    dictionary = Dictionary()

    # Wörter hinzufügen
    dictionary.add_word("apple")
    dictionary.add_word("banana")
    dictionary.add_word("orange")
    dictionary.add_word("app")

    # Testwort überprüfen
    word_to_check = "apple"

    if dictionary.is_word_in_dictionary(word_to_check):
        print(f"'{word_to_check}' is in the dictionary.")
    else:
        print(f"'{word_to_check}' is NOT in the dictionary.")