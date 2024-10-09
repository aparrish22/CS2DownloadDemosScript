import os
import subprocess
import psycopg2
import requests
import sys
from dotenv import load_dotenv

# Configuration
CS_DM_PATH = '/path/to/csdemo'  # Path to CS Demo Manager CLI
DEMO_SAVE_DIR = 'demos'

# load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

try:
    response = input('Do you want to download demos of a specific team? (Y/N): ').strip().upper()
    if response == 'Y':
        TEAM_NAME = input('Enter the team name (no spaces): ').strip()
        if ' ' in TEAM_NAME:
            raise ValueError('Team name should not contain spaces.')
    elif response == 'N':
        TEAM_NAME = None
    else:
        raise ValueError('Invalid input. Please enter Y or N.')
except ValueError as e:
    print(f"Error: {e}")
    sys.exit()





# Ensure demo directory exists
os.makedirs(DEMO_SAVE_DIR, exist_ok=True)

# Function to download demos using CS Demo Manager CLI
def download_demo(demo_url, save_dir):
    command = [CS_DM_PATH, 'download', '-u', demo_url, '-o', save_dir]
    result = subprocess.run(command, capture_output=True)
    if result.returncode == 0:
        return os.path.join(save_dir, demo_url.split('/')[-1])
    else:
        print(f"Error downloading {demo_url}: {result.stderr}")
        return None

# Function to store demo metadata and file in PostgreSQL
def store_demo_in_db(demo_path, metadata):
    with open(demo_path, 'rb') as file:
        demo_data = file.read()

    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO demos (match_id, date, teams, demo_file)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (match_id) DO NOTHING;
    """, (metadata['match_id'], metadata['date'], metadata['teams'], demo_data))
    conn.commit()
    cur.close()
    conn.close()

# Example function to fetch demo URLs from csconfederation.com (simplified)
def fetch_demo_urls():
    response = requests.get('https://csconfederation.com/api/get_demos')
    demo_data = response.json()
    demo_urls = [demo['url'] for demo in demo_data] # retrieves all demo urls
    return demo_urls

# Main process
demo_urls = fetch_demo_urls()
for demo_url in demo_urls:
    demo_filename = demo_url.split('/')[-1]
    
    # Only download if the filename contains "RowdyRaccoons"
    if TEAM_NAME in demo_filename:
        demo_path = download_demo(demo_url, DEMO_SAVE_DIR)
        # if you want to filter speific demos, feel free to add specifics
        # if demo_path:
        #     metadata = {
        #         'match_id': 'example_id',  # Extract or provide actual match ID
        #         'date': '2024-09-28',      # Provide actual date or extract from metadata
        #         'teams': 'Team A vs Team B' # Provide or extract actual team names
        #     }
        # store_demo_in_db(demo_path, metadata)
        store_demo_in_db(demo_path)
        
sys.exit()