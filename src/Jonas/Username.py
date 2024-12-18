import pandas as pd
import os
import csv
def Userpunkte():
    path_csv = os.path.join(os.getcwd(),"user.csv")
    if os.path.isfile(path_csv)==True:
        print("User True")
    else:
        with open('user.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            fieldnames = ['User', 'Punkte']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    df = pd.read_csv(path_csv)