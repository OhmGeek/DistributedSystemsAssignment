#!/usr/bin/python3
""" User Client """
import random
import string
import Pyro4
import socket
import sys
import json

HOST = "localhost"
PORT = 3000


class Client(object):
    """ This is the Client Controller, allowing possible actions to be executed """

    def __init__(self):
        self.userid = self.__gen_user_id()
        # now connect to the server

    def __gen_user_id(self):
        """ Generate user ID """
        my_ID = ""
        for i in range(1, 20):
            my_ID += random.choice(string.ascii_uppercase)
        return my_ID

    def print_options(self):
        """ Print the options of the client program """
        print("\n\nBeadle's Shop")
        print("-----------------------")
        print("Options:")
        print("     1  -   Create Order")
        print("     2  -   Get Order History")
        print("     3  -   Delete Order")

    def create_order(self):
        """ Allows the user to create an order """
        input_str = input("Item List: ")
        resp = make_request("ADD", input_str, self.userid)
        print(resp)

    def get_order_history(self):
        resp = make_request("HISTORY", "", self.userid)
        print("#### ORDER HISTORY ####")
        print(resp)

    def delete_order(self):
        print("#### DELETE ORDER ####")
        print()
        print("Please insert the order number to delete (from the order history)")
        orderid = input()
        resp = make_request("DELETE", orderid, self.userid)
        print(resp)


def control_manager(program, opt):
    """ Manages flow of control based on the option input """
    if opt == "1":
        program.create_order()
    elif opt == "2":
        program.get_order_history()
    elif opt == "3":
        program.delete_order()
    elif opt == "q":
        print("Bye!")
    else:
        print("Invalid option. Try again")


def main():
    exit_status = False
    prog = Client()
    while not exit_status:
        prog.print_options()
        option = input("Select option: ")
        control_manager(prog, option)

        # listen for the exit command
        if option == "q":
            exit_status = True


def make_request(action, data, userid):
    data_to_send = {'action': action, 'data': data, 'userid': userid}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_json_encoded = json.dumps(data_to_send)

    try:
        sock.connect((HOST, PORT))
        sock.sendall(data_json_encoded.encode())
        received = sock.recv(1024)
        received = received.decode()
    finally:
        sock.close()
    return received


if __name__ == "__main__":
    print("arguments: ", sys.argv)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    main()
