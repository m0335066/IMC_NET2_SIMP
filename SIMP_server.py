#!/usr/bin/env python3

import socket
import sys
from message import create_header
from message import check_header

def wait_and_receive(host, port):
    print('Waiting for connections...')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        sq = 0
        while True:
            data, host_from = s.recvfrom(1024)
            print(check_header(data)) #return sequence number header[2]
            if data[2] == sq:
                data_send=create_header('cm','SYN+ACK',sq,'uname','')
                sq +=1
            s.sendto(data_send, host_from)
            if not data:
                continue
            


if __name__ == "__main__":
            
    #wait_and_receive(sys.argv[1], int(sys.argv[2]))
    try:
        wait_and_receive("127.0.0.1",5000)
    except ConnectionResetError:
        print('Connection Reset Error')