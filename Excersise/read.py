import json
import csv
file_path = "C:/Users/remch/flask_project/gay.csv"
try:
    with open(file_path, "r") as file:
        #content = file.read()
        #content = json.load(file)
        content = csv.reader(file)
        for row in content:
            print(row)
except FileNotFoundError:
    print("That file was not found")
except PermissionError:
    print("You not have permission to read that file")