#!/usr/bin/python3
""" This is the order server for managing orders. We use Pyro4 to allow remote execution """
import Pyro4


# todo: refactor orders to be a custom data structure wrapper (so we can decrease coupling)
@Pyro4.expose
class OrderManager(object):
    """ This is a manager to deal with orders"""
    def __init__(self):
        # create a list of orders
        self.orders = {}

    def __create_user(self, userid):
        self.orders[userid] = []

    def __format_order_hist(self, userid):
        output = ""
        history = self.orders[userid]
        index = -1
        for order in history:
            index += 1
            if order is not None:
                output += "ID: " + str(index) + "      items: " + str(order)
                output += "\n\n"
        return output

    def place_order(self, userid, item_list):
        """ Place an order """
        if len(item_list) > 3 or len(item_list) <= 0:
            print("Error, must contain at most 3 items")
        if userid not in self.orders:
            self.__create_user(userid)

        self.orders[userid].append(item_list)
        # get the index of the last element in the list
        return len(self.orders[userid]) - 1

    def get_order_history(self, userid):
        """ Get a user's order history """
        if userid not in self.orders:
            print("User not found")
        # otherwise, format the order history and return it.
        formatted_history = self.__format_order_hist(userid)
        return formatted_history

    def cancel_order(self, userid, orderid):
        """ Cancel a user's order """
        if userid not in self.orders:
            print("User not found")
            return False
        self.orders[userid][orderid] = None
        return True



daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

url = daemon.register(OrderManager)
ns.register("OrderManager", url)
daemon.requestLoop()

