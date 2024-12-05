import pandas as pd
import os as os
import csv


def user_punkte(name):

    user_Date_csv = os.path.join(os.getcwd(),"user.csv")
    
    if os.path.exists(user_Date_csv) != True:
        with open(user_Date_csv, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Punkte']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

    path = os.path.join(os.getcwd(),"user.csv")
    df = pd.read_csv(path, index_col = "Name")
    
    if name not in df.index:
        df.loc[name] = 0
        df.to_csv(path)

    Punkte = df.loc[name]
    
    return Punkte


a = user_punkte("Simon")
print(a)