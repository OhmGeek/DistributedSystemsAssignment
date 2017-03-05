"""
    We create a state machine:
      1. INPUT
      2. DISPLAY
      3. EXIT
    These triggers are sent from the server, to display information.
    For example, we send a message called DISPLAY from the server, followed
    by the message.
    We would request the user for information by calling the INPUT function,
    and then followed by a wait for a response.

"""
from enum import Enum


class TransmissionState(Enum):
    INPUT = 1
    DISPLAY = 2
    EXIT = 3
    INIT = 4
