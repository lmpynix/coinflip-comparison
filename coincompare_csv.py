import csv
import sqlite3
import textwrap
import streakscore.streakscore as ss
import streakscore.dataanalyzer as da
import time
import os


def coincompare_csv():
    seasons = []
    analyzed_seasons = []
    teams = []
    infile_text_name = input("CSV file to import > ")
    start_time = time.time()
    with open(infile_text_name, "r") as infile:
        reader = csv.reader(infile)
        for season in reader:
            team = season[0][:3]
            year_str = season[0][3:]
            seasons.append([team, year_str, ''.join(season[1:])])  # The .join madness turns the list into a string.
    # Now that we have the data, we process it season by season.
    for season_entry in seasons:
        raw_data = ss.streak_analyzer(season_entry[2], quiet=True)
        analyzed_data = da.data_analyzer(raw_data, quiet=True)
        analyzed_seasons.append([season_entry[0], season_entry[1], analyzed_data])
        print("Processed season %s%s" % (season_entry[0], season_entry[1]))
    # Now we have a whole bunch of seasons that have a whole bunch of streaks and stuff.  Have we run out of RAM yet?
    # Let's make this an SQLite DB, shall we?
    # First remove the existing database for now.
    try:
        os.remove("coincompare.db")
    except FileNotFoundError:
        print("coincompare.db doesn't exist.  That's okay, just less work for me.")
    db = sqlite3.connect('coincompare.db')
    # Make a list of all of the teams present.
    for analyzed_season in analyzed_seasons:
        if analyzed_season[0] not in teams:
            teams.append(analyzed_season[0])
    # Now we make an SQLite table for teams with their names.
    db.execute(textwrap.dedent("""\
        CREATE TABLE Teams (
            TEAM_ID varchar(6) NOT NULL,
            TeamName varchar(255),
            PRIMARY KEY (TEAM_ID)
        );"""))  # Must use textwrap.dedent otherwise tabs are weird in the command.
    print("")
    # Now we add the teams and prompt for their names.
    for team_id in teams:
        team_name = input("Name for team with ID %s > " % team_id)
        if team_name == "":
            team_name = team_id;
        db.execute("INSERT INTO Teams VALUES (?, ?);", (team_id, team_name))
    # Okay, we have teams.  Now we need seasons.  Let's start with a table.
    db.execute(textwrap.dedent("""\
            CREATE TABLE TeamsSeasons (
                TEAM_SEASON varchar(16) NOT NULL,
                TEAM_ID varchar(6) NOT NULL,
                YEAR int,
                PRIMARY KEY (TEAM_SEASON)
            );"""))
    # While we're making tables, let's make ones for the individual streaks, which we'll need eventually.
    db.execute(textwrap.dedent("""\
                CREATE TABLE Streaks (
                    STREAK_ID INTEGER PRIMARY KEY,
                    TEAM_SEASON varchar(16) NOT NULL,
                    N int,
                    WINS int,
                    SCORE decimal,
                    START_POINT int
                );"""))
    # Now we go through each season and add it to the table.
    for analyzed_season in analyzed_seasons:
        data_tuple = (analyzed_season[0] + analyzed_season[1], analyzed_season[0], analyzed_season[1])
        db.execute("INSERT INTO TeamsSeasons VALUES (?, ?, ?);", data_tuple)
        # Finally, and this is the fun one, we add each winning streak to a table with its corresponding team's season.
        for streak in analyzed_season[2]:  # analyzed_season[2] is each best streak for a length.
            streak_data_tuple = (analyzed_season[0] + analyzed_season[1], streak[0], streak[2], streak[3], streak[1])
            db.execute("INSERT INTO Streaks (TEAM_SEASON, N, WINS, SCORE, START_POINT) VALUES (?, ?, ?, ?, ?);",
                       streak_data_tuple)
    # We should be done now.  Commit our changes, close things, and wrap up.
    db.commit()
    db.close()
    end_time = time.time()
    delta_time = end_time - start_time
    print("Done!  %fs elapsed." % delta_time)

    return 0


if __name__ == "__main__":
    coincompare_csv()
