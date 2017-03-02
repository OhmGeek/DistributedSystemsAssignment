""" Despite the name, this file is just a memory based data structure for storing orders
    We simply use dictionaries and lists!

    Abstracted here to allow for later integration with Pyro (for linking several different systems together).

"""


class OrderDB(object):
    def __init__(self):
        pass

    def create_user(self, userID):
        pass

    def add_order(self, userID, order):
        # return order ID
        pass

    def delete_order(self, userID, orderID):
        pass
