import socket
import sys
from BitVector import *
from prime_functionalities_1805019 import *
from AES_1805019 import *


def openSocket(port):
    try :
        s = socket.socket()
        s.connect(('127.0.0.1', port))
        print("Successfully connected to receiver")
        return s
    except socket.error as err :
        print("socket connection failed on Sender!")
        sys.exit()


def sendInt(x, soc) :
    soc.send(x.to_bytes(32, 'big'))


def sendStr(s, soc) :
    sendInt(len(s), soc)
    soc.sendall(s.encode())


def recvInt(soc):
    i = int.from_bytes(soc.recv(32), 'big')
    return i


def init_sender(text, port, key_len) :
    # key generation
    p, g = get_diffie_hellman_public_key_pair(key_len)
    alice_secret = generatePrime(key_len-random.randrange(0, key_len//2))
    alice_public = modularExponentiation(g, alice_secret, p)

    # key exchange
    soc = openSocket(port)
    for each in [p, g, alice_public]:
        sendInt(each, soc)
    bob_public = recvInt(soc)
    secret_key = modularExponentiation(bob_public, alice_secret, p)

    print("-----Sender (Alice)-----\np: ", p, "\ng: ", g, "\na: ", alice_secret, "\nshared_key: ", secret_key)

    # encrypt and send
    cipher = encrypt_aes128(text, integer_to_ascii_string(secret_key))
    cipherHex = BitVector(textstring=cipher).get_bitvector_in_hex()
    sendStr(cipherHex, soc)

    print("Plain Text: ", text, "\n\n\ncipher:\n\n\n ", cipher)

    soc.close()



print("Input Text to Send: ")
text = input()
port = 12345
key_len = 128
init_sender(text, port, key_len)