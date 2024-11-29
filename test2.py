import json

def sum_runs_by_batter(file_path, batter_name):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    total_runs = 0
    
    # Navigate through the innings and deliveries
    for innings in data.get('innings', []):
        for over in innings.get('overs', []):
            for delivery in over.get('deliveries', []):
                if delivery.get('batter') == batter_name:
                    total_runs += delivery.get('runs', {}).get('batter', 0)
    
    return total_runs

# Usage
file_path = 'cricket.cricket_data.json'  # Replace with your JSON file path
batter_name = "SA Northeast"
total_runs = sum_runs_by_batter(file_path, batter_name)
print(f"Total runs scored by {batter_name}: {total_runs}")
