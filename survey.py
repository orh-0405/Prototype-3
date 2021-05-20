def open_survey():
    import csv
    import sqlite3
    from sqlite3 import Error
    import os.path

    curr_dir = os.path.dirname(__file__)
    file_name = os.path.join(curr_dir, 'Survey Questions - Sheet1.csv')

    rows = []
    with open(file_name, "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            rows.append(row)

    return(rows)

open_survey()