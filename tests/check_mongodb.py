"""Script to check MongoDB for users."""

from pymongo import MongoClient

uri = "mongodb+srv://soumalyabanerjee2008_db_user:hX0KIpcUwn4srTIj@cluster0.cftgavz.mongodb.net/sustainability_db"
client = MongoClient(uri)
db = client["sustainability_db"]

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
