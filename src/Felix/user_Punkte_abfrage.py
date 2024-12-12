import pandas as pd
import os as os
import csv


def user_punkte_laden(name):

    path = os.path.join(os.getcwd(),"user.csv")
    
    if os.path.exists(path) != True:
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Punkte']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)


    df = pd.read_csv(path, index_col = "Name")
    
    if name not in df.index:
        df.loc[name] = 0
        df.to_csv(path)

    Punkte = df.loc[name,"Punkte"]
    
    return Punkte

a = user_punkte_laden("Simon")
print(a)




def user_punkte_hinzufügen(name,punkte):
    path = os.path.join(os.getcwd(),"user.csv")
    df = pd.read_csv(path, index_col = "Name")

    df.loc[name] = punkte
    df.to_csv(path)



user_punkte_hinzufügen("Felix",121)