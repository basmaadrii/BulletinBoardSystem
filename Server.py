import socket
import threading
from random import randint
from time import sleep


class new_client(threading.Thread):
    def __init__(self, conn, client_address, numberOfAccesses):
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_address = client_address
        self.numberOfAccesses = numberOfAccesses
    def run(self):
        global sSeq, rSeq, rNum, OVAL, writer, rHash

        rtype = ''
        ID = 0

        for i in range(0, self.numberOfAccesses):

            request = self.conn.recv(1024)

            if len(request) > 0:

                fr = open('readers log', 'a+')
                fw = open('writers log', 'a+')

                rtype, ID = request.split(',', 1)
                print 'request received from ', rtype, ID
                f = open('log' + str(ID), 'a+')

                index = str(ID) + str(i)
                rSeq += 1
                rHash[index] = rSeq
                print rHash

                if rtype == 'read':
                    if i == 0:
                        rNum += 1
                    sSeq += 1
                    self.conn.send(str(OVAL) + ',' + str(rHash[index]) + ',' + str(sSeq))
                    fr.write(
                        str(sSeq) + '\t\t' + str(rHash[index]) + '\t\t' + str(OVAL) + '\t\t' + str(ID) + '\t\t' + str(rNum) + '\n')
                    f.write(str(rHash[index]) + '\t\t' + str(sSeq) + '\t\t' + str(OVAL) + '\n')
                    print 'value sent to reader ', ID

                elif rtype == 'write':
                    while (writer): x = 1
                    writer = True
                    OVAL = ID
                    sSeq += 1
                    self.conn.send('OK,' + str(rHash[index]) + ',' + str(sSeq))
                    fw.write(str(sSeq) + '\t\t' + str(rHash[index]) + '\t\t' + str(OVAL) + '\t\t' + str(ID) + '\n')
                    f.write(str(rHash[index]) + '\t\t' + str(sSeq) + '\n')
                    print 'value changed by writer ', ID

                fr.close()
                fw.close()
                f.close()

                t = randint(0, 1000) / 1000.0
                sleep(t)

            if rtype == 'write':
                writer = False

        if rtype == 'read':
            rNum -= 1

        self.conn.close()
        print 'Connection closed with ', rtype, ID


def run_server(IP, Port, numberOfAccesses):

    global sSeq, rSeq, rNum, OVAL, writer, rHash

    writer = False
    sSeq = 0
    rNum = 0
    rSeq = 0
    rHash = {}
    OVAL = -1

    server_address = (IP, Port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    print 'Starting up on IP: ' + IP + ' and Port: ' + str(Port)

    sock.listen(5)
    print 'Waiting for Connection...'

    while True:
        conn, client_address = sock.accept()
        #print 'Connection from ', client_address

        client = new_client(conn, client_address, numberOfAccesses)
        client.start()
