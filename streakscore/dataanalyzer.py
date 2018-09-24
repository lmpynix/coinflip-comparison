import json


def data_analyzer(data_list: list, quiet: bool) -> list:
    """
    Takes in a list of lists of lists spit out by the score generator.
    It then uses a best-so-far system to determine the best streak for each streak length.
    """
    high_scores = []  # List of lists.  Form [[streaklength, score], [...], ...]
    for streaklength_list in data_list:
        highest_score = []  # Best so far variable.
        for streak in streaklength_list:  # Each specific streak.  Form [samplelength, startpt, wins, score].
            if highest_score == [] or streak[3] > highest_score[3]:
                highest_score = streak
        high_scores.append(highest_score)
    # Data accumulated and sorted.  Now we need to export it or print it out in a readable format.
    if not quiet:
        print("Streak Length | Highest Score | Start Position | Wins")
        for highscore_entry in high_scores:
            print("%13d | %13f | %14d | %13d" % (
                highscore_entry[0], highscore_entry[3], highscore_entry[1], highscore_entry[2]))
    return high_scores


if __name__ == "__main__":
    raw_data = []
    with open(input("Raw data file name > "), "r") as infile:
        raw_data = json.load(infile)
    hiscore_data = data_analyzer(raw_data)
    with open(input("Output file name > "), "w") as outfile:
        json.dump(hiscore_data, outfile, indent=4)
        print("Results stored!")
