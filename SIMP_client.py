import socket
import time
from message import create_header, check_header

def start_chatting(s,host,port):
    print('welcome to Jacquelines and Rados SIMP V1.0.0')
    uname = input('enter username: ')
    pass

def handshake(s,host,port):
    pass
        
if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #print('default TO ', s.gettimeout())
        s.settimeout(50)
        host = '127.0.0.1'
        port = 8080
    
        if handshake(s,host,port)==1:
            s.settimeout(None)
            if start_chatting(s,host,port)== 0:
                exit()
        else:
            exit()
