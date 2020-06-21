import logging

from react import get_full_reagent_for, react, pretty_print, common_effects, effects_to_learn

global database
global database_list

NOT_PROFITABLE = 0
FIRST_WILL_LEARN = 1000
BOTH_WILL_LEARN = 2000
FIRST_WILL_LEARN_2 = 3000
FIRST_WILL_LEARN_2_AND_SECOND_WILL_LEARN = 4000
FIRST_WILL_LEARN_3 = 5000

logger = logging.getLogger(__name__)


def rate_reaction_profitability(r1, r2):
    common = common_effects(r1, r2)
    if r1 == r2 or r1["owned"] == 0 or r2["owned"] == 0 or len(common) == 0:
        return NOT_PROFITABLE
    unlearned_r1 = effects_to_learn(r1, r2)
    unlearned_r2 = effects_to_learn(r2, r1)

    if unlearned_r1 >= 3:
        return FIRST_WILL_LEARN_3

    if unlearned_r1 == 2:
        if unlearned_r2 > 0:
            return FIRST_WILL_LEARN_2_AND_SECOND_WILL_LEARN
        else:
            return FIRST_WILL_LEARN_2
    if unlearned_r1 == 1:
        if unlearned_r2 > 0:
            return BOTH_WILL_LEARN
        else:
            return FIRST_WILL_LEARN
    if unlearned_r1 == 0:
        return NOT_PROFITABLE


def calculate(owned, key="most owned"):
    reactions = []
    learned_total = 0
    used_reagents = 0
    reactable = list(owned).copy()

    while len(reactable) > 1:
        # step 1: find the least/most owned reagent
        reverse = (key == "most owned")
        r1 = sorted(reactable, key=lambda x: x["owned"], reverse=reverse)[0]
        if r1["owned"] == 0:
            reactable.remove(r1)
            logger.debug("Removing due to out of stock: " + pretty_print(r1) + "\n")
            continue

        # step 2: pair it with another owned reagent, which shares the most unknown effects, sorted by number owned desc
        profitabilities = list(map(lambda r2: rate_reaction_profitability(r1, r2), reactable))
        profitabilities = list(zip(reactable, profitabilities))
        profitabilities = list(filter(lambda x: x[1] > NOT_PROFITABLE, profitabilities))

        if len(profitabilities) == 0:
            reactable.remove(r1)
            logger.debug("Removing due to no more reactions: " + pretty_print(r1) + "\n")
            continue

        maxprof = max(profitabilities, key=lambda x: x[1])[1]
        profitabilities = list(filter(lambda x: x[1] == maxprof, profitabilities))

        if len(profitabilities) == 0:
            reactable.remove(r1)
            logger.debug("Removing due to ??? " + pretty_print(r1) + "\n")
            continue

        profitabilities.sort(key=lambda x: x[0]["owned"], reverse=True)
        r2 = profitabilities[0][0]

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

    return (learned_total, used_reagents)
