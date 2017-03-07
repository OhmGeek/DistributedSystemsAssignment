# DistributedSystemsAssignment
Distributed Systems Assignment using Python3 and Pyro.

## Dependencies:
    + Python 3.5
    + Pyro 4

This might also work with other versions of Python 3, but this hasn't been tested (yet).

## How to run:
To run the client side, simply call

```bash
./client.py
```

You might need to ensure that the file is executable.

Otherwise, just run it directly with Python.

## Running the app once:
For your convenience, I've written a simple BASH script that runs the program. Just call:

```bash
./run.sh 
```

This will start the nameserver, then run the order server, then the frontend, and then create an interactive client.