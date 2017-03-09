#!/usr/bin/python3
""" User Client """
import json
import socketserver
import sys
import threading

import Pyro4

# TODO: avoid reverting the first back to primary (add a queue of servers essentially).

from Pyro4.errors import CommunicationError, PyroError


class FrontEnd(object):
    def __init__(self):
        self.__update_server_lists()

    def __get_list_of_server_uris(self):
        ns = Pyro4.locateNS()
        self.server_uris = []
        ids = ["OrderManager1", "OrderManager2", "OrderManager3"]
        for id in ids:
            try:
                uri = ns.lookup(id)
                self.server_uris.append(uri)
            except ConnectionRefusedError:
                pass
            except CommunicationError:
                pass
            except PyroError:
                pass

    def __get_order_server(self):
        primary_server = True
        actual_server = None
        for server in self.server_uris:
            try:
                s = Pyro4.Proxy(server)
                s.set_primary_state(primary_server)
                primary_server = False
                if actual_server is None and s.is_working():
                    actual_server = s

            except ConnectionRefusedError:
                pass
            except CommunicationError:
                pass
            except PyroError:
                pass
            except:
                pass

        print("Current Server: \n", str(actual_server))
        return actual_server

    def __update_server_lists(self):
        self.__get_list_of_server_uris()
        serverlist = []
        for uri in self.server_uris:
            try:
                s = Pyro4.Proxy(uri)
                serverlist.append(Pyro4.Proxy(uri))
            except:
                pass

        # update server lists
        for s in serverlist:
            try:
                s.set_servers(self.server_uris)
            except PyroError:
                pass  # ignore the error

        print(self.server_uris)

    def process_command(self, data):
        print("Frontend data: ", data)
        command = data['action']
        userid = data['userid']
        input = data['data']
        out_error = ""
        if not userid:
            return "No USERID specified"

        if command == "ADD":
            print("Running Action Frontend")
            items_to_order = input.split(',')
            if len(items_to_order) > 3 or len(items_to_order) == 0:
                return "Must enter at least 1 item, and no more than 3."
            # deal with batch stuff, to
            results = self.__get_order_server().place_order(userid, items_to_order)

            # todo check length to make sure a server is online.
            return str(results)

        elif command == "DELETE":
            print("running delete front end")
            del_index = input
            results = self.__get_order_server().cancel_order(userid, del_index)

            # todo check results to ensure things are fine :D
            return str(results)

        elif command == "HISTORY":
            print("Running History frontend")
            results = self.__get_order_server().get_order_history(userid)
            print("Frontend results: ", results)
            # todo remove batch processing for this (no CUD needed, only R).
            return str(results)

        else:
            out_error = "Command not found. Please try again"
        self.__update_server_lists()
        return out_error


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
