import pandas as pd
import os as os
import csv


def user_punkte(name):

    if os.path.exists("user.csv") != True:
        with open("user.csv", 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Punkte']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

    path = os.path.join(os.getcwd(),"user.csv")
    df = pd.read_csv(path, index_col = "Name")
    
    if name not in df.index:
        df.loc[name] = 0
        #df.to_csv(path, mode='a', header=False)

        try:
            with open(path, mode='a', newline='') as f:
                df.loc[name].to_csv(f, header=False, index=False)  # Index nicht schreiben
        except IOError:
            print("Fehler beim Schreiben in die CSV-Datei.")

    Punkte = df.loc[name]
    
    return Punkte




a = user_punkte("Marie")
print(a)
