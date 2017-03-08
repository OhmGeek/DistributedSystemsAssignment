"""
    This is a socket server object that can be called to
    send and receive information. This needs to eventually be
    multithreaded.

    When sending messages, use the Transmission State to deal with
    basic states.
"""

import socketserver

from Part1.frontend import FrontEnd


class SocketPrinter(socketserver.StreamRequestHandler):
    def __init__(self):
        self.frontend = FrontEnd(self.io)

    def handle(self):
        # READ the state and ignore
        pass


def main():
    # todo Implement Socket Server
    pass


if __name__ == "__main__":
    main()
