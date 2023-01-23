import sqlite3 as lite
import random

firstNames = ["John", "James", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas", "Christopher", "Daniel", "Paul", "Mark","Donald","George","Kenneth","Steven","Edward","Brian","Ronald","Anthony","Kevin","Jason","Matthew","Gary","Timothy","Jose","Larry"]

lastNames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia","Martinez","Robinson","Clark","Rodriguez","Lewis","Lee","Walker","Hall","Allen","Young","Hernandez","King","Wright"]

conn = lite.connect('database.db')

playerCursor = conn.cursor()
gameCursor = conn.cursor()



#Create a table called players if it does not exist
playerCursor.execute("""CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, offense INTEGER, defense INTEGER)""")
gameCursor.execute("""CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, score1 INTEGER, score2 INTEGER, winner TEXT)""")
#Using sqlite, add 10 rows to the table "players". For id, simply number them 0 to 9. For name, use a combination of one random first name and one random last name. For offense and defense, generate a random integer between 40 and 99.
#Use sqlite to insert or update if the row already exists

gameCursor.execute("INSERT INTO games (id, score1, score2, winner) VALUES (?, ?, ?, ?)", (0, 0, 0, "Neither"))

for i in range(10):
    first_name = random.choice(firstNames)
    last_name = random.choice(lastNames)
    offense = random.randint(40,99)
    defense = random.randint(40,99)

    playerCursor.execute("INSERT OR REPLACE INTO players VALUES (?,?,?,?)", (i, first_name + " " + last_name, offense, defense))


#Print the first ten rows of the players database using sqlite
playerCursor.execute("SELECT * FROM players LIMIT 10")
rows = playerCursor.fetchall()
i = 0
team1Printed = False
team2Printed = False
team1OffenseRatings = []
team1DefenseRatings = []
team2OffenseRatings = []
team2DefenseRatings = []

for row in rows:
    if i < 5:
        if team1Printed is False:
            print("Team 1")
            team1Printed = True
        print(row[1])
        team1OffenseRatings.append(row[2])
        team1DefenseRatings.append(row[3])
    else:
        if team2Printed is False:
            print()
            print("Team 2")
            team2Printed = True
        print(row[1])
        team2OffenseRatings.append(row[2])
        team2DefenseRatings.append(row[3])
    i += 1

#take the average of an array

def averageValue(arr):
    total = 0
    for val in range(0,len(arr)):
        total += arr[val]
    average = total / len(arr)
    return average

team1OffenseAverage = int(averageValue(team1OffenseRatings))
team1DefenseAverage = int(averageValue(team1DefenseRatings))
team2OffenseAverage = int(averageValue(team2OffenseRatings))
team2DefenseAverage = int(averageValue(team2DefenseRatings))

team1Score = team1OffenseAverage - team2DefenseAverage + 65
team2Score = team2OffenseAverage - team1DefenseAverage + 65

if team1Score == team2Score:
    team1Score += 1

#Convert int to string

print("Score: " + str(team1Score) + " - " + str(team2Score))
gameCursor.execute("SELECT MAX(id) FROM games")
maxID = gameCursor.fetchone()[0]
next_id = maxID + 1
#Insert values into table games. Insert into next available row. Insert team1Score for score1. Insert team2Score for score2. Insert id that is greater than highest ID in table already. If team1Score is greater, insert "Team 1" for winner, else insert "Team 2".

gameCursor.execute("INSERT INTO games (id, score1, score2, winner) VALUES (?, ?, ?, ?)", (next_id, team1Score, team2Score, "Team 1" if team1Score > team2Score else "Team 2"))
conn.commit()

conn.close()

