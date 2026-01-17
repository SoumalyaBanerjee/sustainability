"""Script to check MongoDB for users."""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

uri = os.getenv('MONGODB_URI')
if not uri:
    print("❌ Error: MONGODB_URI not found in .env file")
    exit(1)

client = MongoClient(uri)
db_name = os.getenv('MONGODB_DB_NAME', 'sustainability_db')
db = client[db_name]

print("\n" + "="*50)
print("MongoDB User Check")
print("="*50 + "\n")

count = db.users.count_documents({})
print(f"Total users in database: {count}\n")

if count > 0:
    print("Users found:\n")
    for user in db.users.find():
        print(f"✓ Email: {user['email']}")
        print(f"  ID: {user['_id']}")
        print(f"  Active: {user.get('is_active')}")
        print(f"  Created: {user.get('created_at')}")
        print()
else:
    print("No users found in database.")

print("="*50 + "\n")

client.close()
print("Connection closed.")
