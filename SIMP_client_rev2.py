import socket
import time
from message import create_header, check_header

def start_chatting(s,host,port):
    print('welcome to Jacquelines and Rados SIMP V1.0.0')
    uname = input('enter username: ')
    sq = 0
    while(True):
        sq+=1
        message = input(f'{uname}: ')
        m = create_header('chat','send message',sq,uname,message)
        #print(m)      
        s.sendto(m,(host,port)) #send original message
        if message =='quit':
            break
        reply,host_from = s.recvfrom(1024) #gets ACK message
        #print('ACK', reply)
        reply,host_from = s.recvfrom(1024) #gets the real message
        if check_header(reply)[5] == 'quit':         
            break
        print(check_header(reply)[5])
    return 0

def handshake(s,host,port):
    while(True):
        #send SYN
        sq=0
        m = create_header('cm','SYN',sq,'name','')
        s.sendto(m, (host, port))
        print('send SYN....')
        #get reply
        try:
            reply,host_from = s.recvfrom(1024)
            #check reply and take action
            if check_header(reply)[1] == 6: #operation SYN+ACK = 6  
                sq +=1
                m = create_header('cm','ACK',sq,'name','')
                s.sendto(m,(host, port))
                return 1

            elif check_header(reply)[1] == 8: #operation FIN = 8  
                sq += 1
                m = create_header('cm','ACK',sq,'name','')
                s.sendto(m,(host, port))
                print('chat request rejected')
                return 0
            else:
                print('unknown')
                continue
    
        except socket.timeout:
            time = s.gettimeout()
            print(f'timeout hit after {time} seconds')
            continue
        
if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #print('default TO ', s.gettimeout())
        s.settimeout(5)
        host = '127.0.0.1'
        port = 8080
    
        if handshake(s,host,port)==1:
            s.settimeout(None)
            if start_chatting(s,host,port)== 0:
                exit()
        else:
            exit()
