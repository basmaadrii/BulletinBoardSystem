import threading
from time import sleep
from Server import run_server
import spur


class server_thread(threading.Thread):
    def __init__(self, IP, port, numberOfAccesses):
        threading.Thread.__init__(self)
        self.IP = IP
        self.port = port
        self.numberOfAccesses = numberOfAccesses

    def run(self):
        run_server(self.IP, self.port, self.numberOfAccesses)


class reader_thread(threading.Thread):
    def __init__(self, IP, numberOfAccesses, ID):
        threading.Thread.__init__(self)
        self.IP = IP
        self.numberOfAccesses = numberOfAccesses
        self.ID = ID
    def run(self):
        command = 'python ./Downloads/BulletinBoardSystem/Clientreader.py ' \
                        + self.IP + ' ' + str(self.numberOfAccesses) + ' ' + str(self.ID)
        ssh(command)

class writer_thread(threading.Thread):
    def __init__(self, IP, numberOfAccesses, ID):
        threading.Thread.__init__(self)
        self.IP = IP
        self.numberOfAccesses = numberOfAccesses
        self.ID = ID
    def run(self):
        command = 'python ./Downloads/BulletinBoardSystem/Clientwriter.py ' \
                        + self.IP + ' ' + str(self.numberOfAccesses) + ' ' + str(self.ID)
        ssh(command)


def system_config(filename):
    keys = {}

    with open(filename) as f:
        for line in f:
            if '=' in line:
                name, value = line.split('=', 1)
                if name == 'server.port' or name == 'numberOfAccesses' or name == 'numberOfReaders' or name == 'numberOfWriters':
                    keys[name.strip()] = int(value.strip())
                else:
                    keys[name.strip()] = value.strip()

    return keys


def initiate_log_files():

    for i in range(0, 8):
        f = open('log' + str(i), 'w+')
        if i < 4:
            f.write('Client type: Reader\nClient Name: ' + str(i) + '\nrSeq\tsSeq\toVal\n')
        else:
            f.write('Client type: Writer\nClient Name: ' + str(i) + '\nrSeq\tsSeq\n')

    f = open('readers log', 'w+')
    f.write('sSeq\trSeq\toVal\trID\t\trNum\n')

    f = open('writers log', 'w+')
    f.write('sSeq\trSeq\toVal\twID\n')


def ssh(command):
    hostname = '192.168.1.11'
    port = 22
    username = 'nouran'
    password = '12345'

    shell = spur.SshShell(hostname, username, password, port)
    result = shell.run(command.split(' '))
    print result.output
    print result.stderr_output

initiate_log_files()
config = system_config('system.properties')

serverThread = server_thread(config['server'], config['server.port'], config['numberOfAccesses'])
serverThread.start()
sleep(0.1)

for i in range(0, config['numberOfReaders']):
    reader = reader_thread(config['server'], config['numberOfAccesses'], str(i))
    reader.start()

for i in range(0, config['numberOfWriters']):
    writer = writer_thread(config['server'], config['numberOfAccesses'], str(i + 4))
    writer.start()

