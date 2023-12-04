from fedn import APIClient
import yaml

# Initialize the APIClient
client = APIClient(host="localhost", port=8092)

# Get the client configuration
client_yaml_content = client.get_client_config(checksum=True)

# Convert the dictionary to a YAML-formatted string
yaml_content = yaml.dump(client_yaml_content)

# File name
file_name = 'client.yaml'

# Write the YAML content to the file in the same directory as the script
with open(file_name, 'w') as file:
    file.write(yaml_content)
