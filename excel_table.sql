create table TeamsStreaks as 
SELECT Streaks.STREAK_ID, TeamsSeasons.TEAM_SEASON, TeamsSeasons.YEAR, Streaks.N, Streaks.WINS, Streaks.SCORE, Streaks.START_POINT
FROM Streaks
LEFT JOIN TeamsSeasons ON Streaks.TEAM_SEASON = TeamsSeasons.TEAM_SEASON
ORDER BY Streaks.STREAK_ID;