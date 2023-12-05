import argparse
from pymongo import MongoClient
import json
from bson import ObjectId
import time

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Setting up argument parser
parser = argparse.ArgumentParser(description='MongoDB Data Exporter')
parser.add_argument('output_file', help='Full path of the output file', type=str)
parser.add_argument('n_documents', help='Desired number of documents to fetch', type=int)
args = parser.parse_args()

# MongoDB connection with authentication
client2 = MongoClient("mongodb://fedn_admin:password@localhost:6534")
db = client2['fedn-network']
collection = db['control.validations']

# Fetching documents
fetched_count = 0
data = []
while fetched_count < args.n_documents:
    documents = collection.find().limit(args.n_documents - fetched_count)
    new_docs = [doc for doc in documents]
    data.extend(new_docs)
    fetched_count += len(new_docs)
    
    # Check if the desired number of documents is reached
    if fetched_count < args.n_documents:
        time.sleep(2)  # Wait for 2 seconds before trying again

# Saving the data to the specified output file
with open(args.output_file, 'w') as file:
    json.dump(data, file, cls=JSONEncoder, indent=4)

print(f"Data has been saved to {args.output_file}")
