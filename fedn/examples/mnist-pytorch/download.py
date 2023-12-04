import argparse
from pymongo import MongoClient
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Setting up argument parser
parser = argparse.ArgumentParser(description='MongoDB Data Exporter')
parser.add_argument('output_file', help='Full path of the output file', type=str)
args = parser.parse_args()

# MongoDB connection with authentication
client2 = MongoClient("mongodb://fedn_admin:password@localhost:6534")
db = client2['fedn-network']
collection = db['control.validations']

# Fetching documents
documents = collection.find()
data = [doc for doc in documents]

# Saving the data to the specified output file
with open(args.output_file, 'w') as file:
    json.dump(data, file, cls=JSONEncoder, indent=4)

print(f"Data has been saved to {args.output_file}")
