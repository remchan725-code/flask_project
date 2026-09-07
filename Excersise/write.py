import json
import csv
txt_data = "i love pizza"
employee = [["Name","Age","Job"],
            ["Duc",24,"BackEnd Dev"],
            ["Nam",24,"Database Engineer"],
            ["Huy",24,"IT Helpdesk"]]
file_path = "gay.json"
try:
    with open(file_path,"w") as file:
        writer = csv.writer(file)
        for row in employee:
            writer.writerow(row)
        print(f"CSV file {file_path} was created")
except PermissionError :
    print("You don't have any permission to do in this file")