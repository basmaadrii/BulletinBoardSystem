import threading
from random import randint
from time import sleep
import Pyro4


def run_server(IP, Port, numberOfAccesses):

    @Pyro4.expose
    class Client:
        def reader(self, ID, i):
            global sSeq, rSeq, rNum, OVAL, writer, rHash

            fr = open('readers log', 'a+')
            f = open('log' + str(ID), 'a+')
            print 'ID', ID
            print 'i', i
            index = str(ID) + str(i)
            rSeq += 1
            rHash[index] = rSeq
            print rHash

            if i == 0:
                rNum += 1

            sSeq += 1

            fr.write(str(sSeq) + '\t\t' + str(rHash[index]) + '\t\t' + str(OVAL) + '\t\t' + str(ID) + '\t\t' + str(rNum) + '\n')
            f.write(str(rHash[index]) + '\t\t' + str(sSeq) + '\t\t' + str(OVAL) + '\n')
            print 'value sent to reader ', ID

            fr.close()
            f.close()

            t = randint(0, 1000) / 1000.0
            sleep(t)

            if i == numberOfAccesses - 1:
                rNum -= 1

            return OVAL, rHash[index], sSeq


        def writer(self, ID, i):
            global sSeq, rSeq, rNum, OVAL, writer, rHash

            fw = open('writers log', 'a+')
            f = open('log' + str(ID), 'a+')
            print 'ID', ID
            print 'i', i
            index = str(ID) + str(i)
            rSeq += 1
            rHash[index] = rSeq
            print rHash

            while (writer): x = 1
            writer = True
            OVAL = ID
            sSeq += 1
            fw.write(str(sSeq) + '\t\t' + str(rHash[index]) + '\t\t' + str(OVAL) + '\t\t' + str(ID) + '\n')
            f.write(str(rHash[index]) + '\t\t' + str(sSeq) + '\n')
            print 'value changed by writer ', ID

            fw.close()
            f.close()

            t = randint(0, 1000) / 1000.0
            sleep(t)

            writer = False

            return 'OK', rHash[index], sSeq

    global sSeq, rSeq, rNum, OVAL, writer, rHash

    writer = False
    sSeq = 0
    rNum = 0
    rSeq = 0
    rHash = {}
    OVAL = -1

    daemon = Pyro4.Daemon(host=IP, port=Port)

    uri = daemon.register(Client)
    ns = Pyro4.locateNS()
    ns.register('client', uri)
    print(uri)

    daemon.requestLoop()