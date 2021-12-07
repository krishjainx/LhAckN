import socket
import threading



listOfAllConnections = []
def dealwithconnection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            themessage = connection.recv(1024)
            if themessage:
                print(f'{address[0]}:{address[1]} - {themessage.decode()}')
                thetext = f'From {address[0]}:{address[1]} - {themessage.decode()}'
                send(thetext, connection)
            else:
                deleteConnection(connection)
                break
        except Exception as e:
            print(f'Unable to create link with user {e}')
            deleteConnection(connection)
            break
def send(message: str, connection: socket.socket) -> None:

    for client_connection in listOfAllConnections:
        if client_connection != connection:
            try:
                client_connection.send(message.encode()) # send message to all users
            except Exception as e:
                print('We have faced problems sending message to other users {e}')
                deleteConnection(client_connection)
def deleteConnection(connection: socket.socket) -> None:
    if connection in listOfAllConnections:
        connection.close()
        listOfAllConnections.remove(connection)
LISTENING_PORT = 14000 # non admin port on macOS and Linux
try:
    instanceofsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    instanceofsocket.bind(('', LISTENING_PORT))
    instanceofsocket.listen(4)
    print('Server running!')
    while True:
        socket_connection, address = instanceofsocket.accept()
        listOfAllConnections.append(socket_connection)
        threading.Thread(target=dealwithconnection, args=[socket_connection, address]).start()
except Exception as e:
    print(f'Cant connect to the network interface {e}')
finally:
    # abort 
    if len(listOfAllConnections) > 0:
        for connection in listOfAllConnections:
            deleteConnection(connection)
    instanceofsocket.close()


# References: https://realpython.com/python-sockets/, https://www.geeksforgeeks.org/socket-programming-python/, https://stackoverflow.com/questions/1593946/what-is-af-inet-and-why-do-i-need-it
# , https://www.w3.org/Daemon/User/Installation/PrivilegedPorts.html, https://www.freecodecamp.org/news/if-name-main-python-example/, https://pythontic.com/modules/socket/recv
