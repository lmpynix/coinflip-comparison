# Streak analyzer: Takes an input of a binary patterned string (e.g. WLLLWLLWLWLWLWLWLW) and interprets the
# length of streaks and the probability those streaks would occur randomly.
import json
from scipy import special

STARTLENGTH = 3  # The length of sequence we start looking at.  There's no point to say they won 2 out of the last 2.
POSITIVEVALUE = "1" # Character we are looking for as being a positive thing.


def streak_analyzer(data: str, quiet: bool) -> list:
    resultlist = list()
    winaccum = int()
    datalength = len(data)
    NMAX = datalength
    for samplelength in range(STARTLENGTH, NMAX):  # For every sample length between the minimum and maximum,
        if not quiet:
            print("New sample length: " + str(samplelength))
        lengthresultlist = []
        for startpt in range(0, datalength - samplelength):  # For every startpoint the length could have,
            if not quiet:
                print("Running start point " + str(startpt) + " of " + str(datalength - samplelength))
            winaccum = 0  # Re-initialize the win accumulator and the score for this particular set of data points.
            score = 0
            for entryind in range(startpt,
                                  startpt + samplelength):  # For every entry inside the sample at this start pt,
                if data[entryind] == POSITIVEVALUE:  # If this particular entry is a good one, increment the win accum.
                    winaccum += 1
            score = 1 / coin_flip_prob(winaccum, samplelength)
            lengthresultlist.append([samplelength, startpt, winaccum, score])
        resultlist.append(lengthresultlist)
    return resultlist


def coin_flip_prob(wins: int, n: int) -> float:
    signum = -1 if wins < n * 0.5 else 1  # Use a signum function to make losing streaks negative.
    return signum * special.binom(n, wins) * 0.5 ** wins * 0.5 ** (n - wins)  # This is the coin flip probability.

if __name__ == "__main__":
    data = streak_analyzer(input("Data string > "))
    with open("streakout.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Results stored in JSON format in streakout.txt")

