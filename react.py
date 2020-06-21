import globals


def pretty_print(reagent):
    return "name: " + reagent["name"] + ", " + str(sorted(list(reagent["effects"]))) + ", owned: " + str(
        reagent["owned"])


# extract a set of possible effects from two reagents
def common_effects(r1, r2):
    return set(get_full_reagent_for(r1)["effects"]).intersection(get_full_reagent_for(r2)["effects"])


# number of effects that r1 will learn when reacted
def effects_to_learn(r1, r2):
    common = common_effects(r1, r2)
    l1 = set(r1["effects"]).intersection(common)
    return len(common) - len(l1)


def get_full_reagent_for(reagent):
    return globals.database[reagent.get("name")]


def learn(reagent, effects):
    u = set(reagent["effects"]).union(set(effects))
    learned = len(u) - len(reagent["effects"])
    reagent["effects"] = u
    return learned


def react(reagent1, reagent2):
    if reagent1["owned"] <= 0 or reagent2["owned"] <= 0:
        raise Exception("You do not have the required reagent:\n" + str(reagent1) + "\n" + str(reagent2))

    common = set(get_full_reagent_for(reagent1)["effects"]).intersection(get_full_reagent_for(reagent2)["effects"])
    if len(common) == 0:
        raise Exception("The given reagents do not react:\n" + str(reagent1) + "\n" + str(reagent2))

    learned_something = 0
    learned_something += learn(reagent1, common)
    learned_something += learn(reagent2, common)
    reagent1["owned"] -= 1
    reagent2["owned"] -= 1
    return learned_something
