import json
import random

# script #2
# compose a random list of owned ingredients and their known effects - this should be composed by
# the player manually or with GUI or some export from skyrim

with open("resources/ingredients.json", "r") as f:
    data = json.load(f)

owned = random.sample(data, k=100)

for o in owned:
    o["owned"] = round(abs(random.gauss(0, 1)) * 10 + 1)
    o["effects"] = random.sample(o["effects"], k=random.randint(0, 3))

with open("resources/owned.json", "w") as f:
    json.dump(owned, f)
