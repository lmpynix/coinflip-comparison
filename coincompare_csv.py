import csv
import sqlite3
import textwrap
import streakscore.streakscore as ss
import streakscore.dataanalyzer as da


def coincompare_csv():
    seasons = []
    analyzed_seasons = []
    teams = []
    infile_text_name = input("CSV file to import > ")
    with open(infile_text_name, "rb") as infile:
        reader = csv.reader(infile)
        for season in reader:
            team = season[0][:3]
            year_str = season[0][3:]
            seasons.append([team, year_str, ''.join(season[1:])])  # The .join madness turns the list into a string.
    # Now that we have the data, we process it season by season.
    for season_entry in seasons:
        raw_data = ss.streak_analyzer(season_entry[2])
        analyzed_data = da.data_analyzer(raw_data)
        analyzed_seasons.append([season_entry[0], season_entry[1], analyzed_data])
    # Now we have a whole bunch of seasons that have a whole bunch of streaks and stuff.  Have we run out of RAM yet?
    # Let's make this an SQLite DB, shall we?
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
    # Now we add the teams and prompt for their names.
    for team_id in teams:
        team_name = input("Name for team with ID %s" % team_id)
        if team_name != "":
            db.execute("INSERT INTO Teams VALUES (?, ?)", (team_id, team_name))
    # Okay, we have teams.  Now we need seasons.  Let's start with a table.
    db.execute(textwrap.dedent("""\
            CREATE TABLE TeamsSeasons (
                TEAM_SEASON varchar(16) NOT NULL,
                TEAM_ID varchar(6) NOT NULL,
                YEAR int,
                PRIMARY KEY (TEAM_SEASON)
            );"""))
    # Now we go through each season and add it to the table.
    for analyzed_season in analyzed_seasons:
        db.execute("INSERT INTO TeamsSeasons VALUES (?, ?, ?)", ())
