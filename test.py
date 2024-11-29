from pymongo import MongoClient

def find_incomplete_matches():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cricket']
    collection = db['cricket_data']

    # Fetch all records
    matches = collection.find({})

    # Process data in Python
    incomplete_matches = []

    for match in matches:
        players_set = set()
        date = match['info']['dates'][0] if 'dates' in match['info'] and match['info']['dates'] else "Unknown"
        match_id = match.get('_id', 'No ID')  # Fetch an identifier if available

        # Add players from info.players
        for team, players in match['info']['players'].items():
            players_set.update(players)

        # Add players from deliveries
        for innings in match.get('innings', []):
            for over in innings.get('overs', []):
                for delivery in over.get('deliveries', []):
                    batter = delivery.get('batter')
                    bowler = delivery.get('bowler')
                    if batter:
                        players_set.add(batter)
                    if bowler:
                        players_set.add(bowler)

        # Check if the number of unique players is not 22
        if len(players_set) != 22:
            incomplete_matches.append((date, match_id, len(players_set)))

    # Print out matches that do not have exactly 22 players
    if incomplete_matches:
        print("Matches with player counts not equal to 22:")
        for match in incomplete_matches:
            print(f"Date: {match[0]}, Match ID: {match[1]}, Player Count: {match[2]}")
    else:
        print("All matches have exactly 22 players.")

# Call the function
find_incomplete_matches()
