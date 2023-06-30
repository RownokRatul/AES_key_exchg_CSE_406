import random
from timeit import default_timer
from tabulate import tabulate

elapsed_time = []

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
    # print("Primitive root:", g)
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
    p_dash = (primeCandidate(bit_len-1) << 1) + 1 # safe primes are 2q + 1 
    while Miller_Rabin(p_dash) == False :
        p_dash =  (primeCandidate(bit_len) << 1) + 1
    return p_dash


def printTimeSummary() :
    print(tabulate(elapsed_time, headers=["Key-Length", "p", "g", "a", "A", "b", "B", "Shared Key"], floatfmt=".4f", tablefmt="simple_grid"))


def Diffie_Hellman_exchange(key_len) :
    # public key bases
    time_p_start = default_timer()
    p = generateSafePrime(key_len)
    time_p_end = default_timer()
    g = primitiveRootSafePrime(p, 2, p-2)
    time_g_end = default_timer()
    # print("p, g:", p, g)
    # Alice
    red = random.randrange(0, key_len//2)
    time_a_start = default_timer()
    a = generatePrime(key_len - red)
    time_a_end = default_timer()
    A = modularExponentiation(g, a, p)
    time_A_end = default_timer()
    # print("Alice:", a, A)
    # Bob
    red = random.randrange(0, key_len//2)
    time_b_start = default_timer()
    b = generatePrime(key_len - red)
    time_b_end = default_timer()
    B = modularExponentiation(g, b, p)
    time_B_end = default_timer()
    # print("Bob:", b, B)

    # let the key has been exchanged

    # Alice's retrieval
    timer_ka_start = default_timer()
    ka = modularExponentiation(B, a, p)
    timer_ka_end = default_timer()
    # print("Alice gets:", ka)
    # Bob's retrieval
    timer_kb_start = default_timer()
    kb = modularExponentiation(A, b, p)
    timer_kb_end = default_timer()
    # print("Bob gets:", kb)

    if ka == kb :
        print("Successfully key exchanged: ", ka)
    
    elapsed_time.append([key_len, (time_p_end-time_p_start)*1000, (time_g_end-time_p_end)*1000, (time_a_end-time_a_start)*1000, (time_A_end-time_a_end)*1000, (time_b_end-time_b_start)*1000, (time_B_end-time_b_end)*1000, (timer_ka_end-timer_ka_start)*1000])

# main
def test() :
    for i in [128, 192, 256] :
        Diffie_Hellman_exchange(i)
    printTimeSummary()
test()
