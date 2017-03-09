# DistributedSystemsAssignment
Distributed Systems Assignment using Python3 and Pyro.

## Dependencies:
    + Python 3.5
    + Pyro 4

This might also work with other versions of Python 3, but this hasn't been tested (yet).

## Different Programs
The Part1 folder contains the working system, without any failover in the event the primary server falls over.

The Part2 folder contains the system working with failover, so that the backup servers become primary if the old primary
server goes offline.

## How to run:
### 1. Starting the Name Server
Navigate to the folder containing the system you want to run.

First, you will need to start the Pyro nameserver. In most cases, this can be done quickly using the alias:

```bash
pyro4-ns
```

### 2. Starting the Order Servers 
Then, start three order servers. Each server needs to be given a different ID, from the set of {1,2,3}, such as:

```bash
python3 order_server.py 1
```

For your convenience, I've also created a BASH script that automatically starts three servers, although for proper testing
purposes it's advisable to create three separate terminals with three different servers, to see what the server output is.

### 3. Start the FrontEnd
Two arguments are needed to start the frontend. The first is the hostname, which for testing purposes is 'localhost', 
as well as the port number. For example:

```bash
python3 frontend.py localhost 3000
```

Ensure you remember the hostname and port number, as these are needed for step 4...

### 4. Starting the Client

Starting the client also takes the hostname and port number as parameters. You can start a single client using the command:


```bash
python3 client.py localhost 3000
```

The hostname and port should be the same as those used for the frontend.