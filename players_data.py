from pymongo import MongoClient
import csv

def fetch_data_and_process():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    collection = client['cricket']['cricket_data']

    # Fetch records from MongoDB
    data = collection.find({})

    # Initialize results
    player_records = []

    for match in data:
        date = match.get('info', {}).get('dates', ["Unknown"])[0]
        players = match.get('info', {}).get('players', {})
        player_of_match = match.get('info', {}).get('player_of_match', [])
        player_of_match = [player_of_match] if isinstance(player_of_match, str) else player_of_match

        # Count the number of innings in the match
        number_of_innings = len(match.get('innings', []))

        # Prepare player stats
        stats = {p.strip(): {'runs': 0, 'dot_balls': 0, 'is_pom': 1 if p.strip() in player_of_match else 0}
                 for team in players.values() for p in team}

        # Process deliveries
        for innings in match.get('innings', []):
            for over in innings.get('overs', []):
                for d in over.get('deliveries', []):
                    batter = d.get('batter')
                    bowler = d.get('bowler')
                    runs_batted = d.get('runs', {}).get('batter', 0)  # Use batter runs specifically
                    if batter in stats:
                        stats[batter]['runs'] += runs_batted
                    if bowler in stats and runs_batted == 0:
                        stats[bowler]['dot_balls'] += 1

        # Add records to the result list
        player_records.extend({'Date': date, 'Player': p, 'Total Runs Scored': v['runs'],
                               'Dot Balls as Bowler': v['dot_balls'], 'Player of the Match': v['is_pom'],
                               'Number of Innings': number_of_innings}
                              for p, v in stats.items())

    # Write results to CSV
    with open('player_data_with_innings.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'Date', 'Player', 'Total Runs Scored', 'Dot Balls as Bowler', 'Player of the Match', 'Number of Innings'
        ])
        writer.writeheader()
        writer.writerows(player_records)

    print(f"Data saved to player_data_with_innings.csv. Total records: {len(player_records)}")

# Run the function
fetch_data_and_process()
