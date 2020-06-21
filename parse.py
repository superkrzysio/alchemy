import os
import json

# script #1
# parse table copied from Wiki into json

def extract(link):
   link = link.replace("[[", "").replace("]]", "")
   link = link.split("|")[-1]
   return link

def clean(row):
    if not row[0] == "|":
        raise Exception("Expected pipe to be a first char, but got: " + row)
    row = row[1:]
    row = row.replace("\n", "")
    row = row.replace("‡", "")
    row = row.replace("*", "")
    row = row.replace("†", "")
    # parsing
    while True:
        if row.find("[[") == -1:
            break
        part = row[row.find("[["):row.find("]]")+2]
        txt = extract(part)
        row = row.replace(part, txt)
    return row


ingredients = []

counter = 0
print(os.path.abspath("."))
with open("resources/ingredients-table.txt", "r") as f:
    while True:
        row = {}
        sep = f.readline()
        if sep == None or sep == "":
            break
        if sep != "|-\n":
            raise Exception("Expected new table row, but got: " + sep + "at row number " + str(counter) )
        row["name"] = clean(f.readline())
        row["effects"] = [clean(f.readline()), clean(f.readline()), clean(f.readline()), clean(f.readline())]
        row["weight"] = clean(f.readline())
        row["value"] = clean(f.readline())
        row["obtained"] = clean(f.readline())
        row["rarity"] = ""
        row["owned"] = 0
        ingredients.append(row)
        counter += 1

with open("resources/ingredients.json", "w") as f:
    json.dump(ingredients, f)
