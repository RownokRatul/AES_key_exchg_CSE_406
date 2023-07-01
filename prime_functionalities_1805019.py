import random


def modularExponentiation(b, p, m) :
    if p == 0 :
        return 1
    elif p & 1 :
        temp = modularExponentiation(b, (p-1)//2, m)
        return (temp*temp*b) % m
    else :
        temp = modularExponentiation(b, p//2, m)
        return (temp*temp) % m


def Miller_Rabin(p, max_iter=100) : 
    if p == 2 :
        return True
    s = 0
    r = p - 1
    while (r & 1) == 0 :
        s += 1
        r >>= 1
    for i in range(max_iter) :
        a = random.randrange(2, p-1)
        rem = modularExponentiation(a, r, p)
        if rem != 1 and rem != p-1 : 
            for j in range(1, s) :
                rem = modularExponentiation(rem, 2, p)
                if rem == 1 :
                    return False
            if rem != p-1 :
                return False     
    return True


def primitiveRootSafePrime(p, mn, mx) :
    g = random.randrange(mn, mx)
    # 2 and (p-1)/2 divides p-1, as p is safe prime
    while modularExponentiation(g, 2, p) == 1 or modularExponentiation(g, (p-1)//2, p) == 1 :
        g = random.randrange(2, p-1)
    return g


def primeCandidate(n):
    # generate a random odd integer of n bits
    p = random.getrandbits(n)
    p = ((1 << (n-1)) | 1) | p
    return p


def generatePrime(bit_len) :
    p_dash = primeCandidate(bit_len)
    while Miller_Rabin(p_dash) == False :
        p_dash = primeCandidate(bit_len)
    return p_dash


def generateSafePrime(bit_len) : 
    # safe primes are 2q + 1 
    p_dash = (primeCandidate(bit_len-1) << 1) + 1 
    while Miller_Rabin(p_dash) == False :
        p_dash =  (primeCandidate(bit_len) << 1) + 1
    return p_dash


# for socket
def get_diffie_hellman_public_key_pair(key_len) :
    p = generateSafePrime(key_len)
    g = primitiveRootSafePrime(p, 3, p-2)
    return p, g