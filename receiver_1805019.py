import socket
import sys
from prime_functionalities_1805019 import *
from AES_1805019 import *

def openSocket(port):
    try:
        s = socket.socket()
        s.bind(('127.0.0.1', port))
        s.listen(1)
        print("Receiver: listening on", port)
        con, addr = s.accept()
        print("Sender Req Accepted!")
        return con
    except socket.error as err:
        print("Error Opening socket in Receiver!")
        sys.exit()


def sendInt(x, soc) :
    soc.send(x.to_bytes(32, 'big'))


def sendStr(s, soc) :
    sendInt(len(s), soc)
    soc.sendall(s.encode())


def recvInt(soc):
    i = int.from_bytes(soc.recv(32), 'big')
    return i


def recvStr(soc):
    msg_len = recvInt(soc)
    msg = ''
    while len(msg) < msg_len :
        data = soc.recv(min(4096, msg_len-len(msg))).decode()
        msg += data
    return msg


def init_receiver(port, key_len):    
    # key exchange
    soc = openSocket(port)
    p = recvInt(soc)
    g = recvInt(soc)
    alice_public = recvInt(soc)

    # key generation
    bob_secret = generatePrime(key_len-random.randrange(0, key_len//2))
    bob_public = modularExponentiation(g, bob_secret, p)
    sendInt(bob_public, soc)
    secret_key = modularExponentiation(alice_public, bob_secret, p)

    print("-----Receiver (Bob)-----\np: ", p, "\ng: ", g, "\nb: ", bob_secret, "\nshared_key: ", secret_key)

    # receive and decrypt
    cipherHex = recvStr(soc)
    cipher = BitVector(hexstring=cipherHex).get_bitvector_in_ascii()
    plain = decrypt_aes128(cipher, integer_to_ascii_string(secret_key))
    print("\n\n\nReceived Cipher:\n\n\n ", cipher)
    print("\n\nPlain Text:\n\n ", plain)
    soc.close()


port = 12345
key_len = 128
init_receiver(port, key_len)