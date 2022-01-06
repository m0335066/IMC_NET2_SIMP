'''
AUTHORS: JACQUELINE BERGER AND RADOMIR ROMAN
COURSE: NETWORKING 2
'''
import socket
import time
import sys
from message import create_header, check_header

def start_chatting(s,host,port):
    '''
    The function takes the socket, host and port as input variables and keeps sending messages
    between user and server. The aim is to resend messages if no ACK is received after 5 seconds    '''
    uname = input('enter username: ')
    sq_server = 100
    sq_user = 0
    while(True):
        #server receives the first chat meesage
        reply,host_from = s.recvfrom(1024)
        #print(reply[2],' vs ',sq_user),
        #user sequence number gets checks before proceeding
        while (reply[2]!=sq_user):###################################
            #reject message if sq doesnt match 
            reply,host_from = s.recvfrom(1024)

        #the received frame is checked if user wants to quit, in that case FIN was received (corresponds to 8)
        if check_header(reply)[1]==8:
            break
        
        #here the actual chat message frame gets displayed together with the server name 
        print(check_header(reply)[3], ': ', check_header(reply)[5])
        #server creates an ACK control frame with the create_header function
        m = create_header('cm','ACK',reply[2],uname,'')
        sq_user = reply[2]
        #time.sleep(7) ########################################change to delay ACKs
        #server sends back an ACK control frame
        s.sendto(m,host_from)
        #print('sending sq: ', m[2])

        ########################################send chat message
        #server is asked for the message he wants to send
        message = input(f'{uname}: ')

        #if server wants to quit,a FIN control frame gets prepared and sent and connection closes
        if message == 'quit':
            m = create_header('cm','FIN',sq_server,uname,'') 
            s.sendto(m,host_from)   
            break
        
        #this while loops keeps sending chat messages if no ACK control frame is received
        #after 5 seconds
        while(True):
            m = create_header('chat','send message',sq_server,uname,message)
            s.sendto(m,host_from)    
            #print('sending sq: ', m[2])    
            s.settimeout(5)
            try:
                reply, host_from = s.recvfrom(1024) 
                #print(reply[2],' vs ',sq_server)
                while (reply[2]!=sq_server):#############################
                    #the print statement allows to see discarded frames with wrong sequence numbers
                    #print('2: discard frame with sq nb =', reply[2])
                    reply, host_from = s.recvfrom(1024)
            except socket.timeout:
                #the print statement allows to see the re-send frame
                #print('STO: resend' , m , 'with sq = ', m[2])
                continue
            break   
        #set timeout to NOne for the chat message to allow user to take more then 5 seconds to reply
        s.settimeout(None)
        #sequence numbers are enhanced by 1
        sq_server = sq_server + 1  
        sq_user = sq_user + 1  
        

    return 0

def wait_and_receive(s,host,port):
    '''
    This function binds the socket and starts an infinite loop waiting for SYN request
    control frame from the user
    '''
    s.bind((host,port))
    while (True):
        #server receives a SYN frame from the user
        data, host_from = s.recvfrom(1024)
        #sequence number gets extracted and will be used in the reply 
        sq = data[2]
        #check received data with the check_header function and take action
        if check_header(data)[1] == 2: #operation SYN = 2
            #server can accept or reject the chat request
            answer = input(f'accept connection request from {host_from}? press [y] to continue: ')
            if answer == 'y': #server accepts the chat request
                #if server want to continue chatting, a headeris created with create_header function from message.py
                m = create_header('cm','SYN+ACK',sq,'name','')
                #control frame is sent
                s.sendto(m,host_from)
                sq += 1

                #server waits for reply, that should be ACK 
                data, host_from = s.recvfrom(1024)
                #if ACK is received and sequence number matchesm the handhsake was successful and
                #function returns a 1
                if check_header(data)[1] == 4 and check_header(data)[2] == sq: #operation ACK = 4
                    print('handshake succesfull')   
                    return 1
                else:
                    print(data)
                    continue #if the sequence number is still zero, we keep going
            
            else: #in case the server refused to connect, a FIN control frame is prepared and sent
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
        #host = '127.0.0.1'
        #port = 8080
        '''
        socket is opened and function wait_and_receive gets called with system inputs IP address
        when fct handshake returns 1 it means handshale was successful and function 
        start_chatting gets called. If fct start_chatting returns 0, which happens if
        the user or the server quit the chat, then the program exits
        '''
        if wait_and_receive(s,sys.argv[1],int(sys.argv[2]))==1:
            print('welcome to Jacquelines and Rados SIMP V1.0.0')
            if start_chatting(s,sys.argv[1],int(sys.argv[2]))==0:
                exit()
        else:
            exit(0)

 