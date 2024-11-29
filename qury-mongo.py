import csv
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['cricket']
collection = db['cricket_data']

# MongoDB aggregation query
query = [
    {
        "$project": {
            "Date": { "$arrayElemAt": ["$info.dates", 0] },
            "teamA": { "$arrayElemAt": ["$info.teams", 0] },
            "teamB": { "$arrayElemAt": ["$info.teams", 1] },
            "gender": "$info.gender",
            "type": "$info.match_type",
            "winner": "$info.outcome.winner",
            "players": "$info.players",
            "scores": {
                "$arrayToObject": {
                    "$map": {
                        "input": "$info.teams",  # Iterate over teams
                        "as": "team",
                        "in": {
                            "k": "$$team",  # Use team name as key
                            "v": {
                                "$sum": {
                                    "$map": {
                                        "input": {
                                            "$filter": {
                                                "input": "$innings",
                                                "as": "inning",
                                                "cond": { "$eq": ["$$inning.team", "$$team"] }
                                            }
                                        },
                                        "as": "inning",
                                        "in": {
                                            "$reduce": {
                                                "input": "$$inning.overs",
                                                "initialValue": 0,
                                                "in": {
                                                    "$add": ["$$value", {
                                                        "$reduce": {
                                                            "input": "$$this.deliveries",
                                                            "initialValue": 0,
                                                            "in": { "$add": ["$$value", "$$this.runs.total"] }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
]


# Execute the query
results = collection.aggregate(query)

# Open a CSV file for writing
with open("match.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow([
        "Date", "Score Team A", "Score Team B", "Team A", "Team B", "Gender", "Type", "Winner",
        "Player 1 Team A", "Player 2 Team A", "Player 3 Team A", "Player 4 Team A", "Player 5 Team A", "Player 6 Team A", "Player 7 Team A", "Player 8 Team A", "Player 9 Team A", "Player 10 Team A", "Player 11 Team A",
        "Player 1 Team B", "Player 2 Team B", "Player 3 Team B", "Player 4 Team B", "Player 5 Team B", "Player 6 Team B", "Player 7 Team B", "Player 8 Team B", "Player 9 Team B", "Player 10 Team B", "Player 11 Team B"
    ])
    
    # Process the results
    for result in results:
        # Extract fields from the result
        date = result.get("Date")
        teamA = result.get("teamA")
        teamB = result.get("teamB")
        gender = result.get("gender")
        match_type = result.get("type")
        winner = result.get("winner")
        players = result.get("players", {})
        scores = result.get("scores", {})

        # Get scores from the scores dictionary
        score_teamA = scores.get(teamA, 0)
        score_teamB = scores.get(teamB, 0)

        # Dynamically extract players for teamA and teamB
        players_teamA = players.get(teamA, [])
        players_teamB = players.get(teamB, [])

        # Ensure up to 11 players for each team
        players_teamA += ['no-name'] * (11 - len(players_teamA))  # Pad with 'no-name' if less than 11 players
        players_teamB += ['no-name'] * (11 - len(players_teamB))

        # Write the row to the CSV
        writer.writerow([
            date, score_teamA, score_teamB, teamA, teamB, gender, match_type, winner,
            *players_teamA[:11],  # First 11 players for Team A
            *players_teamB[:11]   # First 11 players for Team B
        ])

print("Data saved to match.csv")
