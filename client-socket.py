import socket
import threading

serveraddress = input("Input a valid ip address for server of chat: ")
def dealwithmessages(connection: socket.socket):
 
    while True:
        try:
            themessage = connection.recv(1024)  # read at most 1024 bytes, blocking if no data is waiting to be read.

            if themessage:
                print(themessage.decode())
            else:
                connection.close()
                break

        except Exception as problem:
            print(f'Problem dealing with message from the socket server: {problem}')
            connection.close()
            break


def client() -> None:

    try:

        instanceofsocket = socket.socket()
        instanceofsocket.connect((serveraddress, 14000))

        threading.Thread(target=dealwithmessages, args=[
                         instanceofsocket]).start()

        print('Could connect')

        while True:
            themessage = input()

            if themessage == 'exit':
                break

            instanceofsocket.send(themessage.encode())

        instanceofsocket.close()

    except Exception as error:
        print(f'Problem establishing connection to server {error}')
        instanceofsocket.close()

if __name__ == "__main__": #  script is being run directly , not imported by something else as  if module is being run directlythen __name__ instead is set to the string "__main__". 
 client()
