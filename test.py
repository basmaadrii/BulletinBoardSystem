import Pyro4

@Pyro4.expose
class Greeting:
    def sayHi(self, name):
        return  'Hi ' + name


daemon = Pyro4.Daemon(host='192.168.1.12', port=5555)

uri = daemon.register(Greeting)
ns = Pyro4.locateNS()
ns.register('obj', uri)
print(uri)

daemon.requestLoop()