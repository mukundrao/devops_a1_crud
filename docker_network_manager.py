import docker
import sys

def list_networks(client):
    """List all Docker networks."""
    networks = client.networks.list()
    print("Listing all Docker networks:\n")
    for network in networks:
        print(f"Network: {network.name}, ID: {network.id}, Driver: {network.attrs['Driver']}")

def inspect_network(client, network_name):
    """Inspect a Docker network and display details."""
    try:
        network = client.networks.get(network_name)
        print(f"\nInspecting network '{network_name}':\n")
        print(f"Network ID: {network.id}")
        print(f"Driver: {network.attrs['Driver']}")
        print("Containers connected to this network:")
        for container_id, container_info in network.attrs['Containers'].items():
            print(f"  - Container ID: {container_id}, Name: {container_info['Name']}")
    except docker.errors.NotFound:
        print(f"Network '{network_name}' not found.")

def ensure_container_communication(client, network_name, container_name):
    """Ensure a container is connected to the given network."""
    try:
        network = client.networks.get(network_name)
        container = client.containers.get(container_name)
        
        # Check if the container is connected to the network
        if container.id in network.attrs['Containers']:
            print(f"Container '{container_name}' is connected to network '{network_name}'.")
        else:
            print(f"Container '{container_name}' is NOT connected to network '{network_name}'.")
            # Optionally, you could connect the container to the network:
            # network.connect(container)
            # print(f"Connected container '{container_name}' to network '{network_name}'.")
    except docker.errors.NotFound:
        print(f"Either network '{network_name}' or container '{container_name}' not found.")
    
def list_containers(client):
    """List all running containers."""
    containers = client.containers.list()
    print("\nListing all running containers:\n")
    for container in containers:
        print(f"Container: {container.name}, ID: {container.id}, Status: {container.status}")

def main():
    client = docker.from_env()

    while True:
        print("\nDocker Network Manager")
        print("1. List Docker Networks")
        print("2. Inspect a Docker Network")
        print("3. Ensure Container Communication")
        print("4. List Running Containers")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_networks(client)
        elif choice == '2':
            network_name = input("Enter the network name to inspect: ")
            inspect_network(client, network_name)
        elif choice == '3':
            network_name = input("Enter the network name: ")
            container_name = input("Enter the container name: ")
            ensure_container_communication(client, network_name, container_name)
        elif choice == '4':
            list_containers(client)
        elif choice == '5':
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
