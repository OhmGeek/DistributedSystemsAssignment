"""
    This is the client program.
    It uses sockets to communicate with the server. This is essentially a Thin Client,
    and all functionality is provided on the front end of our system.

"""

import socket
from transmission_state import TransmissionState

HOST = "localhost"
PORT = 3000


