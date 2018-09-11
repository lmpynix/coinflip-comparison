#!/usr/bin/python3

import random
import json
import streakscore.streakscore as ss

randstr = ""
number = int(input("Number of random entries to test > "))
for i in range(number):
    randstr = randstr + random.choice(["0", "1"])


data = ss.streak_analyzer(randstr)
with open("streakout_100k.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
print("Results stored in JSON format in streakout_100k.txt")
