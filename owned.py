import json
import random

# script #2
# compose a sample json of owned ingredients and their known effects

with open("resources/ingredients.json", "r") as f:
    data = json.load(f)

owned = random.sample(data, k=40)

for o in owned:
    o["owned"] = round(abs(random.gauss(0, 1))*10+1)
    o["effects"] = random.sample(o["effects"], k=random.randint(0,3))

with open("resources/owned.json", "w") as f:
    json.dump(owned, f)