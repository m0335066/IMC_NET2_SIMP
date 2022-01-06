from message import create_header, check_header

def test_create_header_meassage():
    assert create_header(
        'chat','send message',2,'RADOMIR','hello this is Rado') == b'\x01\x01\x020000000000000000000000000RADOMIR\x12hello this is Rado'

def test_create_header_ack_syn_plus_ack():
    assert create_header('cm','ACK',1,'username','') == b'\x02\x04\x01000000000000000000000000username\x00'
    assert create_header('cm','SYN+ACK',2,'username','') == b'\x02\x06\x02000000000000000000000000username\x00'


def test_check_header():
    assert check_header(
        create_header('chat','send message',2,'RADOMIR','hello this is Rado')) == (1, 1, 2, 'RADOMIR', 18, 'hello this is Rado')
    assert check_header(
        create_header('chat','send message',2,'JACQUELINE','hello this is Jacqueline')) == (1, 1, 2, 'JACQUELINE', 24, 'hello this is Jacqueline')