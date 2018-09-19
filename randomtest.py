#!/usr/bin/python3

import random
import json
import streakscore.streakscore as ss
import streakscore.dataanalyzer as da

randstr = ""
number = int(input("Number of random entries to test > "))
for i in range(number):
    randstr = randstr + random.choice(["0", "1"])

data = ss.streak_analyzer(randstr)
hiscore_data = da.data_analyzer(data)

outfile_name = input("File to save analyzed JSON data to (Will be overwritten!)> ")
with open(outfile_name, "w"):
    json.dump(hiscore_data, outfile_name, indent=4)
    print("Output file successfully written!")
