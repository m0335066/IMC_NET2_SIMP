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
    between user and server. The aim is to resend messages if no ACK is received after 5 seconds
    '''
    #user inputs a name and sequence numbers for server and user are initialized manually (we took 0 and 100 for simplicity)
    uname = input('enter username: ')
    sq_user = 0
    sq_server = 100
    #user types the message he aims to send
    message = input(f'{uname}: ')
    #infinite while loops starts to allow message exchange until user or server quits
    while(True):   
        #user message is checked to see if user wants to quit and sends a FIN if so
        if message == 'quit':
            m = create_header('cm','FIN',sq_user,uname,'') 
            s.sendto(m,(host,port))   
            break
        #if user message is NOT a quit request the message gets transformed into a header
        #with the create_header function from message.py
        m = create_header('chat','send message',sq_user,uname,message)
        ################################################send chat message frame
        s.sendto(m,(host,port))
        #print('sending sq: ', m[2])
        s.settimeout(5) #set timeout to 5 seconds for the ACK
        #######################################################wait for chat ACK
        try:
            reply, host_from = s.recvfrom(1024)
            #print(reply[2],' vs ',sq_user)
            while (reply[2]!=sq_user):######################wait for correct sq number
                #the print statement allows to see discarded frames with wrong sequence numbers
                #print('2: discard frame with sq nb =', reply[2]) 
                reply, host_from = s.recvfrom(1024)
        except socket.timeout:
            #the print statement allows to see the re-send frame
            #print('STO: resend' , m , 'with sq = ', m[2])
            continue
        
        #ready to receive chat message frame from server after ACK
        s.settimeout(None) #set timeout to NOne for the chat message to allow user to take more then 5 seconds to reply
        reply, host_from = s.recvfrom(1024)
        #this print statement visualizes incomng sequence numbers versus expected sequence number
        #print(reply[2],' vs ',sq_server)
        while(reply[2]!=sq_server):############################wait for correct sq number
            #the print statement allows to see discarded frames with wrong sequence numbers
            #print('2: discard frame with sq nb =', reply[2])
            reply, host_from = s.recvfrom(1024)

        #server sent a FIN and wants to quit
        if check_header(reply)[1]==8:
            return 0

        #here the actual chat message frame gets displayed together with the server name
        print(check_header(reply)[3], ': ', check_header(reply)[5])
        #user created a control frame with ACK using create_header function
        m = create_header('cm','ACK',reply[2],uname,'')
        #saves the incoming server_sq to increment it later to have the acceptance criterion
        sq_server = reply[2]
        #time.sleep allows to delay the ACK that gets sent to see if server responds 
        #by resending the chat message frames after 5 seconds
        #time.sleep(2)########################################
        #user sends back an ACK control frame
        s.sendto(m,(host,port))
        #print('sending sq: ', m[2])
        #user is prompted for his message
        message = input(f'{uname}: ')
        #sequence numbers are enhanced by 1
        sq_user = sq_user + 1
        sq_server = sq_server + 1

    return 0

def handshake(s,host,port):
    '''
    The function opens an infinite while loop that continues until user or server 
    manually exit it by sending quit message or receiving a FIN message
    '''
    while(True):
        #user sends a SYN control frame to server
        sq=0
        m = create_header('cm','SYN',sq,'name','')
        s.sendto(m, (host, port))
        print('send SYN....')
        #user waits for a reply frame
        reply,host_from = s.recvfrom(1024)
        #once reply arrives, check reply with the check_header function from message.py and take action
        #option1 the user gets a SYN+ACK and sends back an ACK, returns 1 to exit the handshake function
        if check_header(reply)[1] == 6: #operation SYN+ACK = 6  
            sq +=1
            m = create_header('cm','ACK',sq,'name','')
            s.sendto(m,(host, port))                
            return 1
        #option2 the user gets a FIN which means server declines the reuqest and user sends back an ACK and quits the connection by returning 0
        elif check_header(reply)[1] == 8: #operation FIN = 8  
            sq += 1
            m = create_header('cm','ACK',sq,'name','')
            s.sendto(m,(host, port))
            print('chat request rejected')
            return 0

        #option3 an error control frame and user closes
        elif check_header(reply)[1] == 1:
            print('received an error')
            return 0

        #option4 gives opportunity to catch any unknown statements
        else:
            print('unknown')
            continue
    
        
if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        #host = '127.0.0.1'
        #port = 8080
        '''
        socket is opened and function handshake gets called with system inputs IP adress and host
        when fct handshake returns 1 it means handshale was successful and function 
        start_chatting gets called. If fct start_chatting returns 0, which happens if
        the user or the server quit the chat, then the program exits
        '''
        if handshake(s,sys.argv[1],int(sys.argv[2]))==1:
            print('welcome to Jacquelines and Rados SIMP V1.0.0')
            if start_chatting(s,sys.argv[1],int(sys.argv[2]))== 0:
                exit()
        else:
            exit()
