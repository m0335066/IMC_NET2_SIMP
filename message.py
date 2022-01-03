import string


def create_header(message_type:string , operation: string, sequence_nb: int, username: string , message: string ):
    '''
    takes 5 parameters as inout and creates a bytearray
    returns a bytearray
    for message type cm a default username 'uname' is used and 'message length' and 'chat message' do not exist
    hence the array is shorter'''
    #1byte message type: 0x01 = chat, 0x02 = control message
    #1byte operation: for chat = 0x01 = send message; for control = 0x01 = error, 0x02 = SYN, 0x04 = ACK, 0x08 = FIN
    #1byte sequence number: Can take values 0x00 or 0x01.
    #32 bytes user: User name in ASCII encoding
    #1bytes payload length
    #x bytes payload
    
    #assign 2 for message type 'control message' or 1 for 'chat'
    if message_type == 'cm':
        b_arr = bytearray(3)
        b_arr[0] = 2

    elif message_type == 'chat':
        b_arr = bytearray(3)
        b_arr[0] = 1

    #assign operation at index 1 depending on function input
    if operation == 'send message':
        b_arr[1] = 1
    elif operation == "error":
        b_arr[1] = 1
    elif operation == "SYN":
        b_arr[1] = 2
    elif operation == "ACK":
        b_arr[1] = 4
    elif operation == "SYN+ACK":
        b_arr[1] = 6
    elif operation == "FIN":
        b_arr[1] = 8
    else:
        print('unknown operation')
        pass

    #assign sequence number at index 2
    b_arr[2] = sequence_nb

    #assign username at index 3
    bytes_username = 32
    lead_zeros = bytes_username-len(username)
    b_arr += (str(lead_zeros*'0')+username).encode('ASCII')

    if message_type == 'chat':
        #assign payload len at index 4
        b_arr += (len(message)).to_bytes(1,byteorder ='little')

        #assign payload at index 5
        b_arr += message.encode('ASCII')
    #print(f'send {operation}')
    return b_arr


def check_header(header:bytearray):
    '''
    takes a bytearray as input and extracts single components as 
    message_type:int , operation: int, sequence_nb: int, username: string , message_length: int , message: string 
    returns the following parameters: message type, operation, sequence number, username, message_length, chat_message
    '''
    h = header
    mtype = h[0]
    operation = h[1]
    chat_message = h[36:].decode('ASCII')
    message_length = h[35]
    name = h[5:35].decode('ASCII').replace('0','')
    sequnr = h[2]
    return (mtype, operation, sequnr, name, message_length, chat_message)



sq = 1
control_mess = create_header('cm','ACK',sq,'username','')
sq = 2
control_mess1 = create_header('cm','SYN+ACK',sq,'username','')
chat_mess = create_header('chat','send message',sq,'RADOMIR','hello this is Rado')

print('control message ACK: ',control_mess)
print('control message SYN+ACK: ',control_mess1)
print('chat message ', chat_mess)

print(check_header(chat_mess))

