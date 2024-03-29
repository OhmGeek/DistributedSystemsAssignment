#!/usr/bin/python3
""" User Client """
import json
import socketserver
import sys

import Pyro4


# TODO: work out what is throwing errors
# TODO: get server polling code to change server status if there is an outage.

class FrontEnd(object):
    def __init__(self):
        ns = Pyro4.locateNS()
        self.server_uris = [ns.lookup("OrderManager1"), ns.lookup("OrderManager2"), ns.lookup("OrderManager3")]
        self.serverlist = []
        for uri in self.server_uris:
            self.serverlist.append(Pyro4.Proxy(uri))

        self.server = self.serverlist[0]
        self.server.set_primary_state(True)
        # update server lists
        for s in self.serverlist:
            s.set_servers(self.server_uris)
        print(self.server_uris)

    def process_command(self, data):
        print("Frontend data: ", data)
        command = data['action']
        userid = data['userid']
        input = data['data']
        if not userid:
            return "No USERID specified"

        if command == "ADD":
            print("Running Action Frontend")
            items_to_order = input.split(',')
            if len(items_to_order) > 3 or len(items_to_order) == 0:
                return "Must enter at least 1 item, and no more than 3."
            # deal with batch stuff, to
            results = self.server.place_order(userid, items_to_order)

            # todo check length to make sure a server is online.
            return str(results)

        elif command == "DELETE":
            print("running delete front end")
            del_index = input
            results = self.server.cancel_order(userid, del_index)

            # todo check results to ensure things are fine :D
            return str(results)

        elif command == "HISTORY":
            print("Running History frontend")
            results = self.server.get_order_history(userid)
            print("Frontend results: ", results)
            # todo remove batch processing for this (no CUD needed, only R).
            return str(results)

        else:
            return "Command not found. Please try again"


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        server = FrontEnd()
        data = self.request.recv(1024).strip()
        data = data.decode()

        data_dict = json.loads(data)
        res = server.process_command(data_dict)
        # server log now
        print("Frontend: ", res)
        response = res.encode()
        print("Frontend encoded: ", response)
        self.request.sendall(response)


def main(host, port):
    # for i in range(1, 4):
    #     t = threading.Thread(target=order_server.main, args=[i])
    #     t.daemon = True
    #     t.start()
    server = socketserver.TCPServer((host, port), MyServer)
    server.serve_forever()


if __name__ == "__main__":
    print("Arguments frontend: ", sys.argv)
    hostname = sys.argv[1]
    portnum = int(sys.argv[2])
    main(hostname, portnum)
