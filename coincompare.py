import json
import streakscore.streakscore as ss
import streakscore.dataanalyzer as da


def coincompare():
    # Get a filename and read in the first line.
    infile_text_name = input("Raw text file to input.  Should be ASCII characters 0 and 1 only. > ")
    with open(infile_text_name, "r") as infile:
        input_string = infile.readline()[:-1]  # str.readline() puts '\n' at the end but we don't want that.
        print("File read successfully")
    raw_data = ss.streak_analyzer(input_string)
    save_intermediate = input("Press ENTER to continue or input a filename to save raw data > ")
    if save_intermediate != "":
        with open(save_intermediate, "w") as intfile:
            json.dump(raw_data, intfile)
    analyzed_data = da.data_analyzer(raw_data)
    save_final = input("Done!  Press ENTER to quit or input a filename to save analyzed data > ")
    if save_final != "":
        with open(save_final, "w") as finalfile:
            json.dump(analyzed_data, finalfile)

if __name__ == "__main__":
    coincompare()
