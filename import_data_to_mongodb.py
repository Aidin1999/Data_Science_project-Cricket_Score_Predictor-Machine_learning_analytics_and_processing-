import zipfile
import json
from pymongo import MongoClient


# MongoDB setup
client = MongoClient('*****')
db = client['cricket']
collection = db['cricket_data']

# Function to process JSON files directly from ZIP
def process_zip(zip_path):
    # Open the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # List all files in the ZIP
        for file_name in zip_ref.namelist():
            # Filter only JSON files
            if file_name.endswith('.json'):
                # Read the file contents as bytes, then convert to a string
                with zip_ref.open(file_name) as file:
                    file_data = file.read()
                    # Load JSON data from string
                    data = json.loads(file_data.decode('utf-8'))
                    # Insert data into MongoDB
                    collection.insert_one(data)
                    print(f"Processed {file_name}")  #  Output to track which files have been processed

# Path to the ZIP file
zip_path = 'all_json.zip'

# Call the function
process_zip(zip_path)
