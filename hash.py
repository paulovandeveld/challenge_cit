import hashlib
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

# Creates MD5 hash (ts + privateKey + publicKey)
hash_input = ts + private_key + public_key
hash_result = hashlib.md5(hash_input.encode()).hexdigest()

print(hash_result)  # Hash to be used on Postman to test connection
