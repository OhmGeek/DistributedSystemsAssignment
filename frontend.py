#!/usr/bin/python3
""" User Client """
import random
import string
import Pyro4


# TODO: generate userid on server, as this is something we want to ensure is unique.
class FrontEnd(object):
    """ This is the Client Controller, allowing possible actions to be executed """

    def __init__(self, is_primary):
        self.userid = self.__gen_user_id()
        # now connect to the server
        ns = Pyro4.locateNS()
        server_uri = ns.lookup("OrderManager")
        self.manager_server = Pyro4.Proxy(server_uri)

    @staticmethod
    def __gen_user_id():
        """ Generate user ID """
        my_ID = ""
        for i in range(1, 20):
            my_ID += random.choice(string.ascii_uppercase)
        return my_ID

    @staticmethod
    def print_options():
        """ Print the options of the client program """
        print("\n\nBeagle's Shop")
        print("-----------------------")
        print("Options:")
        print("     1  -   Create Order")

    def create_order(self):
        """ Allows the user to create an order """
        print("Insert items to order. Max 3 items per order.")
        print("Press the enter key to finish.")
        finished = False
        item_num = 0
        items_to_order = []
        while not finished:
            item_num += 1
            item = input("Item " + str(item_num) + " ")
            if item == "":
                finished = True
            else:
                items_to_order.append(item)

            # now check for finish
            if item_num >= 3:
                finished = True

        self.manager_server.place_order(self.userid, items_to_order)


def control_manager(program, opt):
    """ Manages flow of control based on the option input """
    if opt == "1":
        program.create_order()
    elif opt == "q":
        print("Bye!")
    else:
        print("Invalid option. Try again")


def main():
    exit_status = False
    prog = FrontEnd()
    while not exit_status:
        prog.print_options()
        option = input("Select option: ")
        control_manager(prog, option)

        # listen for the exit command
        if option == "q":
            exit_status = True


if __name__ == "__main__":
    main()