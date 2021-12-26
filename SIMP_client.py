#!/usr/bin/env python3

import socket
import sys
import string
import time
from message import create_header  
from message import check_header

def send(message:bytes, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

        #uname = input('welcome to SIMP client 1.0.0\nPlease enter your name:\n')
        sq = 0
        data_send = create_header('cm','SYN',sq,'uname','')
        s.sendto(data_send, (host, port)) #send SYN
        count=time.time()
        reply = s.recv(1024)
        while count-time.time() > 5 and not reply:
            print('re-send lost packet')
            s.sendto(data_send, (host, port))
        sq += 1
        reply = s.recv(1024)
        if reply[2] == sq  :
        #    data_send = create_header('cm','ACK',1,uname,'')
        #    s.sendto(data_send, (host, port)) #send ACK

        #message = input('>')
        #data_send = create_header('chat','send message',uname,message,2)
        # data_send = bytearray(message)
            s.sendto(data_send, (host, port))
        #reply = s.recv(1024)
        #return repr(reply)
        #return type(data_send)
        return data_send


if __name__ == "__main__":

    #host = "127.0.0.1"
    #port = 5000  

    data = send(sys.argv[0],"127.0.0.1",5000)
    print('Received', data)
