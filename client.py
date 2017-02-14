
class Client(object):
    """ This is the Client Controller, allowing possible actions to be executed """
    def __init__(self):
        pass
    def print_options(self):
        """ Print the options of the client program """
        print("TODO PRINT OPTIONS")
    def option(self):
        """ This is an example option """
        pass

def control_manager(program, option):
    """ Manages flow of control based on the option input """
    if option == "1":
        prog.option()
    else:
        print("Invalid option. Try again")

if __name__ == "__main__":
    exit_status = False
    prog = Client()
    while not exit_status:
        prog.print_options()
        option = input("Select option: ")
        control_manager(prog, option)

        # listen for the exit command
        if option == "q":
            exit_status = True
    
