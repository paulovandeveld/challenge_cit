import requests
import hashlib
import pandas as pd
from tabulate import tabulate
import os
from dotenv import load_dotenv

# Finds and loads .env file with API Keys for security
env_path = os.path.join(os.path.dirname(__file__), 'keys.env')
load_dotenv(env_path)

# Defines timestamp
ts = '1'

# Retrieves API keys from environment
public_key = os.getenv('MARVEL_PUBLIC_KEY')
private_key = os.getenv('MARVEL_PRIVATE_KEY')

if public_key is None or private_key is None:
    raise ValueError("API Keys not found! Check your .env file or environment variables.")

# Generates MD5 hash from hashlib
hash_input = ts + private_key + public_key
hash_result = hashlib.md5(hash_input.encode()).hexdigest()

# Generates url and parameters
url = 'https://gateway.marvel.com/v1/public/characters'

# Pagination settings
limit = 100  # Max number of characters per request
offset = 0   # Start at the first character
all_characters = []  # List to save all characters

# Loop through the API responses 
while True:

    # Parameters 
    params = {
        'ts': ts,
        'apikey': public_key,
        'hash': hash_result,
        'limit': limit,
        'offset': offset
    }

    # GET request
    response = requests.get(url, params=params)

    # Check if request is successful and extracts the data
    if response.status_code == 200:
        data = response.json()
        characters = data['data']['results']
        
        # Add the characters from current page to the list 
        all_characters.extend(characters)
        
        # Check if the while condition continues
        total_characters = data['data']['total']
        print("Loaded", offset+100, "Marvel Heroes from a total of", total_characters)
        offset += limit
        if offset >= total_characters:
            break    

    else: #Prints the status from API if error triggered
        print(f"Error: {response.status_code}")
        break

# Convert the list of all characters to a DataFrame
df = pd.DataFrame(all_characters, columns=['id', 'name', 'description', 'comics', 'series', 'stories', 'events'])

# Show only 50 characters of description
df['description'] = df['description'].apply(lambda x: (x[:50] + '...') if len(x) > 50 else x)

'''
    # Every character info
    for index, row in df.iterrows():
        print(f"ID: {row['id']}")
        print(f"Name: {row['name']}")
        print(f"Description: {row['description']}")
        print(f"Comics Available: {row['comics']['available']}")
        print(f"Series Available: {row['series']['available']}")
        print(f"Stories Available: {row['stories']['available']}")
        print(f"Events Available: {row['events']['available']}")
        print("-" * 50)  
'''

# Tabulate the matrix of characters
df_matrix = df[['id', 'name', 'description', 'comics', 'series', 'stories', 'events']].copy()
df_matrix['comics'] = df_matrix['comics'].apply(lambda x: x['available'])
df_matrix['series'] = df_matrix['series'].apply(lambda x: x['available'])
df_matrix['stories'] = df_matrix['stories'].apply(lambda x: x['available'])
df_matrix['events'] = df_matrix['events'].apply(lambda x: x['available'])

# Selects some records from head and tail to tabulate
df_subset = pd.concat([df_matrix.head(13), df_matrix.tail(13)])
    
print("\nMarvel Super Heroes:\n")
print(tabulate(df_subset, headers='keys', tablefmt='fancy_grid'))
    
