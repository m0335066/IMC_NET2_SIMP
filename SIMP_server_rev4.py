import socket
import time
from message import create_header, check_header

def start_chatting(s,host,port):
    uname = input('enter username: ')
    sq_server = 100
    sq_user = 0
    while(True):
        #receive chat meesage
        reply,host_from = s.recvfrom(1024)
        #print(reply[2],' vs ',sq_user)
        while (reply[2]!=sq_user):###################################
            #reject message if sq doesnt match 
            reply,host_from = s.recvfrom(1024)

        #user wants to quit and sent a FIN
        if check_header(reply)[1]==8:
            break

        print(check_header(reply)[3], ': ', check_header(reply)[5])
        #send back ACK
        m = create_header('cm','ACK',reply[2],uname,'')
        sq_user = reply[2]
        time.sleep(7) ########################################change to delay ACKs
        s.sendto(m,host_from)
        #print('sending sq: ', m[2])

        ########################################send chat message
        message = input(f'{uname}: ')

        #server wants to quit and sends a FIN
        if message == 'quit':
            m = create_header('cm','FIN',sq_server,uname,'') 
            s.sendto(m,host_from)   
            break

        while(True):
            m = create_header('chat','send message',sq_server,uname,message)
            s.sendto(m,host_from)    
            #print('sending sq: ', m[2])    
            s.settimeout(5)
            try:
                reply, host_from = s.recvfrom(1024) 
                #print(reply[2],' vs ',sq_server)
                while (reply[2]!=sq_server):#############################
                    #print('2: discard frame with sq nb =', reply[2])
                    reply, host_from = s.recvfrom(1024)
            except socket.timeout:
                print('STO: resend' , m , 'with sq = ', m[2])
                continue
            break   
        s.settimeout(None)
        sq_server = sq_server + 1  
        sq_user = sq_user + 1  
        

    return 0


def wait_and_receive(s,host,port):
    s.bind((host,port))
    while (True):
        #receive SYN
        data, host_from = s.recvfrom(1024)
        sq = data[2]
        #check data and take action
        if check_header(data)[1] == 2: #operation SYN = 2
            answer = input(f'accept connection request from {host_from}? press [y] to continue: ')
            if answer == 'y': #server accepts the chat request
                m = create_header('cm','SYN+ACK',sq,'name','')
                s.sendto(m,host_from)
                sq += 1

                data, host_from = s.recvfrom(1024)
                #print(check_header(data), 'compared with ', sq)
                '''while check_header(data)[2] != sq: #this while loop discards the old sent SYN frames and waits for the enhanced sequence number
                    #print('discard frame')
                    data, host_from = s.recvfrom(1024)
                    #print(check_header(data), 'compared with ', sq)
                    continue'''

                if check_header(data)[1] == 4 and check_header(data)[2] == sq: #operation ACK = 4
                    print('handshake succesfull')   
                    return 1
                else:
                    print(data)
                    continue #if the sequence number is still zero, we keep going
            else: #server refuses to connect
                m = create_header('cm','FIN',sq,'name','')
                s.sendto(m,host_from)
                sq += 1 

                data, host_from = s.recvfrom(1024)
                while check_header(data)[2] != sq: #this while loop discards 
                    #print('discard frame')
                    data, host_from = s.recvfrom(1024)
                    #print(check_header(data), 'compared with ', sq)
                    continue

                if check_header(data)[1] == 4 and check_header(data)[2] == sq: #operation ACK = 4
                    print('connection cut')
                    exit(0)
                else:
                    continue
            

if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        host = '127.0.0.1'
        port = 8080

        if wait_and_receive(s,host,port)==1:
            print('welcome to Jacquelines and Rados SIMP V1.0.0')
            #s.settimeout(5)
            if start_chatting(s,host,port)==0:
                exit()
        else:
            exit(0)

 