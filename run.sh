#!/usr/bin/env bash
python3 -m Pyro4.naming &
python3 order_server.py &
python3 frontend.py localhost 3001 &
python3 client.py localhost 3001