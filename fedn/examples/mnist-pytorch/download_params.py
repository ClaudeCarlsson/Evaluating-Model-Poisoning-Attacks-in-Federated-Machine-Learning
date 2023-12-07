import argparse
import boto3
from botocore.client import Config
import os

# Setting up argument parser
parser = argparse.ArgumentParser(description='MinIO Object Downloader')
parser.add_argument('path', help='Path to save the downloaded file (including file name)', type=str)
args = parser.parse_args()

# Extract directory and file name from the path
output_dir, output_file_name = os.path.split(args.path)

# MinIO/S3 client configuration
s3_client = boto3.client('s3',
                         endpoint_url='http://localhost:9000',  # Adjust this to the correct API port
                         aws_access_key_id='fedn_admin',
                         aws_secret_access_key='password',
                         config=Config(signature_version='s3v4'))

# List objects in the fedn-models bucket
try:
    objects = s3_client.list_objects_v2(Bucket='fedn-models')['Contents']
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# Find the latest object
latest_object = max(objects, key=lambda x: x['LastModified'])

# Check if the output directory exists, create if not
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Constructing the output file path
output_file_path = os.path.join(output_dir, output_file_name)

# Downloading the latest object
s3_client.download_file('fedn-models', latest_object['Key'], output_file_path)

print(f"Latest object {latest_object['Key']} has been downloaded and saved as {output_file_path}")
