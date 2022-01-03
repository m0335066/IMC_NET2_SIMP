import socket
import time
from message import create_header, check_header

def start_chatting(s,host,port):
    uname = input('enter username: ')
    pass

def wait_and_receive(s,host,port):
    s.bind((host,port))
    pass        

if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        host = '127.0.0.1'
        port = 8080

        if wait_and_receive(s,host,port)==1:
            print('welcome to Jacquelines and Rados SIMP V1.0.0')
            if start_chatting(s,host,port)==0:
                exit()
        else:
            exit(0)

 