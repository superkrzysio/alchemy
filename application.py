import json
import logging

import calculation.num_owned
import calculation.random
import globals


# script #3 - the actual calculator

### functions ###

def log_report(desc, used, learned):
    logger.info(desc)
    logger.info("Used: " + str(used))
    logger.info("Learned: " + str(learned))


def calculate_random():
    reports = []
    for i in range(1, 100):
        with open("resources/owned.json", "r") as f:
            owned = json.load(f)
        reports.append(calculation.random.calculate(owned))

    for r in reports:
        logger.debug(r)

    min_used = min(reports, key=lambda x: x["used_reagents"])
    max_learned = max(reports, key=lambda x: x["learned_total"])

    log_report("Calculating with random method - min used:", min_used["used_reagents"], min_used["learned_total"])
    log_report("Calculating with random method - max learned:", max_learned["used_reagents"],
               max_learned["learned_total"])


def calculate_most_owned():
    with open("resources/owned.json", "r") as f:
        owned = json.load(f)
    (used, learned) = calculation.num_owned.calculate(owned)

    log_report("Calculating with most owned priority", used, learned)


def calculate_least_owned():
    with open("resources/owned.json", "r") as f:
        owned = json.load(f)
    (used, learned) = calculation.num_owned.calculate(owned, "least owned")

    log_report("Calculating with least owned priority", used, learned)


### script ###

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

with open("resources/ingredients.json", "r") as f:
    globals.database_list = json.load(f)
    globals.database = dict((a["name"], a) for a in globals.database_list)

calculate_random()
calculate_least_owned()
calculate_most_owned()
