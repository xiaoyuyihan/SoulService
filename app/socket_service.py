from socket import *

HOST = '127.0.0.1'
PORT = '12345'


appsocket=socket.socket(family=AF_INET,type=SOCK_STREAM)

"""
单链接
"""


def StartSocket():
    appsocket.bind((HOST, PORT))
    appsocket.listen(5)

    while True:
        tcpCliSockm, addr= appsocket.accept()
        while True:
            data = tcpCliSockm.recv(1024)
            if not data:
                break
            tcpCliSockm.close()
    appsocket.close()

