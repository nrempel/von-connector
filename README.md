# VON Connector

Verifiable Organization Network Connector

## Requirements

To run this project locally, you must have an instance of the [VON Network](https://github.com/bcgov/von-network) running.

## Running the VON Connector

First, build the Docker container:

```bash
./manage build
```

Start the VON Connector:

```bash
# Automatically discovers nodes and connects through internal docker network
./manage start
```

```bash
# Specify IP address to connect to remote node pool
./manage start <ip address>
```
