import Pyro4

@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self,name):
        return "Hello " + str(name)

daemon = Pyro4.Daemon()
uri = daemon.register(GreetingMaker)

print("Ready. Object URI is", uri)
daemon.requestLoop()