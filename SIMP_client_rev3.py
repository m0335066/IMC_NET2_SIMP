import socket
import time
from message import create_header, check_header

def start_chatting(s,host,port):
    print('welcome to Jacquelines and Rados SIMP V1.0.0')
    #uname = input('enter username: ')
    uname = 'jacqui'
    sq_user = 0
    sq_server = 100
    message = input(f'{uname}: ')
    while(True):   
        
        m = create_header('chat','send message',sq_user,uname,message)
        ################################################send chat message
        s.sendto(m,(host,port))
        #print('sending sq: ', m[2])
        s.settimeout(5)
        ##########wait for chat ACK
        try:
            reply, host_from = s.recvfrom(1024)
            print(reply[2],' vs ',sq_user)
            while (reply[2]!=sq_user):###################################
                print('2: discard frame with sq nb =', reply[2])
                reply, host_from = s.recvfrom(1024)
        except socket.timeout:
            print('STO: resend' , m , 'with sq = ', m[2])
            continue
        
        #receive chat message after ACK
        s.settimeout(None)
        reply, host_from = s.recvfrom(1024)
        print(reply[2],' vs ',sq_server)
        while(reply[2]!=sq_server):########################################
            print('2: discard frame with sq nb =', reply[2])
            #reject message if sq doesnt match 
            reply, host_from = s.recvfrom(1024)
        print(check_header(reply)[3], ': ', check_header(reply)[5])
        #send back ACK
        m = create_header('cm','ACK',reply[2],uname,'')
        sq_server = reply[2]
        time.sleep(11)########################################change to delay ACKs
        s.sendto(m,(host,port))
        #print('sending sq: ', m[2])
        message = input(f'{uname}: ')
        sq_user = sq_user + 1
        sq_server = sq_server + 1

    return 0

def handshake(s,host,port):
    while(True):
        #send SYN
        sq=0
        m = create_header('cm','SYN',sq,'name','')
        s.sendto(m, (host, port))
        print('send SYN....')
        #get reply
        #try:
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
            #print(reply)
            print('unknown')
            #break
            continue
            #return 0
    
        
if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #print('default TO ', s.gettimeout())
        #s.settimeout(5)
        host = '127.0.0.1'
        port = 8080
    
        if handshake(s,host,port)==1:
            #s.settimeout(5)
            if start_chatting(s,host,port)== 0:
                exit()
        else:
            exit()
    