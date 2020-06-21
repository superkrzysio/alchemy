import logging
import random

from react import get_full_reagent_for, react, pretty_print, effects_to_learn

global database
global database_list

logger = logging.getLogger(__name__)


def is_reactable(r1, r2):
    to_learn = 0
    to_learn += effects_to_learn(r1, r2)
    to_learn += effects_to_learn(r2, r1)
    return to_learn > 0


def calculate(owned):
    raport = {}
    reactions = []
    learned_total = 0
    used_reagents = 0
    reactable = list(owned).copy()
    reactable.sort(key=lambda x: random.random())

    while len(reactable) > 1:
        # step 1: take first
        r1 = random.choice(reactable)
        if r1["owned"] == 0:
            reactable.remove(r1)
            logger.debug("Removing due to out of stock: " + pretty_print(r1) + "\n")
            continue

        r2 = None
        for r2 in reactable:
            if r2["name"] == r1["name"]:
                r2 = None
                continue
            if r2["owned"] == 0:
                r2 = None
                continue
            if is_reactable(r1, r2):
                break
            r2 = None

        if r2 is None:
            reactable.remove(r1)
            logger.debug("Removing due to no more compatible reagents: " + pretty_print(r1) + "\n")
            continue

        # step 3: react them
        logger.debug("Reacting: ")
        logger.debug("r1:      " + pretty_print(r1))
        logger.debug("full r1: " + pretty_print(get_full_reagent_for(r1)))
        logger.debug("r2:      " + pretty_print(r2))
        logger.debug("full r2: " + pretty_print(get_full_reagent_for(r2)))
        logger.debug("Reactables left: " + str(len(reactable)))

        learned_total += react(r1, r2)
        used_reagents += 2
        logger.debug("New r1:  " + pretty_print(r1) + "\n")
        reactions.append((r1["name"], r2["name"]))

    logger.debug("Learned total skills: " + str(learned_total))
    logger.debug("Used reagents: " + str(used_reagents))

    raport["learned_total"] = learned_total
    raport["used_reagents"] = used_reagents
    return raport
