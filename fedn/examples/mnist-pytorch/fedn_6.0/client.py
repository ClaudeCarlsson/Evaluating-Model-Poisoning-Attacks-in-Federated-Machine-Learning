import yaml
from fedn import APIClient
client = APIClient(host="localhost", port=8092)
config = client.get_client_config(checksum=True)
with open("client.yaml", "w") as f:
   f.write(yaml.dump(config))
