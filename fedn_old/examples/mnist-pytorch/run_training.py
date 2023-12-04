import argparse
import time
from fedn import APIClient

def main(n_clients):
    client = APIClient(host="localhost", port=8092)
    client.start_session(session_id="session_training", rounds=args.rounds)

    while client.get_controller_status()["state"] != 'idle':
        time.sleep(3)
        print("Still training...")

    print("Training session completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a session with a specified number of rounds and clients.")
    parser.add_argument("--rounds", type=int, required=True, help="Number of rounds for the session")
    parser.add_argument("--n_clients", type=int, required=True, help="Number of clients to wait for")
    args = parser.parse_args()

    client = APIClient(host="localhost", port=8092)
    time.sleep(2)
    while client.list_clients()["count"] != args.n_clients:
        time.sleep(1)
        print("Waiting for clients to be ready")
        print("Number of clients connected: " + str(client.list_clients()["count"]))
        print("Number of expected clients: " + str(args.n_clients))
    main(args.n_clients)
