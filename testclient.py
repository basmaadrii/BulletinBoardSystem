import  Pyro4

ns = Pyro4.locateNS(host='192.168.1.10')

uri = ns.lookup('obj')

o = Pyro4.Proxy(uri)

print(o.sayHi('basma'))