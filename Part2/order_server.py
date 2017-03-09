#!/usr/bin/python3
""" This is the order server for managing orders. We use Pyro4 to allow remote execution """
import Pyro4


# TODO: work out what is throwing the errors
# TODO: test backup server propagation properly (by running lots of terminals)
import sys


@Pyro4.expose
class OrderManager(object):
    """ This is a manager to deal with orders"""
    orders = {}
    servers = []

    def __init__(self):
        self.is_primary = True

    def set_state(self, state):
        if not self.is_primary:
            print("My state has been set to: ", str(state))
            self.orders = state
        else:
            print("Primary server, so I can't have my state set.")

    def __update_backup_servers(self):
        if not self.is_primary:
            print("Not the primary server so won't propagate")
            return False  # if we are not the primary server
        print("My current servers are:")
        print(str(self.servers))
        for s in self.servers:
            s.set_state(self.orders)
            print("Set state of remote server")
        return True

    def set_primary_state(self, is_primary):
        print("My state is set to ", str(is_primary))
        self.is_primary = is_primary

    def set_servers(self, servers):
        self.servers = []
        for uri in servers:
            self.servers.append(Pyro4.Proxy(uri))

    def __create_user(self, userid):
        self.orders[userid] = []

    def __format_order_hist(self, userid):
        output = ""
        history = self.orders[userid]
        index = -1
        if history is None or len(history) == 0:
            return "No Order"
        for order in history:
            index += 1
            if order is not None:
                output += "ID: " + str(index) + "      items: " + str(order)
                output += "\n"
        return output

    def place_order(self, userid, item_list):
        # start by updating, then update afterwards
        self.__update_backup_servers()
        """ Place an order """
        if len(item_list) > 3 or len(item_list) <= 0:
            print("Error, must contain at most 3 items")
        if userid not in self.orders:
            self.__create_user(userid)

        self.orders[userid].append(item_list)
        self.__update_backup_servers()
        # get the index of the last element in the list
        return len(self.orders[userid]) - 1

    def get_order_history(self, userid):
        """ Get a user's order history """
        if userid not in self.orders:
            return "User not found"
        # otherwise, format the order history and return it.
        formatted_history = self.__format_order_hist(userid)
        return formatted_history

    def cancel_order(self, userid, orderid):
        orderid = int(orderid)  # convert string to integer
        """ Cancel a user's order """
        if userid not in self.orders:
            return "User not found"
        self.orders[userid][orderid] = None
        self.__update_backup_servers()  # we need to update the backups through the primary server.
        return "Deleted"

    def is_working(self):
        return True

def main(counter):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    url = daemon.register(OrderManager())

    ns.register("OrderManager" + str(counter), url)

    daemon.requestLoop()

if __name__ == "__main__":
    counter_val = sys.argv[1]
    main(counter_val)
