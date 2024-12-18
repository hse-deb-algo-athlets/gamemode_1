input = 'one two three'

print (input.split())

class Dictionary:
    def __init__(self, max_size=1000):
        self.words = []
        self.max_size = max_size
    
    def  min(self, x,  y, z):
        if (x < y and x < z):
            return x
        elif (y < x and y < z):
            return y
        else:
            return z


    def minDis(self,source, target, n, m):

        dp = [[0 for i in range(m + 1)] for j in range(n + 1 )]

    # If second string (target) is empty, only option is to
    #Delete all characters of second string
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
        
        return dp[n][m]

    def add_word(self, word):
        """Fügt ein Wort zum Wörterbuch hinzu, falls Platz verfügbar ist."""
        if len(self.words) < self.max_size:
            self.words.append(word)
        else:
            print("Dictionary is full.")

    def is_word_in_dictionary(self, word):
        """Überprüft, ob ein Wort im Wörterbuch enthalten ist."""
        #Muss rein 3 ähnlichsten Worte
       
        return word in self.words
        
    def simular_words_in_dictionary_3(self,word_):
        simular_words = {}
        for word in self.words:
            distance = self.minDis(word_,word,len(word_),len(word))
            simular_words[word] = distance
        sorted_simular_words = sorted(simular_words.items(), key=lambda x: x[1])
        return sorted_simular_words[:3]

# Hauptprogramm
if __name__ == "__main__":
    # Wörterbuch initialisieren
    dictionary = Dictionary()

    # Wörter hinzufügen
    dictionary.add_word("apple")
    dictionary.add_word("banana")
    dictionary.add_word("orange")

    # Testwort überprüfen
    words_to_check = "apple"

    #if dictionary.is_word_in_dictionary(words_to_check):
    #    print(f"'{words_to_check}' is in the dictionary.")
    #else:
    #    print(f"'{words_to_check}' is NOT in the dictionary.")
    print(f"3 most simular words:  ")
    for key in range(0,3):
        print(dictionary.simular_words_in_dictionary_3(words_to_check)[key])