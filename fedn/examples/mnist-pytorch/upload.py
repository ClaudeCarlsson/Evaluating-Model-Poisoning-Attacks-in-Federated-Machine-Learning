from fedn import APIClient
client = APIClient(host="localhost", port=8092)
client.set_package("package.tgz", helper="pytorchhelper")
client.set_initial_model("seed.npz")
