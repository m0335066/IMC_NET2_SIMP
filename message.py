import string

def create_header(message_type:string , operation: string, sequence_nb: int, username: string , message: string ):
    #1byte message type: 0x01 = chat, 0x02 = control message
    #1byte operation: for chat = 0x01 = send message; for control = 0x01 = error, 0x02 = SYN, 0x04 = ACK, 0x08 = FIN
    #1byte sequence number: Can take values 0x00 or 0x01.
    #32 bytes user: User name in ASCII encoding
    #xbytes payload length
    #x bytes payload
    
    #assign 2 for message type 'control message' or 1 for 'chat'
    if message_type == 'cm':
        b_arr = bytearray(4)
        b_arr[0] = 2

    elif message_type == 'chat':
        b_arr = bytearray(6)
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
    b_arr[2] = 0

    #assign username at index 3
    bytes_username = 32
    lead_zeros = bytes_username-len(username)
    b_arr += (str(lead_zeros*'0')+username).encode('ASCII')

    if message_type == 'chat':
        #assign payload len at index 4
        b_arr += (len(message)).to_bytes(1,byteorder ='little')

        #assign payload at index 5
        b_arr += message.encode('ASCII')
    return b_arr

def check_header(header: bytes):
    #message type, operation, sequence nb, use rname, pl len, pl

    #x = int.from_bytes(header[0],byteorder = 'little')
    return header[1],header[2]
    #if int.from_bytes(header[0],byteorder = 'little') == 1:
    #    #chat
    #    return 'chat'
    #else:
    #    #control message
    #    return 'control message'