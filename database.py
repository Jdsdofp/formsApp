
from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://jdsdofp:a3pTtEtXk4iD4G0c@formsapp.qefeoy4.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
except Exception as e:
    print(e)